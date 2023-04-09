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

install(TARGETS 
  nodo_prueba
  talker_demo
  listener_demo
  DESTINATION lib/${PROJECT_NAME})

ament_package()
