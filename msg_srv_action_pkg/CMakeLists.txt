cmake_minimum_required(VERSION 3.8)
project(msg_srv_action_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

#Se puede usar el set para mayor comodidad y juntar todas las interfaces por tipo
# set(msg_files
#   "msg/Message1.msg"
#   "msg/Message2.msg"
#   # etc
#   )

# set(srv_files
#   "srv/Service1.srv"
#   "srv/Service2.srv"
#    # etc
#   )

#Solo con el paquete y esto ya podemos especificar las interfaces que queremos construir
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Sphere.msg"
  "srv/AddThreeInts.srv"
  "action/Fibonacci.action"
  DEPENDENCIES geometry_msgs # Add packages that above messages depend on, in this case geometry_msgs for Sphere.msg
)

#Si queremos usar las interfaces propias en el mismo paquete que las hemos creado, habria que añadir esto:
# rosidl_get_typesupport_target(cpp_typesupport_target
#   ${PROJECT_NAME} rosidl_typesupport_cpp)

# target_link_libraries(<interfaz> "${cpp_typesupport_target}")

ament_package()
