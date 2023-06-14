#!/usr/bin/env python3
#Import library
import time, random, subprocess, rospy, os, threading
from tkinter import FALSE, Y
from xmlrpc.client import Boolean, boolean
from pymycobot.mycobot import MyCobot
# from pythonAPI.mycobot3 import MyCobot as MyCobot3
from pymycobot.genre import Angle, Coord
from std_msgs.msg import Float32MultiArray, Bool, Int16, String
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Quaternion
import tf
#import serial
Ar= 120
grip_F = False
grip_op = 2000
grip_cl = 850
XX=0
ZZ=-180
YY=200
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
        coord_list = [x, z, y,0,0,0] #x,y,z correct
        #rospy.loginfo('Received_FROM_CONTROLLER:' + str(coord_list))
        mycobot.send_coords(coord_list, 65, 1)
        #mycobot.sync_send_coords(coord_list,80,1,7)
        
    else :
        currentCoord = coord_list = [x, z, 280,0,0,0]
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
def initialize_gripper():
    #mycobot.set_gripper_ini()
    #mycobot.set_speed(100)
    #mycobot.set_gripper_ini()
    mycobot.set_encoder(8,grip_op)
    time.sleep(2)
    mycobot.set_encoder(8,grip_cl)
    time.sleep(2)
    mycobot.set_encoder(8,grip_op)
    time.sleep(2)

def mycobot_listenner() :
    global mycobot, pub, subco

    subco=rospy.Subscriber('/mycobotPos', Float32MultiArray, callback,queue_size=1)
    rospy.Subscriber('/grip_ind',Bool,callback_grip,queue_size=5)
    rospy.Subscriber('/pad',Bool,callback_pad,queue_size=5)
    rospy.Subscriber('/key_pub',String,callback_kb,queue_size=5)
    pub = rospy.Publisher('/mycobotCoords',Float32MultiArray,queue_size=1)


    

    rospy.spin()

def callback_grip(input):
    global old, mycobot, pub, subco, x,z, grip_F
    y= input.data

    if y == True:
        mycobot.set_encoder(8,grip_op)
    if y== False:
        subco.unregister()
        mycobot.set_encoder(8,grip_cl)
        #grabat(x,z)
        #time.sleep(0.5)
        #mycobot.set_encoder(8,1500) 
                  
        subco=rospy.Subscriber('/mycobotPos', Float32MultiArray, callback,queue_size=1)


def gripTrig():
    global mycobot,grip_F
    if grip_F == False:
        mycobot.set_encoder(8,grip_op)
        grip_F = True
    elif grip_F == True:
        mycobot.set_encoder(8,grip_cl)
        grip_F = False
        
def limit_input(x,y): #(not tested yet) limited the value of x,y to saturate in 280 radius >> 
    radius = (x ** 2 + y **2 ) ** 0.5
    if radius > 280:
        x = 280 * x / radius
        y = 280 * y / radius
    return x,y
'''
def limit_input_sphere(x, y, z, roll, pitch, yaw):
  # Calculate the radius of the point (x, y, z)
  radius = (x ** 2 + y ** 2 + z ** 2) ** 0.5

  # If the radius is greater than 280, scale the values of x, y, and z
  if radius > 280:
    x = 280 * x / radius
    y = 280 * y / radius
    z = 280 * z / radius

  # Check the limits of the joint positions and orientations
  if roll < MIN_ROLL:
    roll = MIN_ROLL
  elif roll > MAX_ROLL:
    roll = MAX_ROLL
  if pitch < MIN_PITCH:
    pitch = MIN_PITCH
  elif pitch > MAX_PITCH:
    pitch = MAX_PITCH
  if yaw < MIN_YAW:
    yaw = MIN_YAW
  elif yaw > MAX_YAW:
    yaw = MAX_YAW

  # Check the kinematic constraints of the arm
  if not is_valid_pose(x, y, z, roll, pitch, yaw):
    # If the pose is not valid, adjust the values of x, y, and z to the nearest valid values
    x = min(max(x, MIN_X), MAX_X)
    y = min(max(y, MIN_Y), MAX_Y)
    z = min(max(z, MIN_Z), MAX_Z)

  # Return the modified values of x, y, z, and the fixed radius of 280
  return x, y, z, roll, pitch, yaw, 280
'''

def limit_input_sphere(x,y,z): #(not tested yet) limited the value of x,y,z to saturate in 280 radius >> 
    radius = (x ** 2 + y **2 + z **2  ) ** 0.5
    if radius > 280:
        x = 280 * x / radius
        y = 280 * y / radius
        z = 280 * z / radius
    return x,y,z


def callback_kb(input):
    global old, mycobot, pub, subco, x,z, coord_list, XX,ZZ, YY
    subco.unregister() 
    key = input.data
    
    if key == 'left':
        XX+=4
    elif key == 'right':
        XX-=4
    elif key == 'up':
        ZZ-=4
    elif key == 'down':
        ZZ+=4
    elif key == '0':
        YY-=4
    elif key == '1':
        YY+=4
    elif key == 'space': # grab/release
        gripTrig()
    elif key == 'h': # Home 
        XX=0
        ZZ=-180
        YY= 200
        coord_list = [0, -180, 200, -180, 0, 180] # Home
        mycobot.send_coords(coord_list, 30, 1)
        time.sleep(3)
    
    ## Limited value
    if YY > 250 : YY = 250
    if YY < 80 : YY = 80
    if ZZ > -100 : ZZ = -100
    if ZZ < -300 : ZZ = -300
    if XX < -160 : XX = -160
    if XX > 160 : XX = 160
    ## Assigend value
    coord_list = [XX, ZZ, YY, -180, 0, 180] 
    rospy.loginfo(coord_list)
    ## Drive robot
    mycobot.send_coords(coord_list, 80, 1)
               
        
     

