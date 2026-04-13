from catkin_pkg.python_setup import generate_distutils_setup
from distutils.core import setup

setup_args = generate_distutils_setup(
    packages=['keyboard_controller'],
    package_dir={'': '.'},
    scripts=['scripts/keyboard_node'],
    requires=['rospy', 'geometry_msgs']
)

setup(**setup_args)
