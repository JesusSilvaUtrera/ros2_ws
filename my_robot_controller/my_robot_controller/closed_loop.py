#!usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
from functools import partial

class ClosedLoopNode(Node):
    def __init__(self):
        super().__init__('closed_loop')
        self.get_logger().info("closed loop node started")
        self.previous_x = 0
        #Creamos publisher y subscriber (el 10 es el queue_size), ademas de un timer para hacerlo periodico
        self.cmd_vel_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.pose_sub = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)

    #Siempre que recibamos un mensaje en el topic de la pose, enviamos un nuevo comando de velocidad
    def pose_callback(self, pose: Pose):
        #self.get_logger().info("Pose actual: " + str(pose))
        cmd = Twist()
        if pose.x > 9.0 or pose.y > 9.0 or pose.x < 2.0 or pose.y < 2.0:
            cmd.linear.x = 1.5
            cmd.angular.z = 1.8
        else:
            cmd.linear.x = 4.0
            cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd)

        #El uso de previous_x es para que el servicio no se llame todo el rato, sino que solo se llame cuando cambie de mitad y sea realmente necesario
        if pose.x > 5.5 and self.previous_x <= 5.5:
            self.previous_x = pose.x
            self.get_logger().info("Setting colour to green...")
            self.call_set_pen_service(0, 255, 0, 5, 0)
        elif pose.x <= 5.5 and self.previous_x > 5.5:
            self.previous_x = pose.x
            self.get_logger().info("Setting colour to red...")
            self.call_set_pen_service(255, 0, 0, 5, 0)

    #Funcion para crear un cliente para un servicio ya creado y llamarlo segun los param que queramos
    def call_set_pen_service(self, r, g, b, width, off):
        client = self.create_client(SetPen, "/turtle1/set_pen")
        #Debemos asegurarnos de que el servicio esta activo antes de llamarlo
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for set_pen service to be ready...")
        #Creamos la request del servicio
        req = SetPen.Request()
        req.r = r
        req.g = g
        req.b = b
        req.width = width
        req.off = off
        #Lanzamos la peticion de forma asincrona
        #client.call(req, self.set_pen_callback) esto seria de forma sincrona, bloqueando hasta que se reciba la respuesta
        result = client.call_async(req)
        result.add_done_callback(partial(self.set_pen_callback))
        self.get_logger().info("Set pen request sent")

    #Funcion para recibir la respuesta del servicio
    def set_pen_callback(self, result):
        self.get_logger().info("Set pen response received")
        try:
            #En este caso la respuesta no contiene informacion relevante porque el servicio no devuelve nada
            response = result.result()
        except Exception as e:
            self.get_logger().error("Service set_pen call failed: " + str(e))


def main(args=None):
    rclpy.init(args=args)

    node = ClosedLoopNode()
    rclpy.spin(node)

    rclpy.shutdown()