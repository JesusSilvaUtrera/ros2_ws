#!usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class ClosedLoopNode(Node):
    def __init__(self):
        super().__init__('closed_loop')
        self.get_logger().info("closed loop node started")
        #Creamos publisher y subscriber (el 10 es el queue_size), ademas de un timer para hacerlo periodico
        self.cmd_vel_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.pose_sub = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)

    #Siempre que recibamos un mensaje en el topic de la pose, enviamos un nuevo comando de velocidad
    def pose_callback(self, pose: Pose):
        self.get_logger().info("Pose actual: " + str(pose))
        cmd = Twist()
        if pose.x > 9.0 or pose.y > 9.0 or pose.x < 2.0 or pose.y < 2.0:
            cmd.linear.x = 1.5
            cmd.angular.z = 1.8
        else:
            cmd.linear.x = 4.0
            cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)

    node = ClosedLoopNode()
    rclpy.spin(node)

    rclpy.shutdown()