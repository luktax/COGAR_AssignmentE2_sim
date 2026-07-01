#!/usr/bin/env python3
"""
Flat-ground parameter sweep for Unitree Go2 + convex MPC.

Run one parameter sweep at a time on flat terrain, save raw logs, summary metrics,
and plots for:
  - velocity tracking error
  - body height tracking error
  - pitch variation
  - roll variation

Example:
  python3 experiments/flat_param_sweep.py --sweep body_height
  python3 experiments/flat_param_sweep.py --sweep velocity
  python3 experiments/flat_param_sweep.py --sweep swing_height
  python3 experiments/flat_param_sweep.py --sweep duty
  python3 experiments/flat_param_sweep.py --sweep gait_hz

Custom range:
  python3 experiments/flat_param_sweep.py --sweep body_height --min 0.26 --max 0.34 --num 5
"""

import argparse
import csv
import json
import math
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import mujoco as mj
import mujoco.viewer as mjv
import numpy as np

from convex_mpc.go2_robot_data import PinGo2Model
from convex_mpc.mujoco_model import MuJoCo_GO2_Model
from convex_mpc.com_trajectory import ComTraj
from convex_mpc.centroidal_mpc import CentroidalMPC
from convex_mpc.leg_controller import LegController
from convex_mpc.gait import Gait


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

@dataclass
class ExperimentConfig:
    # Simulation
    run_sim_length_s: float = 7.0
    sim_hz: int = 1000
    ctrl_hz: int = 200

    # Viewer
    enable_viewer: bool = False
    viewer_hz: float = 60.0
    viewer_realtime: bool = True

    # Initial pose
    initial_x: float = 0.0
    initial_y: float = 0.0
    initial_z: float = 0.27

    # Flat experiment references
    x_vel_des: float = 0.25
    y_vel_des: float = 0.0
    yaw_rate_des: float = 0.0
    z_pos_des: float = 0.29
    pitch_ref_deg: float = 0.0

    # Terrain
    step_height: float = 0.0
    step_front_x: float = 0.85
    step_depth: float = 0.80

    # Gait parameters
    gait_hz: float = 3.0
    gait_duty: float = 0.60
    height_swing: float = 0.10
    phase_offset: Tuple[float, float, float, float] = (0.5, 0.0, 0.0, 0.5)

    # Command schedule
    stand_time_s: float = 1.0
    stop_time_s: float = 1.0

    # Failure thresholds
    min_base_height_failure: float = 0.14
    max_abs_roll_failure_rad: float = math.radians(35.0)
    max_abs_pitch_failure_rad: float = math.radians(45.0)
    max_contact_force_failure_n: float = 2500.0

    @property
    def sim_dt(self) -> float:
        return 1.0 / self.sim_hz

    @property
    def ctrl_dt(self) -> float:
        return 1.0 / self.ctrl_hz

    @property
    def pitch_ref(self) -> float:
        return math.radians(self.pitch_ref_deg)


@dataclass
class BodyCmdPhase:
    t_start: float
    t_end: float
    x_vel: float
    y_vel: float
    z_pos: float
    yaw_rate: float
    pitch: float


@dataclass
class TrialMetrics:
    success: bool = False
    failure_reason: str = "none"
    final_base_x: float = 0.0
    min_base_z: float = 999.0
    max_base_z: float = -999.0
    max_abs_roll_deg: float = 0.0
    max_abs_pitch_deg: float = 0.0
    max_contact_force_n: float = 0.0
    elapsed_wall_s: float = 0.0


@dataclass
class TrialResult:
    metrics: TrialMetrics
    raw_path: Path
    row: Dict[str, float]


LEG_SLICE = {
    "FL": slice(0, 3),
    "FR": slice(3, 6),
    "RL": slice(6, 9),
    "RR": slice(9, 12),
}

HIP_LIM = 23.7
ABD_LIM = 23.7
KNEE_LIM = 45.43
SAFETY = 0.9
TAU_LIM = SAFETY * np.array([
    HIP_LIM, ABD_LIM, KNEE_LIM,   # FL
    HIP_LIM, ABD_LIM, KNEE_LIM,   # FR
    HIP_LIM, ABD_LIM, KNEE_LIM,   # RL
    HIP_LIM, ABD_LIM, KNEE_LIM,   # RR
])

