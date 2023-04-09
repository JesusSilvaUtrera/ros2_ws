#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

//Se crea la clase del nodo, que hereda de rclcpp::Node. Cualquier this que haya en el codigo se refiere al nodo
class MinimalPublisher : public rclcpp::Node
{
public:
  //Se crea el constructor de la clase, dandole el nombre al nodo e inicializando la vble count_ a 0
  MinimalPublisher()
  : Node("minimal_publisher"), count_(0)
  {
    //Se crea el publisher usando this->, que seria el self. de python, con el tipo de mensaje String, el nombre del topic y la queue_size
    publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
    //Se crea la variable timer_ que hace que se ejecute el timer callback cada medio segundo
    timer_ = this->create_wall_timer(
      500ms, std::bind(&MinimalPublisher::timer_callback, this));
  }

private:
  void timer_callback()
  {
    auto message = std_msgs::msg::String();
    message.data = "Hello, world! " + std::to_string(count_++);
    //Con esto se saca en los logs lo que se está publicando
    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
    //Se envia el mensaje al publisher (tener en cuenta que -> en C++ equivale al . en python, por lo que para usar cualquier metodo se usa)
    publisher_->publish(message);
  }
  //Declaraciones de las vbles de timer, publisher y counter que se hacen privadas para que nadie pueda modificar su tipo
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  size_t count_;
};

int main(int argc, char * argv[])
{
  //Al igual que se hacia en python, en el main se coloca el init, el shutdown y en medio el codigo necesario
  rclcpp::init(argc, argv);
  //Se usa el spin para dejar activo el nodo, y el make_shared es para crear un puntero compartido que apunta a la instancia de la clase que se va a usar 
  //para el nodo
  rclcpp::spin(std::make_shared<MinimalPublisher>());
  rclcpp::shutdown();
  return 0;
}
