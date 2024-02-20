#!/usr/bin/env python3

import time, random, subprocess, rospy, os, threading
from tkinter import FALSE, Y
from xmlrpc.client import Boolean, boolean
from pymycobot.mycobot import MyCobot
# from pythonAPI.mycobot3 import MyCobot as MyCobot3
from pymycobot.genre import Angle, Coord
from std_msgs.msg import Float32MultiArray, Bool, Int16
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Quaternion
import tf
import math
#import serial


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
    global mycobot, currentRot, pub, x,z
    #if array.data[6]==1:
    #coord_list = [50, -200, 200, 0, 0, -45] # Home
    #koko
    ##
    #x = int(array.data[0])
    rospy.loginfo(array.data)
    x= array.data[0]
    if x>350: x= 350
    if x<-350: x= -350


    #y = int(array.data[1])
    y= array.data[1]
    if y>350: y= 350
    if y<200: y= 200
    #z = int(array.data[2])
    z = array.data[2]
    if z>-120: z= -120
    if z<-280: z= -280
    rotx = int(array.data[3])
    roty = int(array.data[4])
    rotz = int(array.data[5])
    #rotz = mycobot.get_angles()
    #coord_list = [50, -100, 300,rotx,0,0] #x,y,z correct
    if array.data[4] ==1:
        
        #coord_list = [x, z, y,-170,0,-180] #x,y,z correct
        #coord_list = [x, z, y,-180,0,-180] #x,y,z correct
        coord_list = [x, z, y,0,180,0] #x,y,z correct
        #rospy.loginfo('Received_FROM_CONTROLLER:' + str(coord_list))
        mycobot.send_coords(coord_list, 65, 1)
        #mycobot.sync_send_coords(coord_list,80,1,7)
        
    else :
        currentCoord = coord_list = [x, z, 280,0,180,0]
        if currentCoord is not None:
            mes = Float32MultiArray()
            mes.data = currentCoord
            pub.publish(mes)
            #rospy.loginfo("current cord:" + str(mes.data))
    #
    #mycobot.send_coords(coord_list, 80, 0)
    #mycobot.sync_send_coords(coord_list, 50, 1, timeout=7)
    #time.sleep(0.01)
    #mycobot.send_coord(Coord.X.value,x,80)
    #mycobot.send_coord(Coord.Y.value,z,80)
    #mycobot.send_coord(Coord.Z.value,y,80)
    
def callback_embInput(tracker_input):
    global  detached_flag
    if detached_flag == True: return
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
    
    
def initialize_gripper():
    #mycobot.set_gripper_ini()
    #mycobot.set_speed(100)
    #mycobot.set_gripper_ini()
    mycobot.set_encoder(8,1500)
    time.sleep(2)
    mycobot.set_encoder(8,1000)
    time.sleep(2)
    mycobot.set_encoder(8,1500)
    time.sleep(2)

def mycobot_listenner() :
    global mycobot, pub, subco, detached_flag

    #subco=rospy.Subscriber('/mycobotPos', Float32MultiArray, callback,queue_size=1)
    emb_input=rospy.Subscriber('/embInput', Float32MultiArray, callback_embInput,queue_size=1)
    subco =emb_input
    #rospy.Subscriber('/grip_ind',Bool,callback_grip,queue_size=5)
    #rospy.Subscriber('/pad',Bool,callback_pad,queue_size=5)
    #rospy.Subscriber('/mycobotPos', Float32MultiArray, callback,queue_size=1)
    #pub = rospy.Publisher('/mycobotCoords',Float32MultiArray,queue_size=1)
    #Mycobot_Mapping_Position()


    

    rospy.spin()
    
def publish_messages(topic, message_type, rate, message_constructor):
    """
    Function to publish messages to a given topic at a specified rate.

    :param topic: Topic name
    :param message_type: ROS message type (e.g., std_msgs.msg.String)
    :param rate: Publishing rate in Hz
    :param message_constructor: A function to construct the message
    """
    publisher =  rospy.Publisher('/mycobotCoords',Float32MultiArray,queue_size=1)
    rate = rospy.Rate(rate)

    while not rospy.is_shutdown():
        message = Mycobot_Mapping_Position() 
        publisher.publish(message)
        #rospy.loginfo(message)
        rate.sleep()