def callback_pad(input):
    global old, mycobot, pub, subco, x,z
    initCoord = []
    pad= input.data
    if pad == True or pad == False:
        subco.unregister() 
    ##    mycobot.send_angle(Angle.J5.value,30,50)
    #    time.sleep(3)
    #    mycobot.send_angle(Angle.J5.value,15,50)
        
        mycobot.jog_angle(4,1,10)
        time.sleep(1)
        mycobot.jog_stop()
            

        subco=rospy.Subscriber('/mycobotPos', Float32MultiArray, callback,queue_size=1)

def callback_JogUP(input):
    global old, mycobot, pub, subco, x,z
    initCoord = []
    pad= input.data
    if pad == True or pad == False:
        subco.unregister()
        while 1:
            mycobot.jog_angle(5,0,50)
            A= mycobot.get_angles()
            if A[4] > 15: 
                mycobot.jog_stop()
                break

        subco=rospy.Subscriber('/mycobotPos', Float32MultiArray, callback,queue_size=1)

def callback_JogDown(input):
    global old, mycobot, pub, subco, x,z
    initCoord = []
    pad= input.data
    if pad == True or pad == False:
        subco.unregister()
        mycobot.jog_angle(5,1,50)
        subco=rospy.Subscriber('/mycobotPos', Float32MultiArray, callback,queue_size=1)

def grabat(X,Z):
   # if os.path.exists('/dev/Mycobot') != 1:
   #     print('received command but myCobot unavailable')
   #     return
  #  if math.sqrt(X**2+Z**2) > 280:
  #      mycobot.set_color(255, 255, 0)
   #     return
    #Z+=17

    if Z>-120: Z= -120
    if Z<-280: Z= -280
    #X+=10
    if X>270: X= 270
    if X<-270: X= -270
    mycobot.set_color(0, 0, 255)
    rx= 0
    # POS 1 AIM
    coord_list = [X, Z, 280,rx,0,0] #x,y,z correct
    rospy.loginfo('Received:' + str(coord_list))
    mycobot.send_coords(coord_list, 30, 1)

    #POS 1 getDown
    time.sleep(2)
    coord_list = [X, Z, 190,rx,0,0] #x,y,z correct
    #rospy.loginfo('Received:' + str(coord_list))
    mycobot.send_coords(coord_list, 50, 1)

    #POS 1 catch
    time.sleep(2)
    mycobot.set_encoder(8,600)

    #POS 1 getUp
    time.sleep(2)
    coord_list = [X, Z, 280,rx,0,0] #x,y,z correct
    #rospy.loginfo('Received:' + str(coord_list))
    mycobot.send_coords(coord_list, 50, 1)
        

def init_mycobot():
    global mycobot, coord_list
    port = '/dev/Mycobot'
    #mycobot = MyCobot('/dev/ttyUSB0')
    mycobot = MyCobot(port)
 
    mycobot.set_color(255, 255, 255)
    time.sleep(2)
    mycobot.send_angles(reset,30)
    rx=-180
    ry=0
    rz=180
    coord_list = [0, -180, 200, rx, ry, rz] # Home
    #coord_list = [-50, -180, 280, 0] # Home
    time.sleep(2)
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",coord_list)
    mycobot.send_coords(coord_list, 30, 0)



    rospy.loginfo('initialized Handnode')

def checkConnection():
    while 1: # Loop to check connection
        x = os.path.exists('/dev/Mycobot')
        if x==1 :
            #print('connected')
            break
        else:
            #print('disconnected')
            None
        time.sleep(0.1)


def thread_check_connection():
    global subco
    Flag1 = False
    rospy.loginfo('initialized check thread')
    while 1:
        y = os.path.exists('/dev/Mycobot')
        if y != 1:
            if Flag1 == False:
                subco.unregister()
                Flag1 = True
            while 1:
                rospy.loginfo('myCobot_Disconnected')    
                check = os.path.exists('/dev/Mycobot')
                if check == 1:
                    rospy.loginfo('myCobot_Disconnected')    
                    init_mycobot()
                    subco=rospy.Subscriber('/mycobotPos', Float32MultiArray, callback,queue_size=1)
                    break
                if t_flag == True: break
                time.sleep(0.3)

        if t_flag == True: break
        time.sleep(1)

if __name__ == '__main__':
    global mycobot, t_flag
    t_flag = False
    rospy.init_node('hand_node')
    rospy.loginfo('initialized arm node')
    reset = [0, 0, 0, 0, 0, 0]
    t1= threading.Thread(target=thread_check_connection, name = 't1')
    checkConnection()
    init_mycobot()
    initialize_gripper()
    t1.start() # start checking serial thread
    mycobot_listenner() 
    t_flag = True # execute when leave the program
    mycobot.send_angles(reset, 30)
    mycobot.set_color(255, 0, 0)

    
