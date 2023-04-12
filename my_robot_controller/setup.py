from setuptools import setup

package_name = 'my_robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jsilva',
    maintainer_email='jsilvautrera@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'test_node = my_robot_controller.first_node:main',
            'closed_loop = my_robot_controller.closed_loop:main',
            'action_server = my_robot_controller.fibonacci_action_server:main',
            'action_client = my_robot_controller.fibonacci_action_client:main',
        ],
    },
)
