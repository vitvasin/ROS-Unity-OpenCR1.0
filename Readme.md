# Detachable Head ROS Package
This package has been tested on Ubuntu 20.04 with ROS Noetic. 
Make sure that ROS is installed correctly before proceeding.


## Installation
1. Clone the repository into your catkin workspace:
```
cd ~catkin_ws/src

git clone https://github.com/vitvasin/ROS-Unity-OpenCR1.0.git

cd ..

catkin_make

```
## Required Repositories
 - file_server from ROS# library: https://github.com/siemens/ros-sharp
 - Rosbridge: `sudo apt-get install ros-kinetic-rosbridge-server`
 - video_stream_opencv: http://wiki.ros.org/video_stream_opencv

## USB Connection (example)
Adjust the parameters to match your current environment:

 - Camera test with webcam: `/dev/video0`
 - OPENCR1.0 (Controller): `/dev/ttyACM0` (baudrate 9600, 57600, or 115200)
 - MyCobot: `/dev/Mycobot` (set up the fixed device name, such as product ID or address, in `/usr/lib/udev/rules.d` or create a new one)

## Demo launch file
To start the demo nodes:

1. Head only: roslaunch detachable_head detachable_head.launch
2. Arm and keyboard control: roslaunch detachable_head Experiment_EMB_TRANF.launch
3. Head, arm, and VIVE controller: roslaunch detachable_head DEMO.launch

For more information about controller setup, see the Google doc at
https://docs.google.com/document/d/17JUlJ-pTC5sRLx5VKVTQgaNw3UoYIy6Dms43cI3WPWk/edit?usp=sharing.
