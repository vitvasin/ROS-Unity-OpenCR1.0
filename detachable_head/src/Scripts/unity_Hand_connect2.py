#!/usr/bin/env python

import time, random, subprocess, rospy
from tkinter import FALSE, Y
from xmlrpc.client import Boolean, boolean
from pymycobot.mycobot import MyCobot
# from pythonAPI.mycobot3 import MyCobot as MyCobot3
from pymycobot.genre import Angle, Coord
from std_msgs.msg import Float32MultiArray, Bool, Int16
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Quaternion
import tf



def __del__():
    global mycobot
    mycobot.release_all_servos()

def out():
    global mycobot
    mycobot.release_all_servos()

def read_angle(angle):
    global currentRot
    currentRot = angle.data


def callback(array):
    global mycobot, currentRot, pub
    #if array.data[6]==1:
    #coord_list = [50, -200, 200, 0, 0, -45] # Home
    #koko
    ##
    #x = int(array.data[0])
    x= array.data[0]
    if x>270: x= 270
    if x<-270: x= -270


    #y = int(array.data[1])
    y= array.data[1]
    if y>300: y= 300
    if y<125: y= 125
    #z = int(array.data[2])
    z = array.data[2]
    if z>-120: z= -120
    if z<-270: z= -270
    rotx = int(array.data[3])
    roty = int(array.data[4])
    rotz = int(array.data[5])
    #rotz = mycobot.get_angles()
    #coord_list = [50, -100, 300,rotx,0,0] #x,y,z correct
    if array.data[4] ==1:
        
        #coord_list = [x, z, y,-170,0,-180] #x,y,z correct
        coord_list = [x, z, y,-170,0,rotz] #x,y,z correct
        
        rospy.loginfo(coord_list)
        mycobot.send_coords(coord_list, 80, 1)
        #mycobot.sync_send_coords(coord_list,80,1,7)
        
    else :
        currentCoord = mycobot.get_coords()
        if currentCoord is not None:
            mes = Float32MultiArray()
            mes.data = currentCoord
            pub.publish(mes)
            #rospy.loginfo(mes.data)
    #
    #mycobot.send_coords(coord_list, 80, 0)
    #mycobot.sync_send_coords(coord_list, 50, 1, timeout=7)
    #time.sleep(0.01)
    #mycobot.send_coord(Coord.X.value,x,80)
    #mycobot.send_coord(Coord.Y.value,z,80)
    #mycobot.send_coord(Coord.Z.value,y,80)


def mycobot_listenner() :
    global mycobot, pub
    rospy.init_node('hand_node')
    rospy.loginfo('initialized')
    rospy.Subscriber('/mycobotPos', Float32MultiArray, callback,queue_size=1)
    pub = rospy.Publisher('/mycobotCoords',Float32MultiArray,queue_size=1)



    rospy.spin()
            


if __name__ == '__main__':
    global mycobot
    reset = [0, 0, 0, 0, 0, 0]
    
    port = subprocess.check_output(['echo -n /dev/Mycobot'], 
                                    shell=True).decode()
    mycobot = MyCobot(port)

    mycobot.set_color(255, 255, 255)
    time.sleep(1)
    mycobot.send_angles(reset,30)
    coord_list = [50, -100, 300, 0, 0, 0] # Home
    coord_list = [-50, -180, 250, -170, 0, -180] # Home
    time.sleep(3)
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",coord_list)
    mycobot.send_coords(coord_list, 30, 1)
    #mycobot.release_all_servos()
    #while 1:
    #    a=mycobot.get_coords()
    #    print(a)

    rospy.loginfo('initialized Handnode')

    mycobot_listenner() 
    
    mycobot.send_angles(reset, 30)
    mycobot.set_color(255, 0, 0)
    #node.mycobot.release_all_servos()

    
