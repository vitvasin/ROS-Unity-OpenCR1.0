#!/usr/bin/env python

import time, random, subprocess, rospy
from tkinter import FALSE, Y
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
    coord_list = [50, -100, 300, 0, 0, 45] # Home
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",coord_list)
    mycobot.send_coords(coord_list, 30, 0)
    

    def __init__(self):
        global mycobot
        self.sub1 = rospy.Subscriber('/hand_flag', Float32MultiArray, self.callback,queue_size=10)
        #self.sub2 = rospy.Subscriber('/gripper', Bool, self.callback_grip)
        port = subprocess.check_output(['echo -n /dev/Mycobot'], shell=True).decode()
        mycobot = MyCobot(port)

    def __del__(self):
        global mycobot
        mycobot.release_all_servos()

    def out(self):
        global mycobot
        mycobot.release_all_servos()

    def callback(self, array):
        global mycobot
        #if array.data[6]==1:
        #coord_list = [50, -200, 200, 0, 0, -45] # Home
        #koko
        ##
        x = int(array.data[10])
        y = int(array.data[11])
        z = int(array.data[12])
        #coord_list = [array.data[10], array.data[11], array.data[12], array.data[13], array.data[14], array.data[15]] #JOI's original
        #coord_list = [array.data[0], array.data[2], array.data[3], 0, 0, array.data[4]] #modified
        coord_list = [x,z,300,0,0,45]
        rospy.loginfo(coord_list)
        #time.sleep(0.1)
        mycobot.send_coords(coord_list, 80, 0)
        
        #armPos = Float32MultiArray()
        #nowPos = self.mycobot.get_coords()
        #armPos[0]=nowPos[0]
        #armPos[1]=nowPos[1]
        #armPos[2]=nowPos[2]
        #self.pub.publish(armPos)
            
            


if __name__ == '__main__':
    global mycobot
    rospy.init_node('hand_node')
    rospy.loginfo('initialized')
    node = HandNode()
    rospy.loginfo('initialized Handnode')
    
    
    while not rospy.is_shutdown():
        rospy.sleep(0.01)
    reset = [0, 0, 0, 0, 0, 0]
    mycobot.send_angles(reset, 50)
    #node.mycobot.release_all_servos()

    
