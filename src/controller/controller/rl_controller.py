import os
import yaml
import time
import rclpy
from rclpy.node import Node
from threading import Lock
import torch
import numpy as np
from pathlib import Path

from ament_index_python.packages import get_package_share_directory

from robot_interfaces.msg import RobotState
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Twist

CONTROL_FREQUENCY = 100

class RLControllerNode(Node):
    def __init__(self):
        super().__init__('rl_controller_node')

        try:
            controller_dir = get_package_share_directory('controller')
        except:
            self.get_logger().error("❌ Package 'controller' not found!")
            return

        # config yaml
        config_path = os.path.join(controller_dir, 'config', 'go2.yaml')
        self.config = self.load_config(config_path)

        # policy path
        policy_relative = self.config.get('policy_path', 'policies/kp_kd_random_policy.pt')
        policy_path = os.path.join(controller_dir, policy_relative)
        self.policy = None

        if not os.path.exists(policy_path):
            self.get_logger().error(f"❌ Policy file not found: {policy_path}")
            return

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.policy_loaded = False

        self.get_logger().info(f"Using device: {self.device}")

        self.load_policy(policy_path)

        self.q = None
        self.dq = None
        self.imu_quat = None
        self.imu_gyro = None
        self.state_lock = Lock()

        num_obs = self.config.get('num_obs', 270)
        self.obs = np.zeros(num_obs, dtype=np.float32)
        self.cur_obs = np.zeros(45, dtype=np.float32)
        self.action = np.zeros(12, dtype=np.float32)

        self.Kp = np.array([100.0] * 12, dtype=np.float32)   # Proporzionale
        self.Kd = np.array([10.0] * 12, dtype=np.float32)    # Derivativo
        self.torque_limit = 100.0  # Safety limit
        
        self.sequence = [3, 4, 5, 0, 1, 2, 9, 10, 11, 6, 7, 8]

        # subscription for robot state (published by simulation/real robot interface)
        self.state_sub = self.create_subscription(RobotState, '/robot_state', self.state_callback, 10)

        self.torque_pub = self.create_publisher(Float64MultiArray, '/joint_torques', 10)

        self.cmd_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)

        self.cmd = np.array([0.0, 0.0, 0.0], dtype=np.float32)

        timer_period = 1.0/ CONTROL_FREQUENCY 
        self.create_timer(timer_period, self.control_step)

        self.step_counter = 0

        self.get_logger().info("RL Controller Node initialized.")

    def load_config(self, config_path: str) -> dict:
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            self.get_logger().info(f"✅ Config loaded from: {config_path}")
            return config
        except Exception as e:
            self.get_logger().error(f"❌ Failed to load config: {e}")
            # Default values se il file non esiste
            return {
                'default_angles': np.zeros(12, dtype=np.float32),
                'dof_pos_scale': 1.0,
                'dof_vel_scale': 1.0,
                'ang_vel_scale': 1.0,
                'cmd_scale': 1.0,
                'action_scale': 1.0,
            }

    def load_policy(self, policy_path: str) -> bool:
        try:
            self.policy = torch.jit.load(policy_path, map_location=self.device)
            self.policy.eval()
            self.get_logger().info("✅ Policy loaded (JIT)")
            return True
        except Exception as e:
            self.get_logger().warn(f"JIT load failed: {e}")
            
            try:
                self.policy = torch.load(policy_path, map_location=self.device)
                self.policy.eval()
                self.get_logger().info("✅ Policy loaded (torch.load)")
                return True
            except Exception as e2:
                self.get_logger().error(f"❌ Failed to load policy: {e2}")
                return False

    def state_callback(self, msg: RobotState):
        with self.state_lock:
            self.q = np.array(msg.q, dtype=np.float32)
            self.dq = np.array(msg.dq, dtype=np.float32)

            self.imu_quat = np.array(msg.imu_quat, dtype=np.float32)
            self.imu_gyro = np.array(msg.imu_gyro, dtype=np.float32)
        
    def control_step(self):
        if self.policy is None:
            return

        with self.state_lock:
            if self.q is None or self.dq is None:
                return
            q = self.q.copy()
            dq = self.dq.copy()
            imu_quat = self.imu_quat.copy() if self.imu_quat is not None else None
            imu_gyro = self.imu_gyro.copy() if self.imu_gyro is not None else None
        
        self._create_cur_obs(q, dq, imu_quat, imu_gyro)

        self.obs = np.concatenate((self.obs[45:], self.cur_obs[:45]))
        self.obs = np.clip(self.obs, -100, 100)

        try:
            # Pytorch tensor conversion
            obs_tensor = torch.from_numpy(self.obs).unsqueeze(0)
                
            # 12 torque array NumPy
            action = self.policy(obs_tensor).detach().numpy().squeeze()
            action = np.clip(action, -1.0, 1.0)
            self.action = action.copy()

            default_angles = np.array(self.config.get('default_angles', np.zeros(12)))
            action_scale = self.config.get('action_scale', 0.25)
            target_dof_pos = default_angles + action * action_scale
            
            # ===== STEP 4: PID CONTROLLER =====
            # target_pos → torque
            torque = self._compute_pid_torque(
                target_pos=target_dof_pos,
                actual_pos=q[7:19],    # 12 giunti
                actual_vel=dq[6:18]    # 12 velocità
            )

            torque_reordered = torque[self.sequence]

            # Publish torques
            msg = Float64MultiArray()
            msg.data = torque_reordered.astype(np.float32).tolist()
            self.torque_pub.publish(msg)

            self.step_counter += 1

            if self.step_counter % 100 == 0:
                self.get_logger().info(
                    f"Step {self.step_counter} | "
                    f"cmd: vx={self.cmd[0]:.2f} vy={self.cmd[1]:.2f} wz={self.cmd[2]:.2f} | "
                    f"torque: min={torque.min():.3f}, max={torque.max():.3f} | "
                    f"action: min={self.action.min():.3f}, max={self.action.max():.3f}"
                )
        except Exception as e:
            self.get_logger().error(f"Error during inference: {e}")

    def _compute_pid_torque(self, target_pos: np.ndarray, 
                            actual_pos: np.ndarray, 
                            actual_vel: np.ndarray) -> np.ndarray:
        # Errore posizione
        error_pos = target_pos - actual_pos
        
        # Errore velocità (target_vel = 0)
        error_vel = -actual_vel
        
        # PID
        torque = self.Kp * error_pos + self.Kd * error_vel
        
        # Clipping per sicurezza
        torque = np.clip(torque, -self.torque_limit, self.torque_limit)
        
        return torque.astype(np.float32)
                        
    def _create_cur_obs(self, q: np.ndarray, dq: np.ndarray,
                        imu_quat: np.ndarray = None,
                        imu_gyro: np.ndarray = None):

        qj = q[7:19]
        dqj = dq[6:18]

        default_angles = np.array(self.config.get('default_angles', np.zeros(12)))
        dof_pos_scale = self.config.get('dof_pos_scale', 1.0)
        dof_vel_scale = self.config.get('dof_vel_scale', 0.05)
        
        qj_obs = (qj - default_angles) * dof_pos_scale
        dqj_obs = dqj * dof_vel_scale
        
        gravity_orientation = np.zeros(3)

        if imu_quat is not None:
            gravity_orientation = self._get_gravity_orientation(imu_quat)
        
        ang_vel = np.zeros(3)
        if imu_gyro is not None:
            ang_vel_scale = self.config.get('ang_vel_scale', 0.3)
            ang_vel = imu_gyro * ang_vel_scale
        
        cmd = self.cmd.copy()
        cmd_scale = self.config.get('cmd_scale', [1.0, 1.0, 1.0])
        if isinstance(cmd_scale, list):
            cmd_scale = np.array(cmd_scale)

        cmd = cmd * cmd_scale
        
        # Assembla i 45 elementi (come nel file originale)
        self.cur_obs[:3] = cmd              # [0:3]
        self.cur_obs[3:6] = gravity_orientation  # [3:6]
        self.cur_obs[6:9] = ang_vel         # [6:9]
        self.cur_obs[9:21] = qj_obs         # [9:21]
        self.cur_obs[21:33] = dqj_obs       # [21:33]
        self.cur_obs[33:45] = self.action

    def cmd_callback(self, msg: Twist):
        with self.state_lock:
            self.cmd = np.array([msg.linear.x, msg.linear.y, msg.angular.z], dtype=np.float32)
            self.get_logger().info(
                f"Comando ricevuto: vx={msg.linear.x:.2f}, vy={msg.linear.y:.2f}, wz={msg.angular.z:.2f}"
            )
    @staticmethod
    def _get_gravity_orientation(quaternion: np.ndarray) -> np.ndarray:
        qw = quaternion[0]
        qx = quaternion[1]
        qy = quaternion[2]
        qz = quaternion[3]
        
        gravity_orientation = np.zeros(3, dtype=np.float32)
        
        gravity_orientation[0] = 2 * (-qz * qx + qw * qy)
        gravity_orientation[1] = -2 * (qz * qy + qw * qx)
        gravity_orientation[2] = 1 - 2 * (qw * qw + qz * qz)
        
        return gravity_orientation




def main(args=None):
    rclpy.init(args=args)
    node = RLControllerNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
            
if __name__ == '__main__':
    main()