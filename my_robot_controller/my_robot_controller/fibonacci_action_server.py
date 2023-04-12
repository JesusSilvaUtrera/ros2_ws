import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
import time

from msg_srv_action_pkg.action import Fibonacci

#Mucho mas sencillo que en C++, creamos la clase a partir de la clase original
class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self.get_logger().info("fibonacci action server started")
        #Creamos el servidor con el tipo, el nombre y la funcion manejadora
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        #Inicializar
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        #Calcular la secuencia de fibonacci
        for i in range(1, goal_handle.request.order):
            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i-1])
            #Mostramos por pantalla el feedback y lo enviamos al cliente
            self.get_logger().info('Feedback: ' + str(feedback_msg.partial_sequence))
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)
        
        goal_handle.succeed() #Necesario para que el status del goal no sea aborted (por defecto toma ese valor)

        #Enviamos la respuesta
        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        return result


def main(args=None):
    rclpy.init(args=args)

    fibonacci_action_server = FibonacciActionServer()

    rclpy.spin(fibonacci_action_server)


if __name__ == '__main__':
    main()