def Mycobot_Mapping_Position() :
    global mycobot, pub, subco
    Current_Coords = mycobot.get_coords()
    x = Current_Coords[0]
    y = Current_Coords[1]
    z = Current_Coords[2]    
    
    return MAP_CAL(x,y)
    
def MAP_CAL(dx,dy):
    #//data[0] = Position
    #//data[1] = pressure level
    # Define the pressure side
    Pos =0
    Plevel = 0
    if dx > 0 and dy > 0:
        Pos = 1 #UR
    elif dx < 0 and dy > 0:
        Pos = 2 #UL
    elif dx < 0 and dy < 0:
        Pos = 3 #LL
    elif dx > 0 and dy < 0:
        Pos = 4 #LR
    
    #Define pressure level
    #calculate how far from the home pos int 3 level near, mid, far
    
    
    r = math.sqrt(dx*dx + dy*dy)
    
    if r > 0 and r < 100:
        Plevel = 1
    elif r > 100 and r < 200 :
        Plevel = 2
    elif r > 200 and r < 300 :
        Plevel = 3


    out = Float32MultiArray()
    
    out.data = [Pos,Plevel]
    #rospy.loginfo("info message")
    #rospy.loginfo(out.data)
    return  out


def init_mycobot():
    global mycobot
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



    rospy.loginfo('initialized Handnode')

def checkConnection():
    while 1: # Loop to check connection
        x = os.path.exists('/dev/Mycobot2')
        if x==1 :
            #print('connected')
            break
        else:
            #print('disconnected')
            None
        time.sleep(0.1)


def thread_check_connection():
    global subco, detached_flag
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
                    rospy.loginfo('myCobot_Disconnected')    
                    init_mycobot()
                    #subco=rospy.Subscriber('/mycobotPos', Float32MultiArray, callback,queue_size=1)
                    subco=rospy.Subscriber('/embInput', Float32MultiArray, callback_embInput,queue_size=1)
                    break
                if t_flag == True: break
                time.sleep(0.3)

        if t_flag == True: break
        time.sleep(1)

def shutdown_hook():
    global mycobot, t_flag
    rospy.loginfo("Shutting down MyCobot node...")
    t_flag = True  # Signal to threads to stop
    #mycobot.release_all_servos()  # Release servos
    reset = [0, 0, 0, 0, 0, 0]
    mycobot.send_angles(reset, 30)
    mycobot.set_color(255, 0, 0)  # Optionally set color to indicate shutdown
    mycobot.stop()
    rospy.loginfo("Shutdown complete.")


if __name__ == '__main__':
    global mycobot, t_flag
    t_flag = False
    rospy.init_node('hand_node')
    #rospy.on_shutdown(shutdown_hook)  # Register shutdown hook
    rospy.loginfo('initialized arm node')
    
    t1= threading.Thread(target=thread_check_connection, name = 't1')
    
    checkConnection()
    init_mycobot()
    initialize_gripper()
    #t2 = threading.Thread(target=publish_messages, args=('/mycobotCoords',Mycobot_Mapping_Position() , 10,Float32MultiArray ))
    # Start the threads
    #t2.start()
    # Keep the main thread alive
    #t2.join()
    t1.start() # start checking serial thread
    mycobot_listenner() 
    rospy.loginfo("Shutting down MyCobot node...")
    t_flag = True  # Signal to threads to stop
    #mycobot.release_all_servos()  # Release servos
    reset = [0, 0, 0, 0, 0, 0]
    mycobot.send_angles(reset, 30)
    mycobot.set_color(255, 0, 0)  # Optionally set color to indicate shutdown
    rospy.loginfo("Shutdown complete.")

    
