# COGAR Assignment E2 SIM - Go2 Convex MPC Simulation

This repository contains the simulation part of the COGAR Assignment E2 project: **Go2 Stair Ascent/Descent with Trunk Stabilization**.

The repository includes a MuJoCo simulation of the Unitree Go2 robot, a Convex MPC locomotion controller, ROS 2 interfaces for online simulation, and offline scripts used to run parameter sweeps and stair-climbing experiments.

## Repository content

Main folders:

- models: MuJoCo and URDF models of the Go2 robot and test environments.
- src/convex_mpc: Convex MPC, gait generation, trajectory generation, leg controller and robot model utilities.
- src/controller: ROS 2 controller node that receives robot state and publishes joint torques.
- src/simulation_py: ROS 2 MuJoCo simulation node.
- src/robot_interfaces: custom ROS 2 messages and services.
- src/experiments: offline simulation experiments and parameter sweeps.
- results: output folder for experiment logs and plots.

## Important note about the online simulation

The ROS 2 online simulation is included in this repository, but it is **not considered reliable for final experiments**.

The online architecture was designed as:

MuJoCo Simulation Node
    |
    | /robot_state
    v
MPC Controller Node
    |
    | /joint_torques
    v
MuJoCo Simulation Node


### Install Python dependencies:

pip3 install numpy==1.26.4 scipy matplotlib casadi mujoco pin torch pyyaml


## Run a single offline experiment

The single-step offline experiment runs one MuJoCo trial without ROS 2 online communication.

cd ~/COGAR_project

source /opt/ros/humble/setup.bash
source install/setup.bash

python3 src/experiments/offline_single_step_experiment.py


## Run systematic offline parameter sweeps

The main script for systematic experiments is:

src/experiments/flat_param_sweep.py

Available sweeps:

body_height
velocity
swing_height
gait_hz
duty
pitch
step_height

Example:
python3 src/experiments/flat_param_sweep.py --sweep body_height


use --viewer to see the simulation on MuJoCo during the experiments

use --show to see the plots at the end of the experiments



## Run the online ROS 2 simulation

### Terminal 1 - Start the MuJoCo simulation node
cd ~/COGAR_project

source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 run simulation_py simulation_node

### Terminal 2 - Start the MPC controller node
cd ~/COGAR_project

source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 run controller controller_node

### Terminal 3 - Send a velocity command
source /opt/ros/humble/setup.bash
source ~/COGAR_project/install/setup.bash

ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.20, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"

### Useful online controller services

Set body height:

ros2 service call /set_body_height robot_interfaces/srv/SetBodyHeight \
"{height: 0.31}"

Update all gait parameters:

ros2 service call /update_gait_params robot_interfaces/srv/UpdateGaitParams \
"{frequency_hz: 3.0, duty_cycle: 0.6, height_swing: 0.10, phase_offset: [0.5, 0.0, 0.0, 0.5]}"

Update one parameter:

ros2 service call /update_single_param robot_interfaces/srv/UpdateSingleParam \
"{param_name: 'gait_hz', value: 3.0}"
