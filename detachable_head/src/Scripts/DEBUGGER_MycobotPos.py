#!/usr/bin/env python
from curses import textpad
from tkinter.scrolledtext import ScrolledText
from xmlrpc.client import Boolean

from matplotlib.pyplot import text
import rospy
from std_msgs.msg import Float32MultiArray, Bool
from tkinter import *

msg = ""
m1=NONE
m2=NONE
m3=NONE
m4=NONE
m5=NONE
l1=NONE
HandFlag = True


def window_component():
    global msg,e1,e2,e3,e4,t1
    window.title('Command sender(FLOAT_MT_ARRAY32)')
    window.minsize(width=250,height=120)

    Label(window,text='Robot XYZ Position').grid(row=0,column=2,sticky=N)
    Label(window,text='X').grid(row=1, column=1,sticky=N)
    Label(window,text='Y').grid(row=1, column=2,sticky=N)
    Label(window,text='Z').grid(row=1, column=3,sticky=N)

    e1 = Entry(window,width=8)
    e2 = Entry(window,width=8)
    e3 = Entry(window,width=8)


    e1.grid(row=2, column=1)
    e2.grid(row=2, column=2)
    e3.grid(row=2, column=3)
    #coord_list = [x, z, y,-180,0,-180] #x,y,z correct
    #coord_list = [-50, -180, 300, 0, 0, 0] # Home
    e1.insert(0,'-50')
    e2.insert(0,'300')
    e3.insert(0,'-180')
    Button(window,text='Send Position',command=sendPos).grid(row=3,column=1)
    Button(window,text='Hand Open/Close',command=sendh).grid(row=3,column=3)

    Label(window,text='Topic to Echo').grid(row=4, column=1)
    e4 = Entry(window)
    e4.grid(row=4, column=2)
    e4.insert(0,'/fad')
    Label(window,text='Message Output').grid(row=5, column=1)
    t1 = ScrolledText(window,width=30,height=4)
    #t1.config(state='disabled', bg='grey100')
    t1.grid(row=5,column=2)
    Button(window,text='Check msg',command=checkmsg).grid(row=5,column=3)
    


    Button(window,text='EXIT',command=window.quit).grid(row=10,column=2,sticky=S)


def checkmsg():
    global msg,e1,e2,e3,e4,t1,a,sub
    
    rostopic = e4.get()
    a = cb
    sub= rospy.Subscriber(rostopic,Float32MultiArray,callback=a)

def cb(inpt):
    global msg,e1,e2,e3,e4,t1,a,sub
    #t1.delete('1.0',END)
    rosmsg = Float32MultiArray()
    rosmsg = inpt
    
    
    i=0
    for p in range(4):
        t1.insert(END,str(rosmsg.data[i])+ ', ')
        i+=1

    t1.insert(END,'\n')
    sub.unregister()
    
    
    
    

        


def sendPos():
    global e1,e2,e3
    rosmsg = Float32MultiArray()
    rosmsg.data = [0]*7
    rosmsg.data = [float(e1.get()),float(e2.get()),float(e3.get()),1,1,0,0]
    pub.publish(rosmsg)
   # rosbool = Bool()
   # rosbool.data = True
   # pub3.publish(rosbool)

def sendh():
    global msg,h1,HandFlag
    rosmsg = Bool()
    
    if  HandFlag == True:
        rosmsg.data =True
    else: rosmsg.data =False
    HandFlag = not HandFlag

    rospy.loginfo(rosmsg)
    #print(xy)
    pub2.publish(rosmsg)

def sendhome():
    global msg

def sendon():
    global msg

def send(xy):
    global msg,m1,m2,m3,m4,m5,l1

    #msg = 'S,' + str(m1.get()) + ',' + str(m2.get()) + ',' + str(m3.get()) + ',' + str(m4.get()) + ',' + str(m5.get()) + ',' + str(l1.get()) + ',F'
    rosmsg = Float32MultiArray()
    rosmsg.data = [0]*22
    rosmsg.data = [m1.get(),l1.get(),m2.get(), m5.get(),m4.get(),m3.get(),1]
    
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
    pub = rospy.Publisher("/mycobotPos",Float32MultiArray,queue_size=10)
    pub2 = rospy.Publisher("/grip_ind",Bool,queue_size=10)
    pub3 = rospy.Publisher("/hand_trigger",Bool,queue_size=10)
    window.mainloop() 
    rospy.loginfo("Node was stopped")