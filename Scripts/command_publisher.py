#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from tkinter import *
msg = ""
m1=NONE
m2=NONE
m3=NONE
m4=NONE
m5=NONE
l1=NONE

def window_component():
    global msg,m1,m2,m3,m4,m5,l1
    window.title('GUI_test')
    window.minsize(width=400,height=400)
    m1 = Scale(window, from_=0, to=1023, orient = HORIZONTAL,command=send)
    m1.set(512)
    m1.pack()
    m2 = Scale(window, from_=0, to=1023, orient = HORIZONTAL,command=send)
    m2.set(512)
    m2.pack()
    m3 = Scale(window, from_=0, to=1023, orient = HORIZONTAL,command=send)
    m3.set(512)
    m3.pack()
    m4 = Scale(window, from_=0, to=1023, orient = HORIZONTAL,command=send)
    m4.set(512)
    m4.pack()
    m5 = Scale(window, from_=0, to=1023, orient = HORIZONTAL,command=send)
    m5.set(512)
    m5.pack()
    l1 = Scale(window, from_=0, to=1023, orient = HORIZONTAL,command=send)
    l1.pack()
    
    
    btn = Button(master=window, text="Home Pos",command = sendhome)
    btn.pack()
    btn2 = Button(master=window, text="onLed",command = sendon)
    btn2.pack()
    btn3 = Button(master=window, text="T",command = sendt)
    btn3.pack()
    #btn2 = Button(master=windwo,text ="")

def sendt():
    global msg
    msg ='T'
    rosmsg = String()
    rosmsg.data = msg
    rate = rospy.Rate(10)
    #while not rospy.is_shutdown():
    rospy.loginfo(rosmsg)
    #print(xy)
    pub.publish(rosmsg)

def sendhome():
    global msg
    msg ='Home'
    rosmsg = String()
    rosmsg.data = msg
    rate = rospy.Rate(10)
    #while not rospy.is_shutdown():
    rospy.loginfo(rosmsg)
    #print(xy)
    pub.publish(rosmsg)
def sendon():
    global msg
    msg ='on1'
    rosmsg = String()
    rosmsg.data = msg
    rate = rospy.Rate(10)
    #while not rospy.is_shutdown():
    rospy.loginfo(rosmsg)
    #print(xy)
    pub.publish(rosmsg)

def send(xy):
    global msg,m1,m2,m3,m4,m5,l1

    msg = 'S,' + str(m1.get()) + ',' + str(m2.get()) + ',' + str(m3.get()) + ',' + str(m4.get()) + ',' + str(m5.get()) + ',' + str(l1.get()) + ',F'
    rosmsg = String()
    rosmsg.data = msg
    rate = rospy.Rate(10)
    #while not rospy.is_shutdown():
    rospy.loginfo(rosmsg)
    #print(xy)
    pub.publish(rosmsg)
    #rate.sleep()

if __name__ == '__main__':
    window = Tk()
    window_component()
    rospy.init_node('command_publisher')
    pub = rospy.Publisher("/head_waist_motor_cmd",String,queue_size=10)
    window.mainloop() 
    rospy.loginfo("Node was stopped")



