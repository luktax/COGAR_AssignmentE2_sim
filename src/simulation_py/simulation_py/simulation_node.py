import time
import rclpy
import numpy as np

from rclpy.node import Node
from threading import Lock

import mujoco as mj
import mujoco.viewer

from convex_mpc.go2_robot_data import PinGo2Model
from convex_mpc.mujoco_model import MuJoCo_GO2_Model

from std_msgs.msg import Float64MultiArray
from robot_interfaces.msg import RobotState

INITIAL_X_POS = 0
INITIAL_Y_POS = 0
INITIAL_Z_POS = 0.27

SIM_HZ = 1000
SIM_DT = 1.0 / SIM_HZ

STATE_PUB_HZ = 100
STATE_PUB_DT = 1.0 / STATE_PUB_HZ
SIM_STEPS_PER_PUB = int(SIM_HZ / STATE_PUB_HZ) # 1000 / 100 = 10 steps

USE_VIEWER = True

class SimulationNode(Node):
    def __init__(self):
        super().__init__('simulation_node')
        self.get_logger().info("Loading GO2 simulation (viewer={'ON' if USE_VIEWER else 'OFF'})...")

        # Pinocchio model
        self.go2 = PinGo2Model()

        # MuJoCo model
        self.mujoco_go2 = MuJoCo_GO2_Model()

        # Initial robot configuration
        q_init = self.go2.current_config.get_q()

        q_init[0] = INITIAL_X_POS
        q_init[1] = INITIAL_Y_POS
        q_init[2] = INITIAL_Z_POS

        self.default_angles = [-0.1, 0.8, -1.5,   # FL
                                0.1, 0.8, -1.5,   # FR
                                -0.1, 1.0, -1.5,  # RL
                                0.1, 1.0, -1.5    # RR
                                ]

        self.mujoco_go2.update_with_q_pin(q_init)
        self.mujoco_go2.model.opt.timestep = SIM_DT

        # Sensor data (IMU, GYRO)
        self.imu_quat_adr = mj.mj_name2id(
            self.mujoco_go2.model, 
            mj.mjtObj.mjOBJ_SENSOR, 
            "imu_quat"
        )
        self.imu_gyro_adr = mj.mj_name2id(
            self.mujoco_go2.model, 
            mj.mjtObj.mjOBJ_SENSOR, 
            "imu_gyro"
        )

        if self.imu_quat_adr == -1:
            self.get_logger().error("❌ Sensor 'imu_quat' not found!")
        else:
            self.get_logger().info(f"✅ imu_quat sensor found at index {self.imu_quat_adr}")

        if self.imu_gyro_adr == -1:
            self.get_logger().error("❌ Sensor 'imu_gyro' not found!")
        else:
            self.get_logger().info(f"✅ imu_gyro sensor found at index {self.imu_gyro_adr}")

        # Initial torque cmd
        self.torque_cmd = [0.0] * 12

        self.controller_ready = False
        self.torque_received_counter = 0
        self.ready_threshold = 1

        # SUBSCRIBERS/PUBLISHERS
        self.create_subscription(Float64MultiArray, '/joint_torques', self.torque_callback, 10)
        self.state_pub = self.create_publisher(RobotState, '/robot_state', 10)

        # timing tracking
        self.sim_step_counter = 0
        self.pub_counter = 0
        self.last_pub_time = 0.0

        # syncrhronization
        self.state_lock = Lock()

        self.get_logger().info("Simulation started.")
        #self.print_geom_names()
        self.run_simulation()
        

    def print_geom_names(self):
        print("\n===== GEOMS =====")

        for i in range(self.mujoco_go2.model.ngeom):

            name = mj.mj_id2name(
                self.mujoco_go2.model,
                mj.mjtObj.mjOBJ_GEOM,
                i
            )

            print(i, name)

    def debug_contacts(self):
        ncon = self.mujoco_go2.data.ncon

        print(f"\nContacts: {ncon}")

        for i in range(ncon):
            c = self.mujoco_go2.data.contact[i]

            geom1_name = mj.mj_id2name(self.mujoco_go2.model, mj.mjtObj.mjOBJ_GEOM, c.geom1)
            geom2_name = mj.mj_id2name(self.mujoco_go2.model, mj.mjtObj.mjOBJ_GEOM, c.geom2)
            
            force = np.zeros(6)

            mj.mj_contactForce(self.mujoco_go2.model, self.mujoco_go2.data, i, force)

            print(f"{i}: {geom1_name} <-> {geom2_name}"
                  f"Force = {force}")
            print(geom1_name, geom2_name, "dist = ", c.dist)

    def get_foot_contacts(self):
        contacts = {"FL": False,
                    "FR": False,
                    "RL": False,
                    "RR": False}

        for i in range(self.mujoco_go2.data.ncon):
            c = self.mujoco_go2.data.contact[i]

            geom1 = mj.mj_id2name(self.mujoco_go2.model, mj.mjtObj.mjOBJ_GEOM, c.geom1)
            geom2 = mj.mj_id2name(self.mujoco_go2.model, mj.mjtObj.mjOBJ_GEOM, c.geom2)

            pair = [geom1, geom2]

            force = np.zeros(6)

            mj.mj_contactForce(self.mujoco_go2.model, self.mujoco_go2.data, i, force)


            if "FL" in pair:
                contacts["FL"] = True

            if "FR" in pair:
                contacts["FR"] = True

            if "RL" in pair:
                contacts["RL"] = True

            if "RR" in pair:
                contacts["RR"] = True
            
        return contacts
    
    def get_contact_forces(self):
        forces = {"FL": 0.0,
                  "FR": 0.0,
                  "RL": 0.0,
                  "RR": 0.0}

        for i in range(self.mujoco_go2.data.ncon):
            c = self.mujoco_go2.data.contact[i]

            geom1 = mj.mj_id2name(self.mujoco_go2.model, mj.mjtObj.mjOBJ_GEOM, c.geom1)
            geom2 = mj.mj_id2name(self.mujoco_go2.model, mj.mjtObj.mjOBJ_GEOM, c.geom2)

            pair = [geom1, geom2]

            force = np.zeros(6)

            mj.mj_contactForce(self.mujoco_go2.model, self.mujoco_go2.data, i, force)

            f = np.linalg.norm(force[:3])

            if "FL" in pair:
                forces["FL"] += f

            if "FR" in pair:
                forces["FR"] += f

            if "RL" in pair:
                forces["RL"] += f

            if "RR" in pair:
                forces["RR"] += f

        return forces
      
    
    def torque_callback(self, msg):
        if len(msg.data) == 12:
            with self.state_lock:
                self.torque_cmd = list(msg.data)
        #print("received torque command:", self.torque_cmd)
                self.torque_received_counter += 1
                if self.torque_received_counter == self.ready_threshold:
                    self.controller_ready = True
                    self.get_logger().info("✅✅✅ CONTROLLER READY! Starting physics simulation")

    def get_imu_quaternion(self) -> np.ndarray:
        if self.imu_quat_adr == -1:
            return np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
        
        sensor_data = self.mujoco_go2.data.sensor(self.imu_quat_adr).data
        return np.array(sensor_data, dtype=np.float32)

    def get_imu_gyro(self) -> np.ndarray:
        if self.imu_gyro_adr == -1:
            return np.array([0.0, 0.0, 0.0], dtype=np.float32)
        
        # 3 value
        sensor_data = self.mujoco_go2.data.sensor(self.imu_gyro_adr).data
        return np.array(sensor_data, dtype=np.float32)

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
        last_sim_time = time.perf_counter()

        while True:
            import rclpy
            rclpy.spin_once(self, timeout_sec=0.0)

            with self.state_lock:
                torque_cmd = self.torque_cmd.copy()
                controller_ready = self.controller_ready
   

            Kp_hold = np.array([20.0] * 12, dtype=np.float32)
            Kd_hold = np.array([2.0] * 12, dtype=np.float32)
            torque_limit = 100.0


            if not controller_ready:
                q = self.go2.current_config.get_q()
                dq = self.go2.current_config.get_dq()
                
                q_joints = q[7:19]
                dq_joints = dq[6:18]
                error_pos = self.default_angles - q_joints
                error_vel = -dq_joints

                torque_hold = Kp_hold * error_pos + Kd_hold * error_vel
                torque_hold = np.clip(torque_hold, -torque_limit, torque_limit)

                self.mujoco_go2.set_joint_torque([0.0] * 12)
                #self.mujoco_go2.set_joint_torque(torque_hold)
            else:
                self.mujoco_go2.set_joint_torque(torque_cmd)

            mj.mj_step(self.mujoco_go2.model, self.mujoco_go2.data)

            self.sim_step_counter += 1

            # ===== PUBLISH STATE EVERY N STEPS =====
            if self.sim_step_counter % SIM_STEPS_PER_PUB == 0:
                # Update
                self.mujoco_go2.update_pin_with_mujoco(self.go2)
                
                # get robot configuration and velocities    
                q = self.go2.current_config.get_q()
                dq = self.go2.current_config.get_dq()

                #get sensor data
                imu_quat = self.get_imu_quaternion()
                imu_gyro = self.get_imu_gyro()

                # prepare Custom message ROBOT STATE 
                msg = RobotState()
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.q = q.tolist()
                msg.dq = dq.tolist()
                msg.imu_quat = imu_quat.tolist()
                msg.imu_gyro = imu_gyro.tolist()

                msg.time = float(self.mujoco_go2.data.time)

                # publish message
                self.state_pub.publish(msg)
                self.pub_counter += 1

                # get contacts
                contacts = self.get_foot_contacts()
                # get contact forces
                forces = self.get_contact_forces()

                # debug print
                if self.pub_counter % 50 == 0:
                    #self.debug_contacts()
                    self.get_logger().info(
                        #f"Published state #{self.pub_counter} at t={msg.time:.3f}s"
                        #f"IMU quat: #{msg.imu_quat} | IMU Gyro: #{msg.imu_gyro}"
                        f"Contacts: "
                        f"FL={contacts['FL']} "
                        f"FR={contacts['FR']} "
                        f"RL={contacts['RL']} "
                        f"RR={contacts['RR']} "
                        f"\nForces: "
                        f"FL={forces['FL']} "
                        f"FR={forces['FR']} "
                        f"RL={forces['RL']} "
                        f"RR={forces['RR']} "
                    )
            if viewer is not None:
                viewer.sync()

            now = time.perf_counter()
            time_until_next = SIM_DT - (now - last_sim_time)
            if time_until_next > 0:
                time.sleep(time_until_next)
                last_sim_time = time.perf_counter()
            else:
                last_sim_time = now
                #self.get_logger().warn( f"Simulation step behind: {-time_until_next*1000:.2f}ms late")

def main(args=None):
    rclpy.init(args=args)
    node = SimulationNode()

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()