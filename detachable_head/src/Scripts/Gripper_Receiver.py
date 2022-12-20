#!/usr/bin/env python

import time, random, subprocess, rospy
from tkinter import FALSE
from xmlrpc.client import Boolean, boolean
from pymycobot.mycobot import MyCobot
# from pythonAPI.mycobot3 import MyCobot as MyCobot3
from pymycobot.genre import Angle, Coord
from std_msgs.msg import Float32MultiArray, Bool, Float32, Int16
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Quaternion
import tf
import colorsys
import serial

def initialize_gripper():
    #mycobot.set_gripper_ini()
    #mycobot.set_speed(100)
    mycobot.set_encoder(8,1500)
    time.sleep(1)
    mycobot.set_encoder(8,800)
    time.sleep(1)
    mycobot.set_encoder(8,1500)
    time.sleep(1)


    #mycobot.set_gripper_value(1500, 70)
    #print(mycobot.get_gripper_value())
    #while mycobot.get_gripper_value() > 1600 :
    #    mycobot.set_gripper_value(1500, 70)
    #time.sleep(0.5)
 
    #mycobot.set_gripper_value(2000, 70)
    #print(mycobot.get_gripper_value())
    #while mycobot.get_gripper_value() < 1900 :
    #   mycobot.set_gripper_value(2048, 70)
    #time.sleep(0.5)
    
    #mycobot.set_servo_data(7,55,0)
    #a = mycobot.get_servo_data(7,55)
    #mycobot.focus_servo(7)
    #a =mycobot.is_servo_enable(7)
    #mycobot.release_servo(7)
    #print(a)
   # mycobot.set_gripper_value(1500, 70)
   # while mycobot.get_gripper_value() > 1600 :
   #     mycobot.set_gripper_value(1500, 70)
   # time.sleep(0.5)


def callback(input):
    global old, mycobot, pub
    y= input.data

    if y == False:
        mycobot.set_encoder(8,1500)
    if y== True:
        mycobot.set_encoder(8,800)



def gripper_listenner() :
    rospy.init_node('Gripper', anonymous=True)
    rospy.Subscriber('/grip_ind',Bool,callback,queue_size=1)
    
    #rospy.Subscriber('/gripperValue',Float32,callback)
    rospy.spin()



if __name__ == '__main__':
    global old, mycobot, pub
    time.sleep(3)
    old = 1500
    pub = rospy.Publisher('/Current_Rotation',Int16,queue_size=1)
    #port = subprocess.check_output(['echo -n /dev/Mycobot'], 
    #                                shell=True).decode()
    #mycobot = MyCobot(port)
    #ser = serial.Serial("/dev/Mycobot", 115200, timeout = 1)
   # ser.close()
    mycobot = MyCobot('/dev/ttyUSB0')
    initialize_gripper() # close at start
    print( 'gripper_node_started')
    
    rospy.logout('gripper_node_started')
    gripper_listenner()