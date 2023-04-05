#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

#muy util usar prog orientada a objetos para crear los nodos, heredando de la clase predeterminada Node
class MyNode(Node):
    def __init__(self):
        super().__init__('first_node')
        #La clase de la que hereda ya contiene muchos metodos, con get_logger() se puede indicar el nivel de log que queremos (warn, error, debug, fatal)
        self.create_timer(1.0, self.timer_callback)

    #Metodo para la llamada al timer para sacar el mensaje cada 1 seg
    def timer_callback(self):
        self.get_logger().info("Hello")

def main(args=None):
    #Primera linea siempre inicializar con los args del main
    rclpy.init(args=args)

    #Aqui ira todo el codigo del nodo
    node = MyNode()
    rclpy.spin(node) #Si queremos hacer que cierto nodo se quede en bucle infinito

    #Ultima linea siempre cerrar las comunicaciones
    rclpy.shutdown()

if __name__ == "__main__":
    main()