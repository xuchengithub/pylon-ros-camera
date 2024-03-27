#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    
    # adapt if needed
    debug = False
    respawn = False

    default_config_file = os.path.join(
        get_package_share_directory('pylon_ros2_camera_wrapper'),
        'config',
        'ip_camera.yaml'
    )

    # launch configuration variables
    node_name = LaunchConfiguration('node_name')
    camera_id = LaunchConfiguration('camera_id')
    config_file = LaunchConfiguration('config_file')
    # launch arguments
    declare_node_name_cmd = DeclareLaunchArgument(
        'node_name',
        default_value='ip_auto_config',
        description='Name of node.'
    )
    declare_camera_id_cmd = DeclareLaunchArgument(
        'camera_id',
        default_value='IP_camera',
        description='Id of the camera. Used as node namespace.'
    )

    declare_config_file_cmd = DeclareLaunchArgument(
        'config_file',
        default_value=default_config_file,
        description='Camera parameters structured in a .yaml file.'
    )
    # see https://navigation.ros.org/tutorials/docs/get_backtrace.html
    if (debug == True):
        launch_prefix = ['xterm -e gdb -ex run --args']
    else:
        launch_prefix = ''


    # node
    ip_auto_config_node = Node(
        package='pylon_ros2_camera_component',
        namespace=camera_id,
        executable='ip_auto_config',
        name=node_name,
        output='screen',
        respawn=respawn,
        emulate_tty=True,
        prefix=launch_prefix,
        prefix=['xterm -e gdb -ex run --args'],
        parameters=[config_file]
    )

    # Define LaunchDescription variable and return it
    ld = LaunchDescription()
    
    ld.add_action(declare_node_name_cmd)
    ld.add_action(declare_camera_id_cmd)
    ld.add_action(declare_config_file_cmd)


    ld.add_action(ip_auto_config_node)

    return ld
