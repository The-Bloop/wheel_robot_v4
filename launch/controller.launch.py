import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    pkg_share = FindPackageShare(package='wheel_robot_v4').find("wheel_robot_v4")

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    sim_time_arg = DeclareLaunchArgument(
        name='use_sim_time',
        default_value="True",
        description='On/Off Simulation time'
    )

    robot_controllers = PathJoinSubstitution(
        [
            pkg_share,
            "config",
            "four_wheel_diff_drive.yaml",
        ]
    )

    # control_node = Node(
    #     package="controller_manager",
    #     executable="ros2_control_node",
    #     parameters=[robot_controllers],
    #     output="both",
    #     remappings=[
    #         ("~/robot_description", "/robot_description"),
    #         ("/robot_diff_drive_controller/cmd_vel", "/cmd_vel"),
    #         ("/robot_diff_drive_controller/odom", "/odom"),
    #     ],
    # )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"]
    )

    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["robot_diff_drive_controller", "--controller-manager", "/controller_manager"]
    )

    ld = LaunchDescription()

    # ld.add_action(control_node)
    ld.add_action(joint_state_broadcaster_spawner)
    ld.add_action(robot_controller_spawner)
    ld.add_action(sim_time_arg)


    return ld