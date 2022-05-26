#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray
from Tkinter import *

msg = ""
m1=NONE
m2=NONE
m3=NONE
m4=NONE
m5=NONE
l1=NONE
HandFlag = True


def window_component():
    global msg,m1,m2,m3,m4,m5,l1
    window.title('Command sender')
    window.minsize(width=400,height=400)
    m1 = Scale(window, from_=1000, to=2000, orient = HORIZONTAL,command=send )
    m1.set(0.0)
    m1.pack()
    m2 = Scale(window, from_=-10.0, to=10.0, orient = HORIZONTAL,command=send)
    m2.set(0.0)
    m2.pack()
    m3 = Scale(window, from_=-150.0, to=150.0, orient = HORIZONTAL,command=send)
    m3.set(0.0)
    m3.pack()
    m4 = Scale(window, from_=-150.0, to=150.0, orient = HORIZONTAL,command=send)
    m4.set(0.0)
    m4.pack()
    m5 = Scale(window, from_=-150.0, to=150.0, orient = HORIZONTAL,command=send)
    m5.set(0.0)
    m5.pack()
    l1 = Scale(window, from_=0.0, to=20000.0, orient = HORIZONTAL,command=send)
    l1.pack()
    #h1 = Scale(window, from_=0.0, to=1.0, orient = HORIZONTAL,command=send)
    #l1.pack()
    
    
    btn = Button(master=window, text="HandOpen/Close",command = sendh)
    btn.pack()
   # btn2 = Button(master=window, text="onLed",command = sendon)
   # btn2.pack()
   # btn3 = Button(master=window, text="T",command = sendt)
   # btn3.pack()
    #btn2 = Button(master=windwo,text ="")

def sendh():
    global msg,h1,HandFlag
    rosmsg = Float32MultiArray()
    rosmsg.data = [0]*22
    if  HandFlag == True:
        rosmsg.data[20] =1.0
    else: rosmsg.data[20] =0.0
    HandFlag = not HandFlag

    rospy.loginfo(rosmsg)
    #print(xy)
    pub.publish(rosmsg)
   # msg ='T'
    #rosmsg = String()
    #rosmsg.data = msg
  #  rate = rospy.Rate(10)
    #while not rospy.is_shutdown():
   # rospy.loginfo(rosmsg)
    #print(xy)
   # pub.publish(rosmsg)
    #
def sendhome():
    global msg
  #  msg ='Home'
   # rosmsg = String()
   # rosmsg.data = msg
    #rate = rospy.Rate(10)
    #while not rospy.is_shutdown():
   # rospy.loginfo(rosmsg)
    #print(xy)
   # pub.publish(rosmsg)
def sendon():
    global msg
   # msg ='on1'
   # rosmsg = String()
    #rosmsg.data = msg
    #rate = rospy.Rate(10)
    #while not rospy.is_shutdown():
    #rospy.loginfo(rosmsg)
    #print(xy)
    #pub.publish(rosmsg)

def send(xy):
    global msg,m1,m2,m3,m4,m5,l1

    #msg = 'S,' + str(m1.get()) + ',' + str(m2.get()) + ',' + str(m3.get()) + ',' + str(m4.get()) + ',' + str(m5.get()) + ',' + str(l1.get()) + ',F'
    rosmsg = Float32MultiArray()
    #rosmsg.data = [m1.get(),l1.get(),m2.get(), m5.get(),m4.get(),m3.get()]
    rosmsg.data = [50, -100, 300, 0, 0, 0,int(m1.get())]
    rate = rospy.Rate(100)
    #while not rospy.is_shutdown():
    rospy.loginfo(rosmsg)
    #print(xy)
    pub.publish(rosmsg)
    #rate.sleep()

if __name__ == '__main__':
    window = Tk()
    window_component()
    rospy.init_node('command_publisher')
    pub = rospy.Publisher("/mycobotPos",Float32MultiArray,queue_size=10)
    window.mainloop() 
    rospy.loginfo("Node was stopped")



