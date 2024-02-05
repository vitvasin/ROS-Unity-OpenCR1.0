#!/usr/bin/env python3

import time, random, subprocess, rospy, os, threading
from tkinter import FALSE, Y
from xmlrpc.client import Boolean, boolean
from pymycobot.mycobot import MyCobot
# from pythonAPI.mycobot3 import MyCobot as MyCobot3
from pymycobot.genre import Angle, Coord
from std_msgs.msg import Float32MultiArray, Bool, Int16
import tf
import math
import pyudev
import re
import atexit
#import serial
# Initialize ROS node
rospy.init_node('mycobot_listener', anonymous=True)
rospy.loginfo("Starting MyCobot 280 monitor...")


mycobot_initialized = False
mycobot = None  # Global variable to hold MyCobot object
t_flag = False
def move_to_home_position():
    rospy.loginfo("Moving MyCobot 280 to home position...")
    home_position = [0, 0, 0, 0, 0, 0]  # Define home position angles
    mycobot.send_angles(home_position, 30)
    rospy.loginfo("MyCobot 280 is now in home position.")

def initialize_mycobot():
    global mycobot
    
    rospy.loginfo("Initializing MyCobot 280...")
    # Initialization logic here
    reset = [0, 0, 0, 0, 0, 0]
    port = '/dev/Mycobot2'
    #mycobot = MyCobot('/dev/ttyUSB0')
    mycobot = MyCobot(port)

    mycobot.set_color(255, 255, 255)
    time.sleep(2)
    mycobot.send_angles(reset,30)
    rx=0
    ry=180
    rz=0
    coord_list = [0, -180, 200, rx, ry, rz] # Home
    #coord_list = [-50, -180, 280, 0] # Home
    time.sleep(2)
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",coord_list)
    mycobot.send_coords(coord_list, 30, 1)

        # For example, sending commands to set up the MyCobot 280 for operation
        
        #atexit.register(move_to_home_position)  # Register home position function


def callback_embInput(tracker_input):
    global mycobot
    #command = data.data
    
        #assign input to the parameter/rearrange coordinate from Unity to ROS coordinate
    emb_x = -tracker_input.data[0]
    emb_y = -tracker_input.data[2]
    emb_z = tracker_input.data[1]
    
    #filter of the input
    
    
    #assign to input matrix
    coord_list_emb = [emb_x, emb_y, emb_z] #x,y,z correct
    coord_list_default = [0, -180, 250] 
    #cal_coord = coord_list_emb+coord_list_default
    
    coord_list = [0+emb_x,-180+emb_y,200+emb_z,0,180,0]
    #drive the robot
    mycobot.send_coords(coord_list, 100, 1)
    rospy.loginfo('Received_FROM_CONTROLLER:' + str(coord_list))
    #current_cord = mycobot.get_coords()
    #rospy.loginfo("current cord:" + str(current_cord))
    #rospy.loginfo(f"Received command: {command}")
    # Implement command handling logic here

def listen_to_ros_topic():
    global subco
    #rospy.Subscriber("mycobot_commands", String, mycobot_command_callback)
    subco=rospy.Subscriber('/embInput', Float32MultiArray, callback_embInput)
    rospy.loginfo("Inlistening")
    rospy.spin()

def check_mycobot_connection(device_path):
    # Use regex to find device path starting with /dev/Mycobot
    for device in os.listdir('/dev'):
        if re.match(r'Mycobot[0-9]*', device):
            return True
    return False

#rospy.loginfo("Monitoring MyCobot 280 connection. Press Ctrl+C to quit.")
def thread_check_connection():
    global subco, detached_flag,t_flag
    Flag1 = False
    detached_flag = False
    rospy.loginfo('initialized check thread')
    while 1:
        y = os.path.exists('/dev/Mycobot2')
        detached_flag = False
        if y != 1:
            if Flag1 == False:
                subco.unregister()
                Flag1 = True
            while 1:
                rospy.loginfo('myCobot_Disconnected')  
                detached_flag = True  
                check = os.path.exists('/dev/Mycobot2')
                if check == 1:
                    rospy.loginfo('myCobot_Reconnected')    
                    initialize_mycobot()
                    #subco=rospy.Subscriber('/mycobotPos', Float32MultiArray, callback,queue_size=1)
                    subco=rospy.Subscriber('/embInput', Float32MultiArray, callback_embInput,queue_size=1)
                    break
                if t_flag == True: break
                time.sleep(0.3)

        if t_flag == True: break
        time.sleep(1)
        
def main():
    global mycobot_initialized,t_flag
    t1= threading.Thread(target=thread_check_connection, name = 't1')
    t1.start
    #t2 = threading.Thread(target=publish_messages, args=('/mycobotCoords',Mycobot_Mapping_Position() , 10,Float32MultiArray ))
    # Start the threads
    #t2.start()
    # Keep the main thread alive
    #t2.join()
    t1.start() # start checking serial thread
    initialize_mycobot()
    listen_to_ros_topic() 
    t_flag = True
    move_to_home_position()
    rospy.loginfo("Shutting down MyCobot 280 monitor.")

if __name__ == '__main__':
    main()