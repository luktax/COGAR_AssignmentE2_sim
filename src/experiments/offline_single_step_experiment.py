"""
Offline single-step experiment for Unitree Go2 + convex MPC.

Purpose
-------
This script reuses the original offline demo structure, but loads the existing
MuJoCo_GO2_Model / stair_world.xml setup and tests a slow, quasi-static gait
against a single front step.

Important
---------
This is intentionally NOT a ROS real-time controller. The simulation advances
only after the controller has computed the torque command. Use it as an offline
benchmark to compare stair-climbing parameters such as:
    - body height
    - body pitch
    - swing height
    - gait frequency
    - duty factor
    - forward velocity

Before running, replace:
    models/MJCF/go2/stair_world.xml
with the provided `stair_world_single_step_front.xml` content, or copy that file
to the same path/name expected by convex_mpc.mujoco_model.MuJoCo_GO2_Model.
"""

import csv
import math
import time
from dataclasses import dataclass, field
from pathlib import Path

import mujoco as mj
import numpy as np

from convex_mpc.go2_robot_data import PinGo2Model
from convex_mpc.mujoco_model import MuJoCo_GO2_Model
from convex_mpc.com_trajectory import ComTraj
from convex_mpc.centroidal_mpc import CentroidalMPC
from convex_mpc.leg_controller import LegController
from convex_mpc.gait import Gait

# --------------------------------------------------------------------------------
# Experiment parameters
# --------------------------------------------------------------------------------

@dataclass
class ExperimentConfig:
    # Simulation
    run_sim_length_s: float = 7.0
    sim_hz: int = 1000
    ctrl_hz: int = 200
    render_hz: float = 120.0
    replay_realtime_factor: float = 0.5
    enable_plots: bool = False
    enable_replay: bool = True

    # Initial pose. The single step is placed in front along +x.
    initial_x: float = 0.0
    initial_y: float = 0.0
    initial_z: float = 0.27

    # Simple single-step geometry, used only to compute references and metrics.
    # The actual collision geometry is in stair_world.xml.
    step_front_x: float = 0.55
    step_back_x: float = 1.75
    step_height: float = 0.15
    nominal_step_depth: float = 0.50

    # Locomotion command: start conservative.
    x_vel_des: float = 0.3
    y_vel_des: float = 0.0
    yaw_rate_des: float = 0.0
    z_pos_des: float = 0.32

    # Stair pitch reference. 0.0 = level body, 1.0 = full stair slope.
    pitch_alpha: float = 0.0

    # Crawl-like gait. With duty 0.80 and phase offsets spaced by 0.25,
    # ideally only one leg is in swing at a time.
    gait_hz: float = 3.0
    gait_duty: float = 0.60
    height_swing: float = 0.20
    phase_offset: tuple = (0.5, 0.0, 0.0, 0.5)

    # Timing of the command schedule.
    stand_time_s: float = 1.0
    stop_time_s: float = 1.0

    # Safety / failure metrics.
    min_base_height_failure: float = 0.16
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
    def render_dt(self) -> float:
        return 1.0 / self.render_hz

    @property
    def slope_pitch(self) -> float:
        # Same sign convention used in your controller: uphill -> negative pitch.
        return -math.atan2(self.step_height, self.nominal_step_depth)

    @property
    def pitch_ref(self) -> float:
        return self.pitch_alpha * self.slope_pitch


@dataclass
class BodyCmdPhase:
    t_start: float
    t_end: float
    x_vel: float
    y_vel: float
    z_pos: float
    yaw_rate: float
    pitch: float


