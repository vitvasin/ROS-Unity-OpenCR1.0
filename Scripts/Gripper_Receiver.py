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
import colorsys


def initialize_gripper():
    mycobot.set_gripper_value(1500, 70)
    while mycobot.get_gripper_value() > 1600 :
        mycobot.set_gripper_value(1500, 70)
    time.sleep(0.5)

    mycobot.set_gripper_value(2048, 70)
    while mycobot.get_gripper_value() < 1900 :
        mycobot.set_gripper_value(2048, 70)
    time.sleep(0.5)

    mycobot.set_gripper_value(1500, 70)
    while mycobot.get_gripper_value() > 1600 :
        mycobot.set_gripper_value(1500, 70)
    time.sleep(0.5)


def callback(input):
    global old, mycobot

    
    if old != input.data:
        rospy.loginfo('Gripper:' + str(input.data))
        rospy.loginfo(input.data)
        old = input.data
        if input.data == True:
            rospy.loginfo('on')
            #self.mycobot.set_gripper_state(0,80)
            print(mycobot.get_gripper_value())
            #mycobot.set_gripper_state(0, 80)
            mycobot.set_gripper_value(2048, 70)
            while mycobot.get_gripper_value() < 1900 :
                mycobot.set_gripper_value(2048, 70)

        if input.data == False:
            rospy.loginfo('off')
            #self.mycobot.set_gripper_state(1,80)
            print(mycobot.get_gripper_value())
            #mycobot.set_gripper_state(1, 80)
            mycobot.set_gripper_value(1500, 70)
            while mycobot.get_gripper_value() > 1600 :
                mycobot.set_gripper_value(1500, 70)

def gripper_listenner() :
    rospy.init_node('Gripper', anonymous=True)
    rospy.Subscriber('/gripper',Bool,callback)
    rospy.spin()



if __name__ == '__main__':
    global old, mycobot
    old = False
    port = subprocess.check_output(['echo -n /dev/Mycobot'], 
                                    shell=True).decode()
    mycobot = MyCobot(port)
    initialize_gripper() # close at start
    print( 'gripper_node_started')
    
    #rospy.logout('gripper_node_started')
    gripper_listenner()