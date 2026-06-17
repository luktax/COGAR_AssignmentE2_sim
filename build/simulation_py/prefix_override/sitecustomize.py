import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/lukat/unitree_mujoco_ws/COGAR_project/install/simulation_py'
