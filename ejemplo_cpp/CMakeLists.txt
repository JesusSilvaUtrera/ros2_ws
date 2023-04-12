cmake_minimum_required(VERSION 3.8)
project(ejemplo_cpp)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(example_interfaces REQUIRED)
find_package(msg_srv_action_pkg REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(rclcpp_components REQUIRED)

#Todo lo necesario para el servidor y el cliente de la accion
add_library(action_server SHARED
  src/Fibonacci_action_server.cpp)
target_include_directories(action_server PRIVATE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_definitions(action_server
  PRIVATE "EJEMPLO_CPP_BUILDING_DLL")
ament_target_dependencies(action_server
  "msg_srv_action_pkg"
  "rclcpp"
  "rclcpp_action"
  "rclcpp_components")
rclcpp_components_register_node(action_server PLUGIN "ejemplo_cpp::FibonacciActionServer" EXECUTABLE Fibonacci_action_server)

add_library(action_client SHARED
  src/Fibonacci_action_client.cpp)
target_include_directories(action_client PRIVATE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_definitions(action_client
  PRIVATE "EJEMPLO_CPP_BUILDING_DLL")
ament_target_dependencies(action_client
  "msg_srv_action_pkg"
  "rclcpp"
  "rclcpp_action"
  "rclcpp_components")
rclcpp_components_register_node(action_client PLUGIN "ejemplo_cpp::FibonacciActionClient" EXECUTABLE Fibonacci_action_client)

add_executable(nodo_prueba src/nodo_prueba.cpp)
target_include_directories(nodo_prueba PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_features(nodo_prueba PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17
ament_target_dependencies(
  nodo_prueba
  "rclcpp"
)

# Esto es lo que hay que añadir para crear un nuevo ejecutable, ademas de meterlo en el install
add_executable(talker_demo src/publisher_example.cpp)
ament_target_dependencies(talker_demo rclcpp std_msgs)

add_executable(listener_demo src/subscriber_example.cpp)
ament_target_dependencies(listener_demo rclcpp std_msgs)

add_executable(server_demo src/servicio_example.cpp)
ament_target_dependencies(server_demo rclcpp example_interfaces)

add_executable(client_demo src/client_example.cpp)
ament_target_dependencies(client_demo rclcpp example_interfaces)

#Para poder hacer uso de plugins en otro paquete, debemos añadir esta linea con el paquete base al que se exporta y el archivo .xml donde se especifica 
#la info de los plugins
#pluginlib_export_plugin_description_file(polygon_base plugins.xml)

install(TARGETS 
  nodo_prueba
  talker_demo
  listener_demo
  server_demo
  client_demo
  action_server
  action_client
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
  DESTINATION lib/${PROJECT_NAME}
  DIRECTORY include/
  DESTINATION include
  #TARGETS polygon_plugins
  #EXPORT export_${PROJECT_NAME})

ament_export_include_directories(
  include
)

#Esto es tambn para el uso de plugins
# ament_export_libraries(
#   polygon_plugins
# )
# ament_export_targets(
#   export_${PROJECT_NAME}
# )

ament_package()