def build_cmd_schedule(cfg: ExperimentConfig):
    return [
        BodyCmdPhase(
            0.0,
            cfg.stand_time_s,
            0.0,
            0.0,
            cfg.z_pos_des,
            0.0,
            0.0,
        ),
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


def get_body_cmd(t: float, schedule):
    for phase in schedule:
        if phase.t_start <= t < phase.t_end:
            return (
                phase.x_vel,
                phase.y_vel,
                phase.z_pos,
                phase.yaw_rate,
                phase.pitch,
            )
    return 0.0, 0.0, 0.27, 0.0, 0.0


# --------------------------------------------------------------------------------
# Logs
# --------------------------------------------------------------------------------

@dataclass
class FootTraj:
    pos_des: np.ndarray
    pos_now: np.ndarray
    vel_des: np.ndarray
    vel_now: np.ndarray


@dataclass
class TrialMetrics:
    success: bool = False
    failure_reason: str = "none"
    final_base_x: float = 0.0
    max_abs_roll_deg: float = 0.0
    max_abs_pitch_deg: float = 0.0
    min_base_z: float = 999.0
    max_base_z: float = -999.0
    max_contact_force_n: float = 0.0
    elapsed_wall_s: float = 0.0


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


def get_contacts_and_max_force(mujoco_go2: MuJoCo_GO2_Model) -> float:
    """Return the maximum 3D contact force norm currently present in MuJoCo."""
    force6 = np.zeros(6, dtype=float)
    max_force = 0.0
    for i in range(mujoco_go2.data.ncon):
        mj.mj_contactForce(mujoco_go2.model, mujoco_go2.data, i, force6)
        max_force = max(max_force, float(np.linalg.norm(force6[:3])))
    return max_force


def update_metrics(metrics: TrialMetrics, go2: PinGo2Model, max_contact_force: float):
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


def detect_failure(cfg: ExperimentConfig, metrics: TrialMetrics) -> str | None:
    if metrics.min_base_z < cfg.min_base_height_failure:
        return "base_too_low"
    if math.radians(metrics.max_abs_roll_deg) > cfg.max_abs_roll_failure_rad:
        return "roll_limit"
    if math.radians(metrics.max_abs_pitch_deg) > cfg.max_abs_pitch_failure_rad:
        return "pitch_limit"
    if metrics.max_contact_force_n > cfg.max_contact_force_failure_n:
        return "contact_force_limit"
    return None


# --------------------------------------------------------------------------------
# Main trial
# --------------------------------------------------------------------------------

def run_trial(cfg: ExperimentConfig):
    if cfg.sim_hz % cfg.ctrl_hz != 0:
        raise ValueError(
            f"SIM_HZ ({cfg.sim_hz}) must be divisible by CTRL_HZ ({cfg.ctrl_hz})."
        )

    sim_steps = int(cfg.run_sim_length_s * cfg.sim_hz)
    ctrl_steps = int(cfg.run_sim_length_s * cfg.ctrl_hz)
    ctrl_decim = cfg.sim_hz // cfg.ctrl_hz

    gait_t = 1.0 / cfg.gait_hz
    mpc_dt = gait_t / 16.0
    mpc_hz = 1.0 / mpc_dt
    steps_per_mpc = max(1, int(cfg.ctrl_hz // mpc_hz))

    print("\n=== Offline single-step experiment ===")
    print(f"step_height       = {cfg.step_height:.3f} m")
    print(f"step_front_x      = {cfg.step_front_x:.3f} m")
    print(f"gait_hz           = {cfg.gait_hz:.2f} Hz")
    print(f"duty              = {cfg.gait_duty:.2f}")
    print(f"height_swing      = {cfg.height_swing:.3f} m")
    print(f"body_height       = {cfg.z_pos_des:.3f} m")
    print(f"pitch_ref         = {math.degrees(cfg.pitch_ref):.2f} deg")
    print(f"x_vel_des         = {cfg.x_vel_des:.3f} m/s")
    print(f"mpc_dt            = {mpc_dt*1000:.2f} ms")
    print(f"steps_per_mpc     = {steps_per_mpc}")

    schedule = build_cmd_schedule(cfg)

    # Storage arrays.
    x_vec_log = np.zeros((12, ctrl_steps))
    mpc_force_world = np.zeros((12, ctrl_steps))
    tau_raw = np.zeros((12, ctrl_steps))
    tau_cmd = np.zeros((12, ctrl_steps))
    time_log_ctrl_s = np.zeros(ctrl_steps)
    q_log_ctrl = np.zeros((ctrl_steps, 19))
    tau_log_ctrl_nm = np.zeros((ctrl_steps, 12))

    foot_traj = FootTraj(
        pos_des=np.zeros((12, ctrl_steps)),
        pos_now=np.zeros((12, ctrl_steps)),
        vel_des=np.zeros((12, ctrl_steps)),
        vel_now=np.zeros((12, ctrl_steps)),
    )

    mpc_update_time_ms = []
    mpc_solve_time_ms = []

    # Initialize models.
    go2 = PinGo2Model()
    mujoco_go2 = MuJoCo_GO2_Model()
    leg_controller = LegController()

    # Set physics dt.
    mujoco_go2.model.opt.timestep = cfg.sim_dt

    # Initial robot pose. Pinocchio quaternion convention: [qx, qy, qz, qw].
    q_init = go2.current_config.get_q().copy()
    q_init[0] = cfg.initial_x
    q_init[1] = cfg.initial_y
    q_init[2] = cfg.initial_z
    q_init[3:7] = np.array([0.0, 0.0, 0.0, 1.0])  # yaw = 0, facing +x
    mujoco_go2.update_with_q_pin(q_init)
    mujoco_go2.update_pin_with_mujoco(go2)

    gait = Gait(
        cfg.gait_hz,
        cfg.gait_duty,
        cfg.height_swing,
        np.asarray(cfg.phase_offset, dtype=float),
    )
    traj = ComTraj(go2)

    # Initialize MPC.
    traj.generate_traj(
        go2,
        gait,
        0.0,
        0.0,
        0.0,
        cfg.z_pos_des,
        0.0,
        0.0,
        time_step=mpc_dt,
    )
    mpc = CentroidalMPC(go2, traj)
    U_opt = np.zeros((12, traj.N), dtype=float)

    # Replay logs sampled at render Hz.
    time_log_render = []
    q_log_render = []
    tau_log_render = []
    next_render_t = 0.0

    metrics = TrialMetrics()
    ctrl_i = 0
    tau_hold = np.zeros(12, dtype=float)

    sim_start_wall = time.perf_counter()

    for k in range(sim_steps):
        time_now_s = float(mujoco_go2.data.time)

        if (k % ctrl_decim) == 0 and ctrl_i < ctrl_steps:
            x_vel, y_vel, z_pos, yaw_rate, pitch_ref = get_body_cmd(time_now_s, schedule)

            mujoco_go2.update_pin_with_mujoco(go2)

            x_vec_log[:, ctrl_i] = go2.compute_com_x_vec().reshape(-1)
            time_log_ctrl_s[ctrl_i] = time_now_s
            q_log_ctrl[ctrl_i, :] = mujoco_go2.data.qpos

            max_force = get_contacts_and_max_force(mujoco_go2)
            update_metrics(metrics, go2, max_force)

            failure = detect_failure(cfg, metrics)
            if failure is not None:
                metrics.success = False
                metrics.failure_reason = failure
                print(f"\n[FAIL] t={time_now_s:.3f}s reason={failure}")
                break

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
                    mpc_solve_time_ms.append(mpc.solve_time)
                    mpc_update_time_ms.append(mpc.update_time)

                    n_horizon = traj.N
                    w_opt = sol["x"].full().flatten()
                    U_opt = w_opt[12 * n_horizon:].reshape((12, n_horizon), order="F")
                else:
                    print(f"\n[WARN] MPC returned None at t={time_now_s:.3f}s; reusing previous U_opt")

            mpc_force_world[:, ctrl_i] = U_opt[:, 0]

            for leg in ("FL", "FR", "RL", "RR"):
                sl = LEG_SLICE[leg]
                out = leg_controller.compute_leg_torque(
                    leg,
                    go2,
                    gait,
                    mpc_force_world[sl, ctrl_i],
                    time_now_s,
                )
                tau_raw[sl, ctrl_i] = out.tau
                foot_traj.pos_des[sl, ctrl_i] = out.pos_des
                foot_traj.pos_now[sl, ctrl_i] = out.pos_now
                foot_traj.vel_des[sl, ctrl_i] = out.vel_des
                foot_traj.vel_now[sl, ctrl_i] = out.vel_now

            tau_cmd[:, ctrl_i] = np.clip(tau_raw[:, ctrl_i], -TAU_LIM, TAU_LIM)
            tau_hold = tau_cmd[:, ctrl_i].copy()
            tau_log_ctrl_nm[ctrl_i, :] = tau_hold

            ctrl_i += 1

        # Lockstep/offline dynamics: compute command first, then advance simulation.
        mj.mj_step1(mujoco_go2.model, mujoco_go2.data)
        mujoco_go2.set_joint_torque(tau_hold)
        mj.mj_step2(mujoco_go2.model, mujoco_go2.data)

        # Render-rate logging for replay.
        t_after = float(mujoco_go2.data.time)
        if t_after + 1e-12 >= next_render_t:
            time_log_render.append(t_after)
            q_log_render.append(mujoco_go2.data.qpos.copy())
            tau_log_render.append(tau_hold.copy())
            next_render_t += cfg.render_dt

    metrics.elapsed_wall_s = time.perf_counter() - sim_start_wall

    # Success criterion: base has moved clearly onto / beyond the single-step front edge
    # and the simulation did not trigger a failure condition.
    if metrics.failure_reason == "none":
        metrics.success = metrics.final_base_x > (cfg.step_front_x + 0.25)
        if not metrics.success:
            metrics.failure_reason = "not_enough_forward_progress"

    print("\n\nSimulation ended.")
    print(f"Elapsed wall time: {metrics.elapsed_wall_s:.3f}s")
    print(f"Control ticks:     {ctrl_i}/{ctrl_steps}")
    print(f"Success:           {metrics.success}")
    print(f"Failure reason:    {metrics.failure_reason}")
    print(f"Final base x:      {metrics.final_base_x:.3f} m")
    print(f"Max |roll|:        {metrics.max_abs_roll_deg:.2f} deg")
    print(f"Max |pitch|:       {metrics.max_abs_pitch_deg:.2f} deg")
    print(f"Min base z:        {metrics.min_base_z:.3f} m")
    print(f"Max contact force: {metrics.max_contact_force_n:.1f} N")

    # Save minimal CSV summary.
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    csv_path = results_dir / "single_step_trial.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "success",
                "failure_reason",
                "final_base_x",
                "max_abs_roll_deg",
                "max_abs_pitch_deg",
                "min_base_z",
                "max_base_z",
                "max_contact_force_n",
                "elapsed_wall_s",
                "gait_hz",
                "gait_duty",
                "height_swing",
                "z_pos_des",
                "pitch_alpha",
                "pitch_ref_deg",
                "x_vel_des",
                "step_height",
            ],
        )
        writer.writeheader()
        writer.writerow({
            "success": metrics.success,
            "failure_reason": metrics.failure_reason,
            "final_base_x": metrics.final_base_x,
            "max_abs_roll_deg": metrics.max_abs_roll_deg,
            "max_abs_pitch_deg": metrics.max_abs_pitch_deg,
            "min_base_z": metrics.min_base_z,
            "max_base_z": metrics.max_base_z,
            "max_contact_force_n": metrics.max_contact_force_n,
            "elapsed_wall_s": metrics.elapsed_wall_s,
            "gait_hz": cfg.gait_hz,
            "gait_duty": cfg.gait_duty,
            "height_swing": cfg.height_swing,
            "z_pos_des": cfg.z_pos_des,
            "pitch_alpha": cfg.pitch_alpha,
            "pitch_ref_deg": math.degrees(cfg.pitch_ref),
            "x_vel_des": cfg.x_vel_des,
            "step_height": cfg.step_height,
        })
    print(f"Saved summary: {csv_path}")

    # Plots and replay.
    if ctrl_i > 0 and cfg.enable_plots:
        t_vec = np.arange(ctrl_i) * cfg.ctrl_dt
        plot_swing_foot_traj(t_vec, foot_traj, False)
        plot_mpc_result(t_vec, mpc_force_world[:, :ctrl_i], tau_cmd[:, :ctrl_i], x_vec_log[:, :ctrl_i], block=False)
        plot_solve_time(mpc_solve_time_ms, mpc_update_time_ms, mpc_dt, mpc_hz, block=not cfg.enable_replay)

    if cfg.enable_replay and len(time_log_render) > 0:
        time_log_render_np = np.asarray(time_log_render, dtype=float)
        q_log_render_np = np.asarray(q_log_render, dtype=float)
        tau_log_render_np = np.asarray(tau_log_render, dtype=float)
        mujoco_go2.replay_simulation(
            time_log_render_np,
            q_log_render_np,
            tau_log_render_np,
            cfg.render_dt,
            cfg.replay_realtime_factor,
        )

    if cfg.enable_plots:
        hold_until_all_fig_closed()

    return metrics


if __name__ == "__main__":
    config = ExperimentConfig()
    run_trial(config)
