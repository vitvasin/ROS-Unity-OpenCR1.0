Tested on Ububtu 20.04-ROS Noetic

package in this Repos.
1. Detachable head

Additional Repos
2. file_server >>> from ROS# library >>> https://github.com/siemens/ros-sharp
3. Rosbridge >>>> sudo apt-get install ros-kinetic-rosbridge-server
4. video steam opencv >>> http://wiki.ros.org/video_stream_opencv

USB connection (example) // adjust the parameter to the current environment
- Camera test with webcam  >>>> /dev/video0 
- OPENCR1.0 (Controller) >>>>> /dev/ttyACM0 baudrate 9600, 57600, 115200


To start nodes demo RUN >>>> roslaunch detachable_head detachable_head.launch

Google doc for more info >>> https://docs.google.com/document/d/17JUlJ-pTC5sRLx5VKVTQgaNw3UoYIy6Dms43cI3WPWk/edit?usp=sharing
