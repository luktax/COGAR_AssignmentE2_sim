import rclpy
from rclpy.node import Node
import numpy as np
from threading import Lock

from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Twist
from robot_interfaces.msg import RobotState
from robot_interfaces.srv import UpdateGaitParams, UpdateSingleParam, SetBodyHeight

import sys

from convex_mpc.go2_robot_data import PinGo2Model
from convex_mpc.com_trajectory import ComTraj
from convex_mpc.centroidal_mpc import CentroidalMPC
from convex_mpc.leg_controller import LegController
from convex_mpc.gait import Gait

# Go2 Joint Torque Limit
HIP_LIM = 23.7
ABD_LIM = 23.7
KNEE_LIM = 45.43
SAFETY = 0.9

TAU_LIM = SAFETY * np.array([
    HIP_LIM, ABD_LIM, KNEE_LIM,   # FL: hip, thigh, calf
    HIP_LIM, ABD_LIM, KNEE_LIM,   # FR
    HIP_LIM, ABD_LIM, KNEE_LIM,   # RL
    HIP_LIM, ABD_LIM, KNEE_LIM,   # RR
])

class MPCControllerNode(Node):
    def __init__(self):
        super().__init__('mpc_controller_node')
        self.get_logger().info("MPC Controller Node started.")

        self.state_lock = Lock()
        self.state_age_max_s = 0.1

        # PUBLISHERS/SUBSCRIBERS
        self.pub = self.create_publisher(Float64MultiArray, '/joint_torques', 10)
        self.sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        
        # subscription for robot state (published by simulation/real robot interface)
        self.state_sub = self.create_subscription(RobotState, '/robot_state', self.state_callback, 10)

        # SERVICES
        self.update_all_srv = self.create_service(UpdateGaitParams, '/update_gait_params', self.update_gait_params_callback)
        self.update_single_srv = self.create_service(UpdateSingleParam, '/update_single_param', self.update_single_param_callback)
        self.set_height_srv = self.create_service(SetBodyHeight, '/set_body_height', self.set_body_height_callback)

        # robot state (configuration and velocities)
        self.q = None
        self.dq = None
        self.last_time = 0.0
        self.last_state_time_wall = 0.0

        # variable settings
        self.height_swing = 0.1
        self.phase_offset = np.array([0.5, 0.0, 0.0, 0.5]).reshape(4)
        self.gait_hz = 3.0 #3.0
        self.gait_duty = 0.6 #0.6

        self.gait_t = 1.0 / self.gait_hz
        self.mpc_dt = self.gait_t / 16.0

        self.ctrl_hz = 100.0
        self.ctrl_dt = 1.0 / self.ctrl_hz
        self.timer = self.create_timer(self.ctrl_dt, self.control_loop_callback)

        self.mpc_update_interval = max(1, int(self.ctrl_hz * self.mpc_dt))

        # stair parameters for pitch reference
        self.stair_height = 0.10
        self.stair_depth = 0.50
        self.pitch_ref = self.compute_pitch(self.stair_height, self.stair_depth)

        # Initialize robot model, gait, trajectory generator, MPC, and leg controller
        self.go2 = PinGo2Model()
        self.gait = Gait(self.gait_hz, self.gait_duty, self.height_swing, self.phase_offset)
        self.traj = ComTraj(self.go2)
        self.mpc = None
        self.leg_controller = LegController()
        self.last_tau = np.zeros(12)

        # cmd initialization
        self.x_vel_des = 0.0
        self.y_vel_des = 0.0
        self.z_pos_des = 0.27
        self.yaw_rate_des = 0.0

        # MPC State
        self.mpc_initialized = False
        self.last_mpc_solution = None

        # RESET Flag
        self.mpc_needs_reset = False

        # Logging
        self.debug_counter = 0
        self.mpc_counter = 0
        self.state_latency_log = []

    #  ========= SERVICES CALLBACKS ==========

    def update_gait_params_callback(self, request, response):
        try:
            freq = request.frequency_hz if request.frequency_hz > 0 else None
            duty = request.duty_cycle if 0 < request.duty_cycle < 1 else None
            height = request.height_swing if request.height_swing >= 0 else None
            phase = list(request.phase_offset) if len(request.phase_offset) == 4 else None

            self.update_parameters(freq, duty, height, phase, None)
            self.get_logger().info("✅ Gait parameters updated!")

            response.success = True
            response.message = "Parameters updated successfully"

        except Exception as e:
            self.get_logger().error(f"Error updating parameters: {str(e)}")
            response.success = False
            response.message = str(e)

        return response

    def update_single_param_callback(self, request, response):
        try:
            param_name = request.param_name.lower()
            value = request.value

            if param_name == "gait_hz" or param_name == "frequency_hz":
                if value <= 0:
                    raise ValueError("frequency_hz should be > 0")
                self.update_parameters(value, None, None, None, None)
                msg = f"gait_hz updated {value:.2f} Hz"

            elif param_name == "gait_duty" or param_name == "duty_cycle":
                if not (0 < value <= 1):
                    raise ValueError("duty_cycle should be between 0 and 1")
                self.update_parameters(None, value, None, None, None)
                msg = f"gait_duty updated {value:.2f}"
            
            elif param_name == "height_swing":
                if value < 0:
                    raise ValueError("height_swing should be >= 0")
                self.update_parameters(None, None, value, None, None)
                msg = f"height_swing updated {value:.3f} m"
            
            elif param_name == "z_pos_des":
                if value <= 0:
                    raise ValueError("body height should be > 0")
                self.update_parameters(None, None, None, None, value)
                msg = f"body height updated {value:.3f} m"
            
            elif param_name == "stair_height":
                if value < 0:
                    raise ValueError("stair_height should be >= 0")
                self.stair_height = value
                self.pitch_ref = self.compute_pitch(self.stair_height, self.stair_depth)
                msg = f"Stair height updated to {value:.3f} m → pitch = {np.degrees(self.pitch_ref):.1f}°"

            elif param_name == "stair_depth":
                if value <= 0:
                    raise ValueError("stair_depth deve essere > 0")
                self.stair_depth = value
                # compute the pitch
                self.pitch_ref = self.compute_pitch(self.stair_height, self.stair_depth)
                msg = f"Stair depth updated to {value:.3f} m → pitch = {np.degrees(self.pitch_ref):.1f}°"

            else:
                raise ValueError(f"Unknown parameter: {param_name}")
            
            self.get_logger().info(f"✅ {msg}")
            response.success = True
            response.message = msg
        
        except Exception as e:
            self.get_logger().error(f"Error: {str(e)}")
            response.success = False
            response.message = str(e)
        
        return response

    def set_body_height_callback(self, request, response):
        try:
            height = request.height
            if height <= 0:
                raise ValueError("Body height should be > 0")
            
            self.z_pos_des = height
            self.get_logger().info(f"Body height updated {height:.3f} m")

            self.mpc_needs_reset = True
            
            response.success = True
            response.message = f"Body height updated {height:.3f} m"
        
        except Exception as e:
            self.get_logger().error(f"Error: {str(e)}")
            response.success = False
            response.message = str(e)
        
        return response

    def update_parameters(self, gait_hz, gait_duty, height_swing, phase_offset, z_pos_des):
        if gait_hz is not None:
            self.gait_hz = gait_hz
        if gait_duty is not None:
            self.gait_duty = gait_duty
        if height_swing is not None:
            self.height_swing = height_swing
        if phase_offset is not None:
            self.phase_offset = np.array(phase_offset)
        if z_pos_des is not None:
            self.z_pos_des = z_pos_des
        
        self.gait_t = 1.0 / self.gait_hz
        self.mpc_dt = self.gait_t / 16.0
        self.mpc_update_interval = max(1, int(self.ctrl_hz * self.mpc_dt))

        self.gait = Gait(self.gait_hz, self.gait_duty, self.height_swing, self.phase_offset)
        self.mpc_needs_reset = True

    # ========= CMD_VEL CALLBACK ===========
    def cmd_vel_callback(self, msg):
        self.x_vel_des = msg.linear.x
        self.y_vel_des = msg.linear.y
        self.yaw_rate_des = msg.angular.z
        if self.debug_counter % 100 == 0:  # Print every 100 timer callbacks
            self.get_logger().info(f"Received cmd_vel: linear_x={self.x_vel_des}, linear_y={self.y_vel_des}, angular_z={self.yaw_rate_des}")

    # ========= CONTROL LOOP ==========
    def control_loop_callback(self):
        with self.state_lock:
            if self.q is None or self.dq is None:
                return
            
            # check latency of state
            state_age = self.last_state_time_wall - self.get_clock().now().nanoseconds * 1e-9
            if abs(state_age) > self.state_age_max_s:
                if self.debug_counter % 50 == 0:
                        self.get_logger().warn(
                            f"State too old: {abs(state_age)*1000:.1f}ms (threshold: "
                            f"{self.state_age_max_s*1000:.1f}ms)"
                        )
                return
            # Get state when is not too old
            q_local = self.q.copy()
            dq_local = self.dq.copy()
            time_now = self.last_time

            if len(self.state_latency_log) >= 100:
                self.state_latency_log.pop(0)
            self.state_latency_log.append(abs(state_age))

        # Update robot model with current state
        self.go2.update_model(q_local, dq_local)

        # 
        if self.debug_counter % 100 == 0:  # Print every 100 timer callbacks
            x = self.go2.compute_com_x_vec()
            avg_latency = np.mean(self.state_latency_log) * 1000
            self.get_logger().info(f"COM = {x[0,0]:.3f}, {x[1,0]:.3f}, {x[2,0]:.3f} | State latency: {avg_latency:.1f}ms")

        # RESET if params changed
        if self.mpc_needs_reset:
            self.get_logger().info("🔄 Reinitializing MPC with new parameters...")
            self.mpc_initialized = False  # Forza reinizializzazione
            self.mpc_needs_reset = False
            return

        # Initialize MPC on the first callback after receiving state
        if not self.mpc_initialized:
            self.traj.generate_traj(self.go2, self.gait, time_now, self.x_vel_des, self.y_vel_des, self.z_pos_des, self.yaw_rate_des, self.pitch_ref, self.mpc_dt)
            self.mpc = CentroidalMPC(self.go2, self.traj)
            self.mpc_initialized = True
            self.get_logger().info(f"MPC initialized with horizon N={self.traj.N}.")
            return

        # Run MPC 
        if self.mpc_counter % self.mpc_update_interval == 0:
            self.traj.generate_traj(self.go2, self.gait, time_now, self.x_vel_des, self.y_vel_des, self.z_pos_des, self.yaw_rate_des,self.pitch_ref, self.mpc_dt)
            sol = self.mpc.solve_QP(self.go2, self.traj, False)
            if sol is not None:  
                #self.get_logger().info(f"MPC solved at time {time_now:.3f}s")
                self.last_mpc_solution = sol
            else:
                self.last_mpc_solution = None
                self.get_logger().warn(f"MPC failed to solve at time {time_now:.3f}s")

        # Compute leg torques from MPC solution
        if self.last_mpc_solution is not None:
            w = self.last_mpc_solution["x"].full().flatten()
            N = self.traj.N
            U = w[12*N:].reshape((12, N), order="F")

            grf = U[:, 0]  # Ground reaction force 
            grf_FL = grf[0:3]
            grf_FR = grf[3:6]
            grf_RL = grf[6:9]
            grf_RR = grf[9:12]

            FL = self.leg_controller.compute_leg_torque("FL", self.go2, self.gait, grf_FL, time_now)
            FR = self.leg_controller.compute_leg_torque("FR", self.go2, self.gait, grf_FR, time_now)
            RL = self.leg_controller.compute_leg_torque("RL", self.go2, self.gait, grf_RL, time_now)
            RR = self.leg_controller.compute_leg_torque("RR", self.go2, self.gait, grf_RR, time_now)

            tau = np.zeros(12)

            tau[0:3]  = FL.tau
            tau[3:6]  = FR.tau
            tau[6:9]  = RL.tau
            tau[9:12] = RR.tau

            self.last_tau = np.clip(tau, -TAU_LIM, TAU_LIM)

        #self.get_logger().info(f"Current q: {len(self.q)} dq: {len(self.dq)}")
        # Publish torques
        msg = Float64MultiArray()
        msg.data = self.last_tau.tolist()

        self.pub.publish(msg)

        self.debug_counter += 1
        self.mpc_counter += 1
        #self.get_logger().info(f"dt_state = {self.get_clock().now().nanoseconds*1e-9 - self.last_time:.4f}")


    def state_callback(self, msg):
        with self.state_lock:
            self.q = np.array(msg.q)
            self.dq = np.array(msg.dq)
            self.last_time = msg.time
            self.last_state_time_wall = self.get_clock().now().nanoseconds * 1e-9
            #self.get_logger().info(f"Received state: q ({len(self.q)}), dq ({len(self.dq)})")

    def compute_pitch(self, stair_height, stair_depth):
        pitch = -np.arctan(stair_height / stair_depth)
        pitch = np.clip(pitch, -np.radians(30), 0.0)
        return pitch

def main():
    rclpy.init()
    node = MPCControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()