import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from msg_srv_action_pkg.action import Fibonacci

class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self.get_logger().info("fibonacci action client started")
        #Creamos el cliente de la accion como una instancia de la clase correspondiente
        self.action_client = ActionClient(self, Fibonacci, '/fibonacci')

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        #Esperamos hasta que el servidor esta listo
        self.action_client.wait_for_server()

        #Enviamos el goal de forma asincrona, el future es el que nos dice si se ha acabado de ejecutar esa parte o no, tambien se añade el callback 
        #para el feedback
        self.send_goal_future = self.action_client.send_goal_async(goal_msg, self.feedback_callback)

        #Añadimos el callback para el resultado de la accion
        self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        #Usamos el goal_handle para saber el status en el que esta el goal, si ha sido aceptado o no
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        #Obtenemos el future del resultado en el caso de que el goal haya sido aceptado, y dejamos que su callback procese el resultado
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: ' + str(result.sequence))
        #En este caso añadimos el shutdown aqui porque el unico proposito de este nodo es enviar el goal una vez
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: ' + str(feedback.partial_sequence))

def main(args=None):

    rclpy.init(args=args)

    #Creamos el nodo, enviamos el goal y el future es el que nos dice si se ha completado
    action_client = FibonacciActionClient()
    action_client.send_goal(10)
    rclpy.spin(action_client)