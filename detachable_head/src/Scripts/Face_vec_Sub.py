#!/usr/bin/env python

from optparse import Values

import rospy, math, numpy as np
from std_msgs.msg import Float32MultiArray, Bool




AHx= 205 #205 mm
AHy= 0 #50 mm

def find_nearest(array, value):
    idx = np.argmin(np.abs(np.array(array)-value))
    return array[idx]


def callback(data):
    global yaw,trigger
    #data = Float32MultiArray
    distance = data.data[0]
    pitch = data.data[1]
    roll = data.data[2]
    #yaw = data.data[3]
    #yaw = 53
    #rospy.loginfo('Distance =' + str(distance) +', Yaw =' + str(yaw)+ 'Trigger' + str(trigger))
    [X,Y] = calculate_robot_pos(distance,pitch,yaw)
    robot_aim_pos = Float32MultiArray()
    robot_aim_pos.data = [X,Y, trigger]
    if(trigger >0):
        pub.publish(robot_aim_pos)
    trigger = 0
    #rospy.loginfo('X =' + str(X) + ',Z = ' + str(Y))

def callback2(data):
    global yaw
    yaw = -1*data.data[4]
    
def callback3(data):
    global trigger
    if data.data == True:
        trigger =1.0
    else: trigger =0.0

def calculate_robot_pos(D,pitch,yaw):
    rad_yaw = math.radians(yaw)
    # X POS
    X = abs(D*math.sin(rad_yaw)-AHx) 
    # Y POS
    Y = abs(D*math.cos(rad_yaw)+AHy)
    
    # validate the robot workspace
    # Thredshoud define min, max that robot can reach

    #Mapping
    
    #estimate output Position A, B, C
    #POSA=[120,210], POSB= [20,-210], POSC= [-75,-210], DIFF_vAL=[185,531]
    arrayPos= [120,20,-75]
    #MAPPING
    X-=185
    #Y-=531
    

    X= find_nearest(arrayPos,X)
    Y=-210


    return [X,Y]


if __name__ == '__main__':
    global yaw
    yaw=0
    trigger = 0
    rospy.init_node('face_cal')
    sub = rospy.Subscriber('/fad', Float32MultiArray, callback)
    sub2 = rospy.Subscriber('/head_command', Float32MultiArray, callback2)
    sub3 = rospy.Subscriber('/hand_trigger', Bool, callback3)
    pub = rospy.Publisher('/rb_pos',Float32MultiArray, queue_size=10)
    rate=rospy.Rate(0.5)
    while not rospy.is_shutdown():
        rate.sleep()
