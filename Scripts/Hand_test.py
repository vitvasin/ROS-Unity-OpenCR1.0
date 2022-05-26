#!/usr/bin/env python

import time, random, subprocess, rospy
from pymycobot.mycobot import MyCobot
# from pythonAPI.mycobot3 import MyCobot as MyCobot3
from pymycobot.genre import Angle, Coord
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Quaternion
import tf

class HandNode():
    port = subprocess.check_output(['echo -n /dev/Mycobot'], 
                                    shell=True).decode()
    mycobot = MyCobot(port)
    coords = [160, 160, 160, 0, 0, 0]
    mycobot.send_coords(coords, 30, 0)
    rospy.loginfo('SET')



    def __init__(self):
        self.sub1 = rospy.Subscriber('/hand_flag', Float32MultiArray, self.callback)
        port = subprocess.check_output(['echo -n /dev/Mycobot'], shell=True).decode()
        mycobot = MyCobot(port)

    def __del__(self):
        self.mycobot.release_all_servos()


    def callback(self, array):
 
        coord_list = [array.data[0], array.data[1], array.data[2], 0, 0, array.data[3]]
        rospy.loginfo(rospy.get_caller_id()+" I heard %s",coord_list)
        self.mycobot.send_coords(coord_list, 30, 0)

            


if __name__ == '__main__':
    rospy.init_node('hand_node')
    rospy.loginfo('initialized')
    node = HandNode()
    rospy.loginfo('initialized Handnode')


    while not rospy.is_shutdown():
        rospy.sleep(0)
