from launch import LaunchDescription
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
    container = ComposableNodeContainer(
        name='go2_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[
            # Simulation Component
            ComposableNode(
                package='simulation_py',
                plugin='simulation_py.simulation_node::SimulationNode',
                name='simulation_node',
            ),
            # Controller Component
            ComposableNode(
                package='controller',
                plugin='controller.convex_mpc_controller::MPCControllerNode',
                name='controller_node',
            ),
        ],
        output='screen',
    )

    return LaunchDescription([container])