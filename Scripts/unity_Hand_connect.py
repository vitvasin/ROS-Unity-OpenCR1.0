#!/usr/bin/env python

import time, random, subprocess, rospy
from tkinter import FALSE
from xmlrpc.client import Boolean, boolean
from pymycobot.mycobot import MyCobot
# from pythonAPI.mycobot3 import MyCobot as MyCobot3
from pymycobot.genre import Angle, Coord
from std_msgs.msg import Float32MultiArray, Bool
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Quaternion
import tf

class HandNode():
    port = subprocess.check_output(['echo -n /dev/Mycobot'], 
                                    shell=True).decode()
    mycobot = MyCobot(port)

    mycobot.set_color(255, 255, 255)
    time.sleep(1)
    coord_list = [50, -200, 200, 0, 0, -45] # Home
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",coord_list)
    mycobot.send_coords(coord_list, 30, 0)
    

    def __init__(self):
        self.sub1 = rospy.Subscriber('/hand_flag', Float32MultiArray, self.callback)
        #self.sub2 = rospy.Subscriber('/gripper', Bool, self.callback_grip)
        port = subprocess.check_output(['echo -n /dev/Mycobot'], shell=True).decode()
        mycobot = MyCobot(port)

    def __del__(self):
        self.mycobot.release_all_servos()

    def out(self):
        self.mycobot.release_all_servos()

    def callback(self, array):
        if array.data[6]==1:
            #coord_list = [50, -200, 200, 0, 0, -45] # Home
            #koko
            coord_list = [array.data[10], array.data[11], array.data[12], 0, 0, array.data[15]] #JOI's original
            #coord_list = [array.data[0], array.data[2], array.data[3], 0, 0, array.data[4]] #modified
            #rospy.loginfo(rospy.get_caller_id()+"I heard %s",coord_list)
            self.mycobot.send_coords(coord_list, 30, 0)
            
            #armPos = Float32MultiArray()
            #nowPos = self.mycobot.get_coords()
            #armPos[0]=nowPos[0]
            #armPos[1]=nowPos[1]
            #armPos[2]=nowPos[2]
            #self.pub.publish(armPos)
            
            


if __name__ == '__main__':
    rospy.init_node('hand_node')
    rospy.loginfo('initialized')
    node = HandNode()
    rospy.loginfo('initialized Handnode')
    
    
    while not rospy.is_shutdown():
        rospy.sleep(0)

    
