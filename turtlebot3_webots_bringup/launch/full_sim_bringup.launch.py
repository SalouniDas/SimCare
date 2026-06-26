from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    turtlebot3_model = LaunchConfiguration('model', default='burger')

    # Paths to included launch files
    webots_launch = os.path.join(
        FindPackageShare('webots_ros2_turtlebot').find('webots_ros2_turtlebot'),
        'launch', 'robot_launch.py'
    )

    state_pub_launch = os.path.join(
        FindPackageShare('turtlebot3_bringup').find('turtlebot3_bringup'),
        'launch', 'turtlebot3_state_publisher.launch.py'
    )

    slam_launch = os.path.join(
        FindPackageShare('turtlebot3_cartographer').find('turtlebot3_cartographer'),
        'launch', 'cartographer.launch.py'
    )

    nav2_launch = os.path.join(
        FindPackageShare('turtlebot3_navigation2').find('turtlebot3_navigation2'),
        'launch', 'navigation2.launch.py'
    )

    return LaunchDescription([
        IncludeLaunchDescription(PythonLaunchDescriptionSource(webots_launch)),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(state_pub_launch)),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(slam_launch), launch_arguments={'use_sim_time': 'true'}.items()),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(nav2_launch), launch_arguments={'use_sim_time': 'true'}.items()),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', os.path.join(
                FindPackageShare('turtlebot3_navigation2').find('turtlebot3_navigation2'),
                'rviz', 'navigation2.rviz'
            )]
        )
    ])

