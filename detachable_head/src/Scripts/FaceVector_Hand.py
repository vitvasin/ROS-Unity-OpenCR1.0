#!/usr/bin/env python

from distutils.log import debug
import time, random, subprocess, rospy, os, threading

from numpy import math
from tkinter import FALSE, Y
from xmlrpc.client import Boolean, boolean
from pymycobot.mycobot import MyCobot
# from pythonAPI.mycobot3 import MyCobot as MyCobot3
from pymycobot.genre import Angle, Coord
from std_msgs.msg import Float32MultiArray, Bool, Int16
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Quaternion
import tf
import serial


def __del__():
    global mycobot
    mycobot.release_all_servos()

def out():
    global mycobot
    mycobot.release_all_servos()

def read_angle(angle):
    global currentRot
    currentRot = angle.data

def grabat(X,Z):
    if os.path.exists('/dev/Mycobot') != 1:
        print('received command but myCobot unavailable')
        return
    if math.sqrt(X**2+Z**2) > 280:
        mycobot.set_color(255, 255, 0)
        return
    
    mycobot.set_color(0, 255, 0)
    rx= 0
    # POS 1 AIM
    coord_list = [X, Z, 280,rx,0,0] #x,y,z correct
    rospy.loginfo('Received:' + str(coord_list))
    mycobot.send_coords(coord_list, 80, 1)

    #POS 1 getDown
    time.sleep(2)
    coord_list = [X, Z, 210,rx,0,0] #x,y,z correct
    rospy.loginfo('Received:' + str(coord_list))
    mycobot.send_coords(coord_list, 50, 1)

    #POS 1 catch
    time.sleep(2)
    mycobot.set_encoder(8,800)

    #POS 1 getUp
    time.sleep(2)
    coord_list = [X, Z, 280,rx,0,0] #x,y,z correct
    rospy.loginfo('Received:' + str(coord_list))
    mycobot.send_coords(coord_list, 50, 1)

    # POS 2
    coord_list = [120, -210, 280, rx, 0, 0] # Home
    time.sleep(2)
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",coord_list)
    mycobot.send_coords(coord_list, 50, 1)

    # POS 3
    coord_list = [150, 20, 280, rx, 0, 0] # ReleasePOS
    time.sleep(2)
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",coord_list)
    mycobot.send_coords(coord_list, 50, 1)

    #POS 3 release
    time.sleep(3)
    mycobot.set_encoder(8,1500)

def callback_direct(array):
    global mycobot
    x=array.data[0]
    z=array.data[2]
    Trigger = array.data[4]
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",array.data)
    if Trigger ==1:        
        grabat(x,z)
    Trigger =0

def callback(array):
    global mycobot, currentRot, pub

    x= array.data[0]
    #if x>270: x= 270
    #if x<-270: x= -270

    z = array.data[1]
    #if z>-120: z= -120
    #if z<-280: z= -280
    Trigger = array.data[2]

    if array.data[2] ==1:        
        grabat(x,z)
        


def mycobot_listenner() :
    global mycobot, pub
    rospy.init_node('hand_node')
    rospy.loginfo('initialized')
    rospy.Subscriber('/rb_pos', Float32MultiArray, callback,queue_size=1)
    rospy.Subscriber('/rb_pos_direct', Float32MultiArray, callback_direct,queue_size=1)
    pub = rospy.Publisher('/mycobotCoords',Float32MultiArray,queue_size=1)

    

    rospy.spin()
            
def checkConnection():
    while 1: # Loop to check connection
        x = os.path.exists('/dev/ttyUSB0')
        if x==1:
            print('connected')
            break
        else:
            print('disconnected')
        time.sleep(0.1)
        
    

def thread_check_connection():
    while 1:
        y = os.path.exists('/dev/ttyUSB0')
        if y != 1:
            #mycobot.send_angles(reset,30)
            #mycobot.set_color(255, 0, 0)
            while 1:
                print('myCobot_Disconnected')    
                check = os.path.exists('/dev/ttyUSB0')
                if check == 1:
                    init_mycobot()
                    break
                if t_flag == True: break
                time.sleep(0.1)

        if t_flag == True: break
        time.sleep(0.5)
            



def init_mycobot():
    global mycobot
    port = '/dev/Mycobot'
    #mycobot = MyCobot('/dev/ttyUSB0')
    mycobot = MyCobot(port)
 
    mycobot.set_color(255, 255, 255)
    time.sleep(2)
    mycobot.send_angles(reset,30)
    rx=0
    ry=0
    rz=0
    coord_list = [-50, -180, 280, rx, ry, rz] # Home
    #coord_list = [-50, -180, 280, 0] # Home
    time.sleep(2)
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",coord_list)
    mycobot.send_coords(coord_list, 30, 1)

    coord_list = [120, -210, 280, rx, ry, rz] # 
    #coord_list = [120, -210, 280, 0] # 
    time.sleep(2)
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",coord_list)
    mycobot.send_coords(coord_list, 30, 1)
    
    coord_list = [150, 20, 280, rx, ry, rz] #
    #coord_list = [150, 20, 280, 0] #  
    time.sleep(2)
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",coord_list)
    mycobot.send_coords(coord_list, 30, 1)

    rospy.loginfo('initialized Handnode')

if __name__ == '__main__':
    global mycobot, t_flag
    t_flag = False
    reset = [0, 0, 0, 0, 0, 0]
    t1= threading.Thread(target=thread_check_connection, name = 't1')
    checkConnection()
    init_mycobot()
    t1.start() # start checking serial thread
    mycobot_listenner() 
    t_flag = True # execute when leave the program
    mycobot.send_angles(reset, 30)
    mycobot.set_color(255, 0, 0)
    
    

    
