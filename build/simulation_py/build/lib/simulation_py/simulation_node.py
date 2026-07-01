import time
from threading import Lock, Thread

import mujoco as mj
import mujoco.viewer
import numpy as np
import rclpy
from rclpy.node import Node

from convex_mpc.mujoco_model import MuJoCo_GO2_Model
from robot_interfaces.msg import RobotState
from std_msgs.msg import Float64MultiArray

INITIAL_X_POS = 0
INITIAL_Y_POS = 0
INITIAL_Z_POS = 0.27

SIM_HZ = 1000
SIM_DT = 1.0 / SIM_HZ

STATE_PUB_HZ = 100
STATE_PUB_DT = 1.0 / STATE_PUB_HZ
SIM_STEPS_PER_PUB = SIM_HZ // STATE_PUB_HZ # 1000 / 100 = 10 steps
REALTIME_FACTOR = 0.2

BATCH_WALL_DT = STATE_PUB_DT / REALTIME_FACTOR

RENDER_HZ = 60
RENDER_DT = 1.0 / RENDER_HZ
USE_VIEWER = True
DEBUG_HZ = 1


class SimulationNode(Node):
    def __init__(self):
        super().__init__('simulation_node')
        self.get_logger().info(
            f"Loading GO2 simulation (viewer={'ON' if USE_VIEWER else 'OFF'})..."
        )

        # MuJoCo model
        self.mujoco_go2 = MuJoCo_GO2_Model()
        self.mujoco_go2.model.opt.timestep = SIM_DT

        # initial configuration
        self.default_angles = np.asarray(
            [
                -0.1, 0.8, -1.5,   # FL
                 0.1, 0.8, -1.5,   # FR
                -0.1, 1.0, -1.5,   # RL
                 0.1, 1.0, -1.5,   # RR
            ],
            dtype=float,
        )
        q_init = np.concatenate(
            (
                [INITIAL_X_POS, INITIAL_Y_POS, INITIAL_Z_POS],
                [0.0, 0.0, 0.0, 1.0],
                self.default_angles,
            )
        )

        self.mujoco_go2.update_with_q_pin(q_init)

        # Sensor data (IMU, GYRO)
        self.imu_quat_id = mj.mj_name2id(
            self.mujoco_go2.model, mj.mjtObj.mjOBJ_SENSOR, "imu_quat"
        )
        self.imu_gyro_id = mj.mj_name2id(
            self.mujoco_go2.model, mj.mjtObj.mjOBJ_SENSOR, "imu_gyro"
        )

        if self.imu_quat_id == -1:
            self.get_logger().error("❌ Sensor 'imu_quat' not found!")
        else:
            self.get_logger().info(f"✅ imu_quat sensor found at index {self.imu_quat_id}")

        if self.imu_gyro_id == -1:
            self.get_logger().error("❌ Sensor 'imu_gyro' not found!")
        else:
            self.get_logger().info(f"✅ imu_gyro sensor found at index {self.imu_gyro_id}")

        self.foot_geom_to_leg = {}
        for leg in ("FL", "FR", "RL", "RR"):
            geom_id = mj.mj_name2id(
                self.mujoco_go2.model, mj.mjtObj.mjOBJ_GEOM, leg
            )
            if geom_id >= 0:
                self.foot_geom_to_leg[geom_id] = leg

        # Initial torque cmd
        self.torque_cmd = np.zeros(12, dtype=float)
        self.controller_ready = False
        self.state_lock = Lock()

        # Gains for PD initial controller
        self.kp_hold = np.full(12, 20.0, dtype=float)
        self.kd_hold = np.full(12, 2.0, dtype=float)
        self.hold_torque_limit = 100.0

        # SUBSCRIBERS/PUBLISHERS
        self.create_subscription(Float64MultiArray, '/joint_torques', self.torque_callback, 10)
        self.state_pub = self.create_publisher(RobotState, '/robot_state', 10)

        # timing tracking
        self.sim_step_counter = 0
        self.pub_counter = 0
        self._last_stats_wall = time.perf_counter()
        self._last_stats_sim = float(self.mujoco_go2.data.time)
        self._step_cpu_acc = 0.0
        self._publish_cpu_acc = 0.0
        self._render_cpu_acc = 0.0
        self._stats_batches = 0

        self.ros_thread = Thread(target=rclpy.spin, args=(self,), daemon=True)
        self.ros_thread.start()

        self.get_logger().info(
            f"Simulation started: physics={SIM_HZ} Hz, state={STATE_PUB_HZ} Hz, "
            f"render={RENDER_HZ if USE_VIEWER else 0} Hz"
        )
        self.run_simulation()
        

    def get_contacts_and_forces(self):
        contacts = {leg: False for leg in ("FL", "FR", "RL", "RR")}
        forces = {leg: 0.0 for leg in ("FL", "FR", "RL", "RR")}
        force6 = np.zeros(6, dtype=float)

        for i in range(self.mujoco_go2.data.ncon):
            contact = self.mujoco_go2.data.contact[i]
            leg = self.foot_geom_to_leg.get(contact.geom1)
            if leg is None:
                leg = self.foot_geom_to_leg.get(contact.geom2)
            if leg is None:
                continue

            contacts[leg] = True
            force6.fill(0.0)
            mj.mj_contactForce(
                self.mujoco_go2.model, self.mujoco_go2.data, i, force6
            )
            forces[leg] += float(np.linalg.norm(force6[:3]))

        return contacts, forces
      
    
    def torque_callback(self, msg):
        if len(msg.data) != 12:
            self.get_logger().warning(
                f"Ignoring torque command with {len(msg.data)} elements"
            )
            return

        with self.state_lock:
            self.torque_cmd[:] = msg.data
            first_command = not self.controller_ready
            self.controller_ready = True

        if first_command:
            self.get_logger().info("Controller ready; applying commanded torques")

    def get_imu_quaternion(self) -> np.ndarray:
        if self.imu_quat_id < 0:
            return np.asarray([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
        return np.asarray(
            self.mujoco_go2.data.sensor(self.imu_quat_id).data,
            dtype=np.float32,
        ).copy()

    def get_imu_gyro(self) -> np.ndarray:
        if self.imu_gyro_id < 0:
            return np.zeros(3, dtype=np.float32)
        return np.asarray(
            self.mujoco_go2.data.sensor(self.imu_gyro_id).data,
            dtype=np.float32,
        ).copy()

    def _current_applied_torque(self) -> np.ndarray:
        with self.state_lock:
            if self.controller_ready:
                return self.torque_cmd.copy()

        q_joints = np.asarray(self.mujoco_go2.data.qpos[7:19])
        dq_joints = np.asarray(self.mujoco_go2.data.qvel[6:18])
        torque = self.kp_hold * (self.default_angles - q_joints)
        torque -= self.kd_hold * dq_joints
        return np.clip(
            torque, -self.hold_torque_limit, self.hold_torque_limit
        )

    def _get_pin_state_from_mujoco(self):
        q_mj = np.asarray(self.mujoco_go2.data.qpos, dtype=float)
        dq_mj = np.asarray(self.mujoco_go2.data.qvel, dtype=float)

        # MuJoCo quaternion: [qw, qx, qy, qz]
        qw, qx, qy, qz = q_mj[3:7]

        # Rotazione body -> world
        R_body_to_world = np.array([
            [
                1.0 - 2.0 * (qy * qy + qz * qz),
                2.0 * (qx * qy - qw * qz),
                2.0 * (qx * qz + qw * qy),
            ],
            [
                2.0 * (qx * qy + qw * qz),
                1.0 - 2.0 * (qx * qx + qz * qz),
                2.0 * (qy * qz - qw * qx),
            ],
            [
                2.0 * (qx * qz - qw * qy),
                2.0 * (qy * qz + qw * qx),
                1.0 - 2.0 * (qx * qx + qy * qy),
            ],
        ])

        # MuJoCo: velocità lineare della base in world
        # Pinocchio: velocità lineare del free-flyer in body
        v_world = dq_mj[0:3]
        v_body = R_body_to_world.T @ v_world

        # MuJoCo usa già la velocità angolare della base nel frame body
        omega_body = dq_mj[3:6]

        # Pinocchio quaternion: [qx, qy, qz, qw]
        q_pin = np.concatenate([
            q_mj[0:3],
            [qx, qy, qz, qw],
            q_mj[7:19],
        ])

        dq_pin = np.concatenate([
            v_body,
            omega_body,
            dq_mj[6:18],
        ])

        return q_pin, dq_pin

    def _publish_state(self) -> None:
        q, dq = self._get_pin_state_from_mujoco()

        msg = RobotState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.q = q.tolist()
        msg.dq = dq.tolist()
        msg.imu_quat = self.get_imu_quaternion().tolist()
        msg.imu_gyro = self.get_imu_gyro().tolist()
        msg.time = float(self.mujoco_go2.data.time)
        self.state_pub.publish(msg)
        self.pub_counter += 1

    def _log_stats(self) -> None:
        now = time.perf_counter()
        wall_dt = now - self._last_stats_wall
        if wall_dt < 1.0 / DEBUG_HZ:
            return

        sim_now = float(self.mujoco_go2.data.time)
        sim_dt = sim_now - self._last_stats_sim
        rtf = sim_dt / wall_dt if wall_dt > 0 else 0.0
        batches = max(self._stats_batches, 1)

        contacts, forces = self.get_contacts_and_forces()
        self.get_logger().info(
            f"[SIM PERF] rtf={rtf:.3f} "
            f"step_batch={1e3*self._step_cpu_acc/batches:.3f} ms "
            f"publish={1e3*self._publish_cpu_acc/batches:.3f} ms "
            f"render={1e3*self._render_cpu_acc/batches:.3f} ms "
            f"contacts={contacts} forces={forces}"
        )

        self._last_stats_wall = now
        self._last_stats_sim = sim_now
        self._step_cpu_acc = 0.0
        self._publish_cpu_acc = 0.0
        self._render_cpu_acc = 0.0
        self._stats_batches = 0

    def run_simulation(self):
        if USE_VIEWER:
            self.run_with_viewer()
        else:
            self.run_without_viewer()

    def run_with_viewer(self):
        with mujoco.viewer.launch_passive(
            self.mujoco_go2.model,
            self.mujoco_go2.data
        ) as viewer:
            viewer.cam.distance = 2.0
            viewer.cam.elevation = -20
            viewer.cam.azimuth = 90

            # Rendering options
            viewer.user_scn.flags[mj.mjtRndFlag.mjRND_SHADOW] = 0
            viewer.user_scn.flags[mj.mjtRndFlag.mjRND_REFLECTION] = 0
            viewer.user_scn.flags[mj.mjtRndFlag.mjRND_SKYBOX] = 0
            viewer.user_scn.flags[mj.mjtRndFlag.mjRND_FOG] = 0
            viewer.user_scn.flags[mj.mjtRndFlag.mjRND_HAZE] = 0
            #viewer.opt.flags[mj.mjtVisFlag.mjVIS_CONTACTPOINT] = False
            #viewer.opt.flags[mj.mjtVisFlag.mjVIS_CONTACTFORCE] = False

            self.get_logger().info("Viewer started.")
            
            self.simulation_loop(viewer)

    def run_without_viewer(self):
        self.get_logger().info("Running headless (NO viewer)")
        self.simulation_loop(None)

    def simulation_loop(self, viewer):
        next_batch_deadline = time.perf_counter() + BATCH_WALL_DT
        next_render_sim_time = float(self.mujoco_go2.data.time)

        while rclpy.ok() and (viewer is None or viewer.is_running()):
            torque = self._current_applied_torque()
            self.mujoco_go2.set_joint_torque(torque)

            t0 = time.perf_counter()
            for _ in range(SIM_STEPS_PER_PUB):
                mj.mj_step(self.mujoco_go2.model, self.mujoco_go2.data)
                self.sim_step_counter += 1
            self._step_cpu_acc += time.perf_counter() - t0

            t0 = time.perf_counter()
            self._publish_state()
            self._publish_cpu_acc += time.perf_counter() - t0

            sim_time = float(self.mujoco_go2.data.time)
            if viewer is not None and sim_time >= next_render_sim_time:
                t0 = time.perf_counter()
                viewer.sync()
                self._render_cpu_acc += time.perf_counter() - t0
                # Skip missed frames rather than trying to render them all.
                next_render_sim_time = sim_time + RENDER_DT

            self._stats_batches += 1
            self._log_stats()

            sleep_time = next_batch_deadline - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)
                next_batch_deadline += BATCH_WALL_DT
            else:
                # Preserve phase for small overruns, reset after a large stall.
                next_batch_deadline += BATCH_WALL_DT
                if sleep_time < -0.1:
                    next_batch_deadline = time.perf_counter() + BATCH_WALL_DT

def main(args=None):
    rclpy.init(args=args)
    node = SimulationNode()

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()