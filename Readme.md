Used package

1. Detachable head
2. file_server >>> pull from ROS# library >>> https://github.com/siemens/ros-sharp

Additional download 

3. Rosbridge library >>>> `sudo apt-get install ros-kinetic-rosbridge-server`
4. video steam opencv >>>  pull from this library >>>> http://wiki.ros.org/video_stream_opencv
5. rosserial library >>>> `sudo apt-get install ros-kinetic-rosserial`
             >>>>> `sudo apt-get install ros-kinetic-rosserial-arduino`

Install

1. `cd <ws>/src`
2.  `git clone https://github.com/vitvasin/ROS-Unity-OpenCR1.0.git`
3.  `cd <ws>`
4.  `catkin_make`


USB connection (depend on environment)
- Camera test with webcam  >>>> /dev/video0 
- OPENCR1.0 (Controller) >>>>> /dev/ttyACM0 baudrate 57600

RUN
To start nodes RUN  `roslaunch detachable_head detachable_head.launch`

Google doc for more info >>> https://docs.google.com/document/d/17JUlJ-pTC5sRLx5VKVTQgaNw3UoYIy6Dms43cI3WPWk/edit?usp=sharing
