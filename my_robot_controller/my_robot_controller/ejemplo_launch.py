# turtlesim/launch/multisim.launch.py
#Se puede usar Python, XML o YAML para escribir los archivos launch

from launch import LaunchDescription
import launch_ros.actions

def generate_launch_description():
    #Hay muchas opciones a la hora de desplegar un nodo en un archivo launch, como el tipo de output, el respawn...
    return LaunchDescription([
        launch_ros.actions.Node(
            namespace= "turtlesim1", package='turtlesim', executable='turtlesim_node', output='screen'),
        launch_ros.actions.Node(
            namespace= "turtlesim2", package='turtlesim', executable='turtlesim_node', output='screen'),
    ])