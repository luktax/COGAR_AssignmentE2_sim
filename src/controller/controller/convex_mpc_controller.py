import time
from threading import Lock

import numpy as np
import rclpy
from geometry_msgs.msg import Twist
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

from robot_interfaces.msg import RobotState
from robot_interfaces.srv import SetBodyHeight, UpdateGaitParams, UpdateSingleParam

from convex_mpc.centroidal_mpc import CentroidalMPC
from convex_mpc.com_trajectory import ComTraj
from convex_mpc.gait import Gait
from convex_mpc.go2_robot_data import PinGo2Model
from convex_mpc.leg_controller import LegController

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

SIM_REALTIME_FACTOR = 0.2

class MPCControllerNode(Node):
    def __init__(self):
        super().__init__('mpc_controller_node')
        self.get_logger().info("MPC Controller Node started.")

        self.state_lock = Lock()
        self.mpc_lock = Lock()
        self.state_age_max_s = 0.1

        # PUBLISHERS/SUBSCRIBERS
        self.pub = self.create_publisher(Float64MultiArray, '/joint_torques', 10)
        self.sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        
        # subscription for robot state (published by simulation/real robot interface)
        self.state_cb = MutuallyExclusiveCallbackGroup()
        self.mpc_cb = MutuallyExclusiveCallbackGroup()

        self.state_sub = self.create_subscription(RobotState, '/robot_state', self.state_callback, 10, callback_group=self.state_cb)

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
        self.height_swing = 0
        self.phase_offset = np.array([0.5, 0.0, 0.0, 0.5]).reshape(4)
        self.gait_hz = 1.5 # 3.0
        self.gait_duty = 0.6 # 0.6

        self.gait_t = 1.0 / self.gait_hz
        self.mpc_dt = self.gait_t / 16.0
        self.mpc_timer_period = self.mpc_dt / SIM_REALTIME_FACTOR

        self.ctrl_hz = 100.0
        self.ctrl_dt = 1.0 / self.ctrl_hz

        # TIMER (ONE FAST - ONE SLOW)
        self.mpc_timer = self.create_timer(self.mpc_timer_period, self.mpc_loop, callback_group=self.mpc_cb)

        self.mpc_update_interval = max(1, int(self.ctrl_hz * self.mpc_dt))

        # stair parameters for pitch reference
        self.stair_height = 0.0
        self.stair_depth = 0.50
        self.pitch_ref = self.compute_pitch(self.stair_height, self.stair_depth)

        # Initialize robot model, gait, trajectory generator, MPC, and leg controller
        self.go2 = PinGo2Model() # FAST loop
        self.go2_mpc = PinGo2Model() # MPC loop

        self.gait = Gait(self.gait_hz, self.gait_duty, self.height_swing, self.phase_offset)
        self.traj = ComTraj(self.go2_mpc)

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
        self._last_loop_wall = 0
        self._loop_dt_log = []
        self.last_sim_time = 0

        #
        self.last_grf = None
        self.last_des = None
        self.last_contact = None

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
        self.mpc_timer_period = self.mpc_dt / SIM_REALTIME_FACTOR

        self.mpc_timer.cancel()
        self.mpc_timer = self.create_timer(self.mpc_timer_period, self.mpc_loop, callback_group=self.mpc_cb)

        self.gait = Gait(self.gait_hz, self.gait_duty, self.height_swing, self.phase_offset)
        self.mpc_needs_reset = True

    # ========= CMD_VEL CALLBACK ===========
    def cmd_vel_callback(self, msg):
        self.x_vel_des = msg.linear.x
        self.y_vel_des = msg.linear.y
        self.yaw_rate_des = msg.angular.z
        if self.debug_counter % 100 == 0:  # Print every 100 timer callbacks
            self.get_logger().info(f"Received cmd_vel: linear_x={self.x_vel_des}, linear_y={self.y_vel_des}, angular_z={self.yaw_rate_des}")

    def mpc_loop(self):
        wall = self.get_clock().now().nanoseconds*1e-9

        t0 = time.thread_time()
        with self.state_lock:
            if self.q is None or self.dq is None:
                return
            q = self.q.copy()
            dq = self.dq.copy()
            t = self.last_time
        
        #self.get_logger().info(
        #    f"[MPC START]"
        #    f" sim_time={t:.4f}"
        #    f" wall={wall:.4f}"
        #)

        # reset logic
        if self.mpc_needs_reset:
            self.mpc_initialized = False
            self.mpc_needs_reset = False
            return
        
        self.go2_mpc.update_model(q, dq)
        t1 = time.thread_time()

        # init MPC
        if not self.mpc_initialized:
            self.traj.generate_traj(self.go2_mpc, self.gait, t, self.x_vel_des, self.y_vel_des, self.z_pos_des, self.yaw_rate_des, self.pitch_ref, self.mpc_dt)
            self.mpc = CentroidalMPC(self.go2_mpc, self.traj)
            self.mpc_initialized = True
            return
        
        # trajectory update
        self.traj.generate_traj(self.go2_mpc, self.gait, t, self.x_vel_des, self.y_vel_des, self.z_pos_des, self.yaw_rate_des, self.pitch_ref, self.mpc_dt)
        
        t2 = time.thread_time()

        # solve MPC
        sol = self.mpc.solve_QP(self.go2_mpc, self.traj, False)
        t3 = time.thread_time()

        if sol is None:
            return

        w = sol["x"].full().flatten()
        N = self.traj.N

        grf0 = w[12*N:12*N+12].copy()

        #print(f"model={(t1-t0)*1000:.2f} "f"traj={(t2-t1)*1000:.2f} "f"qp={(t3-t2)*1000:.2f}")
        #self.get_logger().info(
        #    f"[MPC] "
        #    f"update={self.mpc.update_time:.2f} ms "
        #    f"solve={self.mpc.solve_time:.2f} ms "
        #    f"total={self.mpc.update_time+self.mpc.solve_time:.2f} ms"
        #)

        #self.get_logger().info(
        #    f"[MPC SOLVED]"
        #    f" sim_time={t:.4f}"
        #    f" Fx_FL={grf0[0]:.2f}"
        #    f" Fy_FL={grf0[1]:.2f}"
        #    f" Fz_FL={grf0[2]:.2f}"
        #)

        des = (
            self.go2_mpc.x_vel_des_world,
            self.go2_mpc.y_vel_des_world,
            self.go2_mpc.x_pos_des_world,
            self.go2_mpc.y_pos_des_world,
            self.go2_mpc.yaw_rate_des_world
        )

        with self.mpc_lock:
            self.last_mpc_solution = sol
            self.last_grf = grf0
            self.last_des = des

    def state_callback(self, msg):
        dt = msg.time - self.last_sim_time
        self.last_sim_time = msg.time

        #print(f"sim dt = {dt*1000:.2f} ms")

        with self.state_lock:
            self.q = np.array(msg.q)
            self.dq = np.array(msg.dq)
            self.last_time = msg.time
            self.last_state_time_wall = self.get_clock().now().nanoseconds * 1e-9
            #self.get_logger().info(
            #    f"[CTRL RX STATE]"
            #    f" sim_time={msg.time:.4f}"
            #    f" wall={self.get_clock().now().nanoseconds*1e-9:.4f}"
            #    f" qz={self.q[2]:.3f}"
            #    f" pitch={self.q[4]:.3f}"
            #)
            #self.get_logger().info(f"Received state: q ({len(self.q)}), dq ({len(self.dq)})")

            if self.q is None or self.dq is None:
                return

            q = self.q.copy()
            dq = self.dq.copy()
            t = self.last_time

        t0 = time.thread_time()

        self.go2.update_model(q, dq)

        t1 = time.thread_time()

        with self.mpc_lock:
            sol = self.last_mpc_solution
            if self.last_grf is None:
                return
            grf = self.last_grf.copy()
            des = self.last_des

            #self.get_logger().info(
            #    f"[FAST LOOP]"
            #    f" sim_time={t:.4f}"
            #    f" Fz_FL={grf[2]:.2f}"
            #)
        
        if sol is None:
            return
        
        self.go2.x_vel_des_world = des[0]
        self.go2.y_vel_des_world = des[1]
        self.go2.x_pos_des_world = des[2]
        self.go2.y_pos_des_world = des[3]
        self.go2.yaw_rate_des_world = des[4]

        FL = self.leg_controller.compute_leg_torque("FL", self.go2, self.gait, grf[0:3], t)
        FR = self.leg_controller.compute_leg_torque("FR", self.go2, self.gait, grf[3:6], t)
        RL = self.leg_controller.compute_leg_torque("RL", self.go2, self.gait, grf[6:9], t)
        RR = self.leg_controller.compute_leg_torque("RR", self.go2, self.gait, grf[9:12], t)

        t2 = time.thread_time()

        tau = np.zeros(12)
        tau[0:3] = FL.tau
        tau[3:6] = FR.tau
        tau[6:9] = RL.tau
        tau[9:12] = RR.tau

        self.last_tau = np.clip(tau, -TAU_LIM, TAU_LIM)

        msg = Float64MultiArray()
        msg.data = self.last_tau.tolist()
        self.pub.publish(msg)

        t3 = time.thread_time()
        #self.get_logger().info(
        #    f"[CTRL TX TORQUE]"
        #    f" sim_time={t:.4f}"
        #    f" tau0={self.last_tau[0]:.2f}"
        #    f" tau1={self.last_tau[1]:.2f}"
        #    f" tau2={self.last_tau[2]:.2f}"
        #)

        wall = self.get_clock().now().nanoseconds*1e-9
        age = wall - self.last_state_time_wall

        #self.get_logger().info(
        #    f"[STATE AGE]"
        #    f" age={age*1000:.2f} ms"
        #    f"model={(t1-t0)*1000:.2f} "
        #    f"legs={(t2-t1)*1000:.2f} "
        #    f"pub={(t3-t2)*1000:.2f}"
        #)
        self.debug_counter += 1


    def compute_pitch(self, stair_height, stair_depth):
        pitch = -np.arctan(stair_height / stair_depth)
        pitch = np.clip(pitch, -np.radians(30), 0.0)
        return pitch

def main():
    rclpy.init()
    node = MPCControllerNode()
    exe = MultiThreadedExecutor(num_threads=3)
    exe.add_node(node)
    exe.spin()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()