Tested on Ububtu 20.04-ROS Noetic

package in this Repository
1. Detachable head
To install
`cd catkin_ws/src`


Additional Repository
2. file_server >>> from ROS# library >>> https://github.com/siemens/ros-sharp
3. Rosbridge >>>> sudo apt-get install ros-kinetic-rosbridge-server
4. video steam opencv >>> http://wiki.ros.org/video_stream_opencv

USB connection (example) // adjust the parameter to the current environment
- Camera test with webcam  >>>> /dev/video0 
- OPENCR1.0 (Controller) >>>>> /dev/ttyACM0 baudrate 9600, 57600, 115200
- MyCobot >>>>> /dev/Mycobot >>>> setup the fix device name (bind with product ID, address, etc. ) in/usr/lib/udev/rules.d > or make new one

To start nodes demo RUN (Only head) >>>> roslaunch detachable_head detachable_head.launch
To start nodes demo RUN (Only arm+kbcontrol) >>>> roslaunch detachable_head Experiment_EMB_TRANF.launch
To start nodes demo RUN (Head + Arm + VIVE Controller) >>>> roslaunch detachable_head DEMO.launch



Google doc for more info. related to controller setup >>> https://docs.google.com/document/d/17JUlJ-pTC5sRLx5VKVTQgaNw3UoYIy6Dms43cI3WPWk/edit?usp=sharing
