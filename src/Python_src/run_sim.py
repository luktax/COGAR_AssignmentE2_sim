import time
import mujoco as mj
import mujoco.viewer

from convex_mpc.go2_robot_data import PinGo2Model
from convex_mpc.mujoco_model import MuJoCo_GO2_Model

# --------------------------------------------------------------------------------
# Parameters
# --------------------------------------------------------------------------------

# Simulation Setting
INITIAL_X_POS = 0
INITIAL_Y_POS = 0
INITIAL_Z_POS = 0.27
#RUN_SIM_LENGTH_S = 10.0

SIM_HZ = 1000
SIM_DT = 1.0 / SIM_HZ

# --------------------------------------------------------------------------------
# Simulation Initialization
# --------------------------------------------------------------------------------
def main():
    print("Initializing MuJoCo model...")

    # Pinocchio model
    go2 = PinGo2Model()

    # MuJoCo model
    mujoco_go2 = MuJoCo_GO2_Model()

    # ----------------------------------------
    # Initial robot configuration
    # ----------------------------------------

    q_init = go2.current_config.get_q()

    q_init[0] = INITIAL_X_POS
    q_init[1] = INITIAL_Y_POS
    q_init[2] = INITIAL_Z_POS

    mujoco_go2.update_with_q_pin(q_init)

    # ----------------------------------------
    # Physics timestep
    # ----------------------------------------
    mujoco_go2.model.opt.timestep = SIM_DT

    print("Simulation started.")

    # ----------------------------------------
    # Viewer
    # ----------------------------------------

    with mujoco.viewer.launch_passive(
        mujoco_go2.model,
        mujoco_go2.data
    ) as viewer:

        viewer.cam.distance = 2.0
        viewer.cam.elevation = -20
        viewer.cam.azimuth = 90

        while viewer.is_running():

            # Sync Pinocchio model
            mujoco_go2.update_pin_with_mujoco(go2)

            # Physics step
            mj.mj_step(mujoco_go2.model, mujoco_go2.data)

            # Render
            viewer.sync()

            time.sleep(SIM_DT)
        
    print("Simulation ended.")

if __name__ == "__main__":
    main()
