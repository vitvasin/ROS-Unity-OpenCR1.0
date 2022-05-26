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


def initialize_gripper():
    #mycobot.set_gripper_ini()
    #mycobot.set_speed(100)
    mycobot.set_encoder(8,2800)
    time.sleep(1)
    mycobot.set_encoder(8,1500)
    time.sleep(1)
    mycobot.set_encoder(8,2800)
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

    #rospy.loginfo('Gripper:' + str(input.data[6]))
    #rospy.loginfo(input.data[6])
    old = input.data[6]
    current_rot= Int16()
    #read_coord = mycobot.get_coords()
    #current_rot.data = read_coord[5]
    y= int(input.data[6])
    rot = int(input.data[3])
    time.sleep(0.01)    
    mycobot.set_speed(100)
    #mycobot.set_encoder(8,y)
    if y == 0:
        mycobot.set_encoder(8,2800)
    if y== 1:
        mycobot.set_encoder(8,1500)


    if input.data[4] == 0:
        mycobot.set_encoder(7,rot)
       # print(current_rot.data)
    
    #pub.publish(current_rot)
    
    #mycobot.set_gripper_value(y, 100)
    #mycobot.send_angle(Angle.J6.value,rot,80)


        

    #mycobot.set_gripper_value(y, 100)
    #if y>1800: 
    #    mycobot.set_gripper_state(0,30)
    #if y<1500:
    #    mycobot.set_gripper_state(1,30)   

    #mycobot.set_gripper_state(1)


def gripper_listenner() :
    rospy.init_node('Gripper', anonymous=True)
    rospy.Subscriber('/mycobotPos',Float32MultiArray,callback,queue_size=1)
    
    #rospy.Subscriber('/gripperValue',Float32,callback)
    rospy.spin()



if __name__ == '__main__':
    global old, mycobot, pub
    time.sleep(3)
    old = 1500
    pub = rospy.Publisher('/Current_Rotation',Int16,queue_size=1)
    port = subprocess.check_output(['echo -n /dev/Mycobot'], 
                                    shell=True).decode()
    mycobot = MyCobot(port)

    initialize_gripper() # close at start
    print( 'gripper_node_started')
    
    rospy.logout('gripper_node_started')
    gripper_listenner()