PRESETS = {
    # sweep_name: config field, min, max, num values
    "body_height": ("z_pos_des", 0.20, 0.35, 8),
    "velocity": ("x_vel_des", 0.10, 1.5, 10),
    "swing_height": ("height_swing", 0.06, 0.22, 6),
    "gait_hz": ("gait_hz", 2.0, 4.0, 6),
    "duty": ("gait_duty", 0.30, 0.90, 6),
    "pitch": ("pitch_ref_deg", -20.0, 20.0, 8),
    "step_height": ("step_height", 0.02, 0.22, 10),
}

# -----------------------------------------------------------------------------
# Utility
# -----------------------------------------------------------------------------

def find_repo_root() -> Path:
    cwd = Path.cwd().resolve()
    for p in [cwd, *cwd.parents]:
        if (p / "models" / "MJCF" / "go2" / "go2.xml").exists():
            return p
    raise RuntimeError(
        "Could not find COGAR_project root. Run this script from inside the project, "
        "where models/MJCF/go2/go2.xml exists."
    )

def write_single_step_world(
    repo_root: Path,
    step_height: float,
    step_front_x: float = 0.85,
    step_depth: float = 0.80,
    step_width: float = 1.50,
) -> Path:
    world_path = repo_root / "models" / "MJCF" / "go2" / "generated_single_step_world.xml"

    step_center_x = step_front_x + step_depth / 2.0
    step_center_z = step_height / 2.0

    xml = f"""<mujoco model="go2 single step sweep">
  <include file="go2.xml"/>

  <statistic center="0 0 0.1" extent="0.8"/>

  <visual>
    <headlight diffuse="0.6 0.6 0.6" ambient="0.3 0.3 0.3" specular="0 0 0"/>
    <rgba haze="0.15 0.25 0.35 1"/>
    <global azimuth="-130" elevation="-20"/>
  </visual>

  <asset>
    <texture type="skybox" builtin="gradient"
             rgb1="0.3 0.5 0.7" rgb2="0 0 0"
             width="512" height="3072"/>
    <texture type="2d" name="groundplane" builtin="checker" mark="edge"
             rgb1="0.2 0.3 0.4" rgb2="0.1 0.2 0.3"
             markrgb="0.8 0.8 0.8"
             width="300" height="300"/>
    <material name="groundplane"
              texture="groundplane"
              texuniform="true"
              texrepeat="5 5"
              reflectance="0.2"/>
  </asset>

  <worldbody>
    <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>

    <geom name="floor"
          type="plane"
          size="0 0 0.05"
          material="groundplane"
          friction="1.2 0.005 0.0001"/>

    <geom name="single_step"
          type="box"
          pos="{step_center_x:.4f} 0 {step_center_z:.4f}"
          size="{step_depth / 2.0:.4f} {step_width / 2.0:.4f} {step_height / 2.0:.4f}"
          friction="1.2 0.005 0.0001"/>
  </worldbody>
</mujoco>
"""

    world_path.write_text(xml)
    return world_path


def build_cmd_schedule(cfg: ExperimentConfig) -> List[BodyCmdPhase]:
    return [
        BodyCmdPhase(0.0, cfg.stand_time_s, 0.0, 0.0, cfg.z_pos_des, 0.0, 0.0),
        BodyCmdPhase(
            cfg.stand_time_s,
            cfg.run_sim_length_s - cfg.stop_time_s,
            cfg.x_vel_des,
            cfg.y_vel_des,
            cfg.z_pos_des,
            cfg.yaw_rate_des,
            cfg.pitch_ref,
        ),
        BodyCmdPhase(
            cfg.run_sim_length_s - cfg.stop_time_s,
            cfg.run_sim_length_s + 1e-9,
            0.0,
            0.0,
            cfg.z_pos_des,
            0.0,
            0.0,
        ),
    ]


def get_body_cmd(t: float, schedule: List[BodyCmdPhase]) -> Tuple[float, float, float, float, float]:
    for phase in schedule:
        if phase.t_start <= t < phase.t_end:
            return phase.x_vel, phase.y_vel, phase.z_pos, phase.yaw_rate, phase.pitch
    return 0.0, 0.0, 0.27, 0.0, 0.0


def get_contacts_and_max_force(mujoco_go2: MuJoCo_GO2_Model) -> float:
    force6 = np.zeros(6, dtype=float)
    max_force = 0.0
    for i in range(mujoco_go2.data.ncon):
        mj.mj_contactForce(mujoco_go2.model, mujoco_go2.data, i, force6)
        max_force = max(max_force, float(np.linalg.norm(force6[:3])))
    return max_force


def update_metrics(metrics: TrialMetrics, go2: PinGo2Model, max_contact_force: float) -> None:
    x_vec = go2.compute_com_x_vec().reshape(-1)
    base_x = float(go2.current_config.base_pos[0])
    base_z = float(go2.current_config.base_pos[2])
    roll = float(x_vec[3])
    pitch = float(x_vec[4])

    metrics.final_base_x = base_x
    metrics.min_base_z = min(metrics.min_base_z, base_z)
    metrics.max_base_z = max(metrics.max_base_z, base_z)
    metrics.max_abs_roll_deg = max(metrics.max_abs_roll_deg, abs(math.degrees(roll)))
    metrics.max_abs_pitch_deg = max(metrics.max_abs_pitch_deg, abs(math.degrees(pitch)))
    metrics.max_contact_force_n = max(metrics.max_contact_force_n, max_contact_force)


def detect_failure(cfg: ExperimentConfig, metrics: TrialMetrics) -> Optional[str]:
    if metrics.min_base_z < cfg.min_base_height_failure:
        return "base_too_low"
    if math.radians(metrics.max_abs_roll_deg) > cfg.max_abs_roll_failure_rad:
        return "roll_limit"
    if math.radians(metrics.max_abs_pitch_deg) > cfg.max_abs_pitch_failure_rad:
        return "pitch_limit"
    if metrics.max_contact_force_n > cfg.max_contact_force_failure_n:
        return "contact_force_limit"
    return None


def rmse(x: np.ndarray) -> float:
    if x.size == 0:
        return float("nan")
    return float(np.sqrt(np.mean(x ** 2)))


def mae(x: np.ndarray) -> float:
    if x.size == 0:
        return float("nan")
    return float(np.mean(np.abs(x)))


def max_abs(x: np.ndarray) -> float:
    if x.size == 0:
        return float("nan")
    return float(np.max(np.abs(x)))


# -----------------------------------------------------------------------------
# Trial execution
# -----------------------------------------------------------------------------

def run_trial(cfg: ExperimentConfig, trial_name: str, raw_dir: Path, sweep_name: str, sweep_value: float) -> TrialResult:
    if cfg.sim_hz % cfg.ctrl_hz != 0:
        raise ValueError(f"sim_hz ({cfg.sim_hz}) must be divisible by ctrl_hz ({cfg.ctrl_hz}).")

    sim_steps = int(cfg.run_sim_length_s * cfg.sim_hz)
    ctrl_steps = int(cfg.run_sim_length_s * cfg.ctrl_hz)
    ctrl_decim = cfg.sim_hz // cfg.ctrl_hz

    gait_t = 1.0 / cfg.gait_hz
    mpc_dt = gait_t / 16.0
    mpc_hz = 1.0 / mpc_dt
    steps_per_mpc = max(1, int(cfg.ctrl_hz // mpc_hz))

    print("\n" + "=" * 88)
    print(f"TRIAL {trial_name}")
    print("=" * 88)
    print(f"sweep             = {sweep_name} = {sweep_value:.4f}")
    print(f"x_vel_des         = {cfg.x_vel_des:.3f} m/s")
    print(f"body_height       = {cfg.z_pos_des:.3f} m")
    print(f"height_swing      = {cfg.height_swing:.3f} m")
    print(f"gait_hz           = {cfg.gait_hz:.2f} Hz")
    print(f"gait_duty         = {cfg.gait_duty:.2f}")
    print(f"pitch_ref         = {cfg.pitch_ref_deg:.2f} deg")
    print(f"mpc_dt            = {mpc_dt * 1000:.2f} ms")
    print(f"steps_per_mpc     = {steps_per_mpc}")

    schedule = build_cmd_schedule(cfg)

    # Logs at control rate.
    time_log = np.zeros(ctrl_steps)
    cmd_log = np.zeros((ctrl_steps, 5))       # x_vel, y_vel, z_pos, yaw_rate, pitch_ref
    base_log = np.zeros((ctrl_steps, 9))      # base x,y,z, roll,pitch,yaw, vx,vy,vz
    x_vec_log = np.zeros((ctrl_steps, 12))
    tau_cmd_log = np.zeros((ctrl_steps, 12))
    mpc_force_log = np.zeros((ctrl_steps, 12))
    contact_force_log = np.zeros(ctrl_steps)

    mpc_update_time_ms: List[float] = []
    mpc_solve_time_ms: List[float] = []

    go2 = PinGo2Model()
    mujoco_go2 = MuJoCo_GO2_Model()
    leg_controller = LegController()

    mujoco_go2.model.opt.timestep = cfg.sim_dt

    q_init = go2.current_config.get_q().copy()
    q_init[0] = cfg.initial_x
    q_init[1] = cfg.initial_y
    q_init[2] = cfg.initial_z
    q_init[3:7] = np.array([0.0, 0.0, 0.0, 1.0])
    mujoco_go2.update_with_q_pin(q_init)
    mujoco_go2.update_pin_with_mujoco(go2)

    gait = Gait(
        cfg.gait_hz,
        cfg.gait_duty,
        cfg.height_swing,
        np.asarray(cfg.phase_offset, dtype=float),
    )
    traj = ComTraj(go2)

    traj.generate_traj(
        go2,
        gait,
        0.0,
        0.0,
        0.0,
        cfg.z_pos_des,
        0.0,
        cfg.pitch_ref,
        time_step=mpc_dt,
    )
    mpc = CentroidalMPC(go2, traj)
    U_opt = np.zeros((12, traj.N), dtype=float)

    metrics = TrialMetrics()
    ctrl_i = 0
    tau_hold = np.zeros(12, dtype=float)
    sim_start_wall = time.perf_counter()

    viewer_cm = None
    viewer = None
    next_viewer_t = 0.0
    viewer_dt = 1.0 / cfg.viewer_hz
    viewer_wall_start = time.perf_counter()

    if cfg.enable_viewer:
        viewer_cm = mjv.launch_passive(mujoco_go2.model, mujoco_go2.data)
        viewer = viewer_cm.__enter__()

        viewer.cam.type = mj.mjtCamera.mjCAMERA_TRACKING
        viewer.cam.trackbodyid = mujoco_go2.base_bid
        viewer.cam.distance = 2.0
        viewer.cam.elevation = -20
        viewer.cam.azimuth = 90

        viewer.opt.flags[mj.mjtVisFlag.mjVIS_CONTACTPOINT] = True

    for k in range(sim_steps):
        time_now_s = float(mujoco_go2.data.time)

        if (k % ctrl_decim) == 0 and ctrl_i < ctrl_steps:
            x_vel, y_vel, z_pos, yaw_rate, pitch_ref = get_body_cmd(time_now_s, schedule)

            mujoco_go2.update_pin_with_mujoco(go2)
            x_vec = go2.compute_com_x_vec().reshape(-1)
            max_force = get_contacts_and_max_force(mujoco_go2)

            update_metrics(metrics, go2, max_force)
            failure = detect_failure(cfg, metrics)
            if failure is not None:
                metrics.success = False
                metrics.failure_reason = failure
                print(f"\n[FAIL] t={time_now_s:.3f}s reason={failure}")
                break

            time_log[ctrl_i] = time_now_s
            cmd_log[ctrl_i, :] = [x_vel, y_vel, z_pos, yaw_rate, pitch_ref]
            x_vec_log[ctrl_i, :] = x_vec
            base_log[ctrl_i, :] = [
                float(go2.current_config.base_pos[0]),
                float(go2.current_config.base_pos[1]),
                float(go2.current_config.base_pos[2]),
                float(x_vec[3]),
                float(x_vec[4]),
                float(x_vec[5]),
                float(x_vec[6]),
                float(x_vec[7]),
                float(x_vec[8]),
            ]
            contact_force_log[ctrl_i] = max_force

            if (ctrl_i % steps_per_mpc) == 0:
                print(f"\rSimulation Time: {time_now_s:.3f} s", end="", flush=True)

                traj.generate_traj(
                    go2,
                    gait,
                    time_now_s,
                    x_vel,
                    y_vel,
                    z_pos,
                    yaw_rate,
                    pitch_ref,
                    time_step=mpc_dt,
                )

                sol = mpc.solve_QP(go2, traj, False)
                if sol is not None:
                    mpc_solve_time_ms.append(float(mpc.solve_time))
                    mpc_update_time_ms.append(float(mpc.update_time))
                    n_horizon = traj.N
                    w_opt = sol["x"].full().flatten()
                    U_opt = w_opt[12 * n_horizon:].reshape((12, n_horizon), order="F")
                else:
                    print(f"\n[WARN] MPC returned None at t={time_now_s:.3f}s; reusing previous U_opt")

            mpc_force_log[ctrl_i, :] = U_opt[:, 0]

            tau_raw = np.zeros(12, dtype=float)
            for leg in ("FL", "FR", "RL", "RR"):
                sl = LEG_SLICE[leg]
                out = leg_controller.compute_leg_torque(
                    leg,
                    go2,
                    gait,
                    mpc_force_log[ctrl_i, sl],
                    time_now_s,
                )
                tau_raw[sl] = out.tau

            tau_hold = np.clip(tau_raw, -TAU_LIM, TAU_LIM)
            tau_cmd_log[ctrl_i, :] = tau_hold
            ctrl_i += 1

        # Lockstep/offline dynamics.
        mj.mj_step1(mujoco_go2.model, mujoco_go2.data)
        mujoco_go2.set_joint_torque(tau_hold)
        mj.mj_step2(mujoco_go2.model, mujoco_go2.data)

        if viewer is not None:
            t_after = float(mujoco_go2.data.time)

            if t_after >= next_viewer_t:
                if not viewer.is_running():
                    print("\n[VIEWER CLOSED] continuing without viewer...")
                    viewer_cm.__exit__(None, None, None)
                    viewer = None
                    viewer_cm = None
                else:
                    viewer.sync()

                    if cfg.viewer_realtime:
                        target_wall = viewer_wall_start + t_after
                        sleep_time = target_wall - time.perf_counter()
                        if sleep_time > 0.0:
                            time.sleep(min(sleep_time, 0.02))

                    next_viewer_t += viewer_dt

    metrics.elapsed_wall_s = time.perf_counter() - sim_start_wall

    # Crop logs.
    time_log = time_log[:ctrl_i]
    cmd_log = cmd_log[:ctrl_i]
    base_log = base_log[:ctrl_i]
    x_vec_log = x_vec_log[:ctrl_i]
    tau_cmd_log = tau_cmd_log[:ctrl_i]
    mpc_force_log = mpc_force_log[:ctrl_i]
    contact_force_log = contact_force_log[:ctrl_i]

    # Success criterion for flat walking: no failure and at least meaningful progress.
    if metrics.failure_reason == "none":
        motion_duration = max(0.0, cfg.run_sim_length_s - cfg.stand_time_s - cfg.stop_time_s)
        expected_progress = max(0.0, cfg.x_vel_des * motion_duration)
        min_required_progress = min(0.20, expected_progress * 0.40) if expected_progress > 0 else 0.0
        metrics.success = metrics.final_base_x >= min_required_progress
        if not metrics.success:
            metrics.failure_reason = "not_enough_forward_progress"

    row = compute_tracking_metrics(cfg, metrics, time_log, cmd_log, base_log)
    row.update({
        "trial_name": trial_name,
        "sweep_name": sweep_name,
        "sweep_value": float(sweep_value),
        "success": int(metrics.success),
        "failure_reason": metrics.failure_reason,
        "final_base_x": float(metrics.final_base_x),
        "elapsed_wall_s": float(metrics.elapsed_wall_s),
        "max_contact_force_n": float(metrics.max_contact_force_n),
        "mean_mpc_update_ms": float(np.mean(mpc_update_time_ms)) if mpc_update_time_ms else float("nan"),
        "mean_mpc_solve_ms": float(np.mean(mpc_solve_time_ms)) if mpc_solve_time_ms else float("nan"),
        "x_vel_des_cfg": float(cfg.x_vel_des),
        "z_pos_des_cfg": float(cfg.z_pos_des),
        "height_swing_cfg": float(cfg.height_swing),
        "gait_hz_cfg": float(cfg.gait_hz),
        "gait_duty_cfg": float(cfg.gait_duty),
        "pitch_ref_deg_cfg": float(cfg.pitch_ref_deg),
    })

    raw_path = raw_dir / f"{trial_name}.npz"
    np.savez_compressed(
        raw_path,
        t=time_log,
        cmd=cmd_log,
        base=base_log,
        x_vec=x_vec_log,
        tau=tau_cmd_log,
        mpc_force=mpc_force_log,
        contact_force=contact_force_log,
        config_json=json.dumps(asdict(cfg)),
        metrics_json=json.dumps(row),
    )

    print("\n\nTrial ended.")
    print(f"success            = {metrics.success}")
    print(f"failure_reason     = {metrics.failure_reason}")
    print(f"final_base_x       = {metrics.final_base_x:.3f} m")
    print(f"vx_rmse            = {row['vx_error_rmse']:.4f} m/s")
    print(f"body_z_rmse        = {row['body_z_error_rmse']:.4f} m")
    print(f"pitch_max_abs_delta= {row['pitch_delta_max_abs_deg']:.2f} deg")
    print(f"roll_max_abs_delta = {row['roll_delta_max_abs_deg']:.2f} deg")
    print(f"raw log            = {raw_path}")

    if viewer_cm is not None:
        viewer_cm.__exit__(None, None, None)

    return TrialResult(metrics=metrics, raw_path=raw_path, row=row)


def compute_tracking_metrics(
    cfg: ExperimentConfig,
    metrics: TrialMetrics,
    t: np.ndarray,
    cmd: np.ndarray,
    base: np.ndarray,
) -> Dict[str, float]:
    if len(t) == 0:
        return {}

    stand_mask = t < cfg.stand_time_s
    motion_mask = (t >= cfg.stand_time_s) & (t <= cfg.run_sim_length_s - cfg.stop_time_s)

    if not np.any(stand_mask):
        stand_mask = np.arange(len(t)) < max(1, min(20, len(t)))
    if not np.any(motion_mask):
        motion_mask = np.ones(len(t), dtype=bool)

    vx_meas = base[:, 6]
    vx_des = cmd[:, 0]
    body_z_meas = base[:, 2]
    body_z_des = cmd[:, 2]
    roll = base[:, 3]
    pitch = base[:, 4]

    roll0 = float(np.mean(roll[stand_mask]))
    pitch0 = float(np.mean(pitch[stand_mask]))

    vx_err = vx_meas[motion_mask] - vx_des[motion_mask]
    body_z_err = body_z_meas[motion_mask] - body_z_des[motion_mask]

    roll_delta = roll[motion_mask] - roll0
    pitch_delta = pitch[motion_mask] - pitch0

    roll_delta_deg = np.degrees(roll_delta)
    pitch_delta_deg = np.degrees(pitch_delta)

    return {
        "vx_des_mean": float(np.mean(vx_des[motion_mask])),
        "vx_meas_mean": float(np.mean(vx_meas[motion_mask])),
        "vx_error_mean": float(np.mean(vx_err)),
        "vx_error_rmse": rmse(vx_err),
        "vx_error_mae": mae(vx_err),
        "vx_error_max_abs": max_abs(vx_err),

        "body_z_des_mean": float(np.mean(body_z_des[motion_mask])),
        "body_z_meas_mean": float(np.mean(body_z_meas[motion_mask])),
        "body_z_error_mean": float(np.mean(body_z_err)),
        "body_z_error_rmse": rmse(body_z_err),
        "body_z_error_mae": mae(body_z_err),
        "body_z_error_max_abs": max_abs(body_z_err),

        "roll0_deg": float(math.degrees(roll0)),
        "roll_mean_delta_deg": float(np.mean(roll_delta_deg)),
        "roll_std_delta_deg": float(np.std(roll_delta_deg)),
        "roll_min_delta_deg": float(np.min(roll_delta_deg)),
        "roll_max_delta_deg": float(np.max(roll_delta_deg)),
        "roll_range_deg": float(np.max(roll_delta_deg) - np.min(roll_delta_deg)),
        "roll_delta_max_abs_deg": max_abs(roll_delta_deg),

        "pitch0_deg": float(math.degrees(pitch0)),
        "pitch_mean_delta_deg": float(np.mean(pitch_delta_deg)),
        "pitch_std_delta_deg": float(np.std(pitch_delta_deg)),
        "pitch_min_delta_deg": float(np.min(pitch_delta_deg)),
        "pitch_max_delta_deg": float(np.max(pitch_delta_deg)),
        "pitch_range_deg": float(np.max(pitch_delta_deg) - np.min(pitch_delta_deg)),
        "pitch_delta_max_abs_deg": max_abs(pitch_delta_deg),

        "min_base_z": float(metrics.min_base_z),
        "max_base_z": float(metrics.max_base_z),
        "max_abs_roll_deg_global": float(metrics.max_abs_roll_deg),
        "max_abs_pitch_deg_global": float(metrics.max_abs_pitch_deg),
    }


# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------

def plot_timeseries(raw_paths: List[Path], summary_rows: List[Dict[str, float]], plot_dir: Path, sweep_name: str) -> Path:
    fig, axes = plt.subplots(4, 1, figsize=(12, 12), sharex=True)

    for raw_path, row in zip(raw_paths, summary_rows):
        data = np.load(raw_path, allow_pickle=True)
        t = data["t"]
        cmd = data["cmd"]
        base = data["base"]
        label = f"{row['sweep_value']:.3f}"

        axes[0].plot(t, base[:, 6], label=label)
        axes[1].plot(t, base[:, 2], label=label)

        # Use initial standing mean as zero reference for attitude variation.
        stand_mask = t < 1.0
        if not np.any(stand_mask):
            stand_mask = np.arange(len(t)) < max(1, min(20, len(t)))
        pitch0 = np.mean(base[stand_mask, 4])
        roll0 = np.mean(base[stand_mask, 3])
        axes[2].plot(t, np.degrees(base[:, 4] - pitch0), label=label)
        axes[3].plot(t, np.degrees(base[:, 3] - roll0), label=label)

    # Desired references from first trial.
    if raw_paths:
        data0 = np.load(raw_paths[0], allow_pickle=True)
        t0 = data0["t"]
        cmd0 = data0["cmd"]
        axes[0].plot(t0, cmd0[:, 0], "--", linewidth=2, label="desired")
        axes[1].plot(t0, cmd0[:, 2], "--", linewidth=2, label="desired")

    axes[0].set_ylabel("vx [m/s]")
    axes[0].set_title(f"{sweep_name}: velocity tracking")
    axes[0].grid(True)

    axes[1].set_ylabel("base z [m]")
    axes[1].set_title(f"{sweep_name}: body height tracking")
    axes[1].grid(True)

    axes[2].set_ylabel("pitch delta [deg]")
    axes[2].set_title(f"{sweep_name}: pitch variation")
    axes[2].grid(True)

    axes[3].set_ylabel("roll delta [deg]")
    axes[3].set_xlabel("time [s]")
    axes[3].set_title(f"{sweep_name}: roll variation")
    axes[3].grid(True)

    for ax in axes:
        ax.legend(title=sweep_name, fontsize=8)

    fig.tight_layout()
    out = plot_dir / f"{sweep_name}_timeseries.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out


def plot_summary(summary_rows: List[Dict[str, float]], plot_dir: Path, sweep_name: str) -> Path:
    values = np.array([float(r["sweep_value"]) for r in summary_rows])
    vx_rmse = np.array([float(r["vx_error_rmse"]) for r in summary_rows])
    z_rmse = np.array([float(r["body_z_error_rmse"]) for r in summary_rows])
    pitch_max = np.array([float(r["pitch_delta_max_abs_deg"]) for r in summary_rows])
    roll_max = np.array([float(r["roll_delta_max_abs_deg"]) for r in summary_rows])
    success = np.array([int(r["success"]) for r in summary_rows])

    fig, axes = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

    axes[0].plot(values, vx_rmse, marker="o")
    axes[0].set_ylabel("vx RMSE [m/s]")
    axes[0].set_title("Velocity tracking error")
    axes[0].grid(True)

    axes[1].plot(values, z_rmse, marker="o")
    axes[1].set_ylabel("base z RMSE [m]")
    axes[1].set_title("Body height tracking error")
    axes[1].grid(True)

    axes[2].plot(values, pitch_max, marker="o", label="pitch")
    axes[2].plot(values, roll_max, marker="o", label="roll")
    axes[2].set_ylabel("max abs delta [deg]")
    axes[2].set_title("Pitch and roll variation")
    axes[2].legend()
    axes[2].grid(True)

    axes[3].plot(values, success, marker="o")
    axes[3].set_ylabel("success [0/1]")
    axes[3].set_xlabel(sweep_name)
    axes[3].set_yticks([0, 1])
    axes[3].set_title("Trial success")
    axes[3].grid(True)

    fig.tight_layout()
    out = plot_dir / f"{sweep_name}_summary.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out


# -----------------------------------------------------------------------------
# Main sweep
# -----------------------------------------------------------------------------

def build_cfg_from_baseline(baseline: ExperimentConfig, field_name: str, value: float) -> ExperimentConfig:
    cfg = ExperimentConfig(**asdict(baseline))
    setattr(cfg, field_name, float(value))
    return cfg


def safe_value_name(value: float) -> str:
    return f"{value:.4f}".replace("-", "m").replace(".", "p")


def run_sweep(args) -> None:
    if args.sweep not in PRESETS:
        raise ValueError(f"Unknown sweep '{args.sweep}'. Available: {list(PRESETS.keys())}")

    field_name, default_min, default_max, default_num = PRESETS[args.sweep]
    vmin = args.min if args.min is not None else default_min
    vmax = args.max if args.max is not None else default_max
    num = args.num if args.num is not None else default_num
    values = np.linspace(vmin, vmax, num)

    repo_root = find_repo_root()
    stamp = time.strftime("%Y%m%d_%H%M%S")

    out_root = repo_root / "results" / f"sweep_{args.sweep}_{stamp}"
    raw_dir = out_root / "raw"
    plot_dir = out_root / "plots"
    raw_dir.mkdir(parents=True, exist_ok=True)
    plot_dir.mkdir(parents=True, exist_ok=True)

    baseline = ExperimentConfig(
        run_sim_length_s=args.duration,
        x_vel_des=args.base_velocity,
        z_pos_des=args.base_body_height,
        height_swing=args.base_swing_height,
        gait_hz=args.base_gait_hz,
        gait_duty=args.base_duty,
        pitch_ref_deg=args.base_pitch_deg,
        enable_viewer=args.viewer,
        viewer_hz=args.viewer_fps,
    )

    summary_rows: List[Dict[str, float]] = []
    raw_paths: List[Path] = []

    print("\n" + "=" * 88)
    print("STARTING PARAMETER SWEEP")
    print("=" * 88)
    print("World file is selected directly inside convex_mpc/mujoco_model.py")
    print(f"sweep: {args.sweep}")
    print(f"field: {field_name}")
    print(f"values: {values}")

    for i, value in enumerate(values):
        cfg = build_cfg_from_baseline(baseline, field_name, float(value))
        if args.sweep == "step_height":
            world_path = write_single_step_world(
                repo_root,
                step_height=cfg.step_height,
                step_front_x=cfg.step_front_x,
                step_depth=cfg.step_depth,
            )
            print(f"Generated step world: {world_path}")
            print(f"Step height: {cfg.step_height:.3f} m")

        trial_name = f"{args.sweep}_{i:02d}_{field_name}_{safe_value_name(float(value))}"

        result = run_trial(
            cfg,
            trial_name,
            raw_dir,
            args.sweep,
            float(value),
        )

        summary_rows.append(result.row)
        raw_paths.append(result.raw_path)

    summary_path = out_root / "summary.csv"

    fieldnames = list(summary_rows[0].keys())
    with summary_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    timeseries_plot = plot_timeseries(raw_paths, summary_rows, plot_dir, args.sweep)
    summary_plot = plot_summary(summary_rows, plot_dir, args.sweep)

    print("\n" + "=" * 88)
    print("SWEEP FINISHED")
    print("=" * 88)
    print(f"summary csv:      {summary_path}")
    print(f"raw logs:         {raw_dir}")
    print(f"timeseries plot:  {timeseries_plot}")
    print(f"summary plot:     {summary_plot}")
    print("\nMost important columns:")
    print("  vx_error_rmse, body_z_error_rmse, pitch_delta_max_abs_deg, roll_delta_max_abs_deg")

    if args.show:
        img = plt.imread(summary_plot)
        plt.figure(figsize=(10, 12))
        plt.imshow(img)
        plt.axis("off")
        plt.show()

def parse_args():
    parser = argparse.ArgumentParser(description="Flat-ground parameter sweep for Go2 convex MPC.")
    parser.add_argument(
        "--sweep",
        default="body_height",
        choices=list(PRESETS.keys()),
        help="Which single parameter to sweep. Default: body_height.",
    )
    parser.add_argument("--min", type=float, default=None, help="Minimum sweep value. Overrides preset.")
    parser.add_argument("--max", type=float, default=None, help="Maximum sweep value. Overrides preset.")
    parser.add_argument("--num", type=int, default=None, help="Number of values. Overrides preset.")

    parser.add_argument("--duration", type=float, default=7.0, help="Simulation duration per trial [s].")
    parser.add_argument("--base-velocity", type=float, default=0.5, help="Baseline x velocity [m/s].")
    parser.add_argument("--base-body-height", type=float, default=0.27, help="Baseline desired body height [m].")
    parser.add_argument("--base-swing-height", type=float, default=0.10, help="Baseline swing height [m].")
    parser.add_argument("--base-gait-hz", type=float, default=3.0, help="Baseline gait frequency [Hz].")
    parser.add_argument("--base-duty", type=float, default=0.60, help="Baseline gait duty factor.")
    parser.add_argument("--base-pitch-deg", type=float, default=0.0, help="Baseline pitch reference [deg].")

    parser.add_argument("--show", action="store_true", help="Show final summary plot at the end.")

    parser.add_argument("--viewer", action="store_true", help="Show MuJoCo viewer during simulation.")
    parser.add_argument("--viewer-fps", type=float, default=60.0, help="Viewer refresh rate.")

    return parser.parse_args()


def main():
    args = parse_args()
    run_sweep(args)


if __name__ == "__main__":
    main()
