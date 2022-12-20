#!/usr/bin/env python
import rospy

import math
from std_msgs.msg import Float32MultiArray
from Tkinter import *

msg = ""
m1=NONE
m2=NONE
m3=NONE
m4=NONE
m5=NONE
l1=NONE
freq=NONE
Amp=NONE
duration=NONE
Dof=NONE
def window_component():
    global msg,m1,m2,m3,m4,m5,l1,freq,Amp,duration,Dof
    window.title('Sine input generator')
    window.minsize(width=400,height=400)
    n1= DoubleVar()
    n2= DoubleVar()
    n3= DoubleVar()
    dof_val = ('fe','lb','yaw','pitch','roll')
    n4 = StringVar(value=dof_val)
    
    Dof = Listbox(window,listvariable=n4)
    Dof.pack()
    lab = Label(text ="Amplitude(Deg)1-90")
    lab.pack()
    Amp = Entry(window,textvariable = n1)
    Amp.delete(0,END)
    Amp.insert(0,15)
    Amp.pack()

    lab = Label(text ="Frequency(Hz)")
    lab.pack()
    freq = Entry(window,textvariable = n2)
    freq.delete(0,END)
    freq.insert(0,1)
    freq.pack()

    lab = Label(text ="duration(Sec)")
    lab.pack()
    duration = Entry(window,textvariable = n3)
    duration.delete(0,END)
    duration.insert(0,3)
    duration.pack()
  #  m1 = Scale(window, from_=-180.0, to=180.0, orient = HORIZONTAL,command=send )
   # m1.set(0.0)
   # m1.pack()
  #  m2 = Scale(window, from_=-180.0, to=180.0, orient = HORIZONTAL,command=send)
  #  m2.set(0.0)
   # m2.pack()
   # m3 = Scale(window, from_=-180.0, to=180.0, orient = HORIZONTAL,command=send)
   # m3.set(0.0)
   # m3.pack()
    #m4 = Scale(window, from_=-180.0, to=180.0, orient = HORIZONTAL,command=send)
   # m4.set(0.0)
    #m4.pack()
   # m5 = Scale(window, from_=-180.0, to=180.0, orient = HORIZONTAL,command=send)
   # m5.set(0.0)
   # m5.pack()
    #l1 = Scale(window, from_=0.0, to=1.0, orient = HORIZONTAL,command=send)
    #l1.pack()
    
    
   # btn = Button(master=window, text="Home Pos",command = sendhome)
   # btn.pack()
   # btn2 = Button(master=window, text="onLed",command = sendon)
   # btn2.pack()
   # btn3 = Button(master=window, text="T",command = sendt)
   # btn3.pack()
    btn3 = Button(master=window, text="Freq_send",command = Freq)
    btn3.pack()
    #btn2 = Button(master=windwo,text ="")


def sendt():
    global msg
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
def Freq():
    global msg,freq,Amp,duration,Dof
    # get value from text box
    RATE =100 #publishing rate
    rosmsg = Float32MultiArray()
  
    rosmsg.data = [None]*56
    i=0
    while i<55:
        rosmsg.data[i]=0.0
        i+=1
    Select_indices = Dof.curselection()
    dof = ','.join([Dof.get(i) for i in Select_indices])
    a=3
    b=0
    if dof=='fe':
        a= 0
    elif dof == 'y+-':
        a= 1
    elif dof == 'lb':
        a= 2
        
    elif dof == 'pitch':
        a= 3
        b=49
    elif dof == 'yaw':
        a= 4
        b=50
    elif dof == 'roll':
        a= 5
        b=51
    rospy.loginfo(a)
    frequency = float(freq.get())
    amplitude = float(Amp.get())
    dur = float(duration.get())*RATE
    
    rate = rospy.Rate(RATE) #10hz
    step =0
    offset = 50
    while not rospy.is_shutdown():

        out = amplitude * math.sin(2*math.pi*frequency*step/RATE)

       # rosmsg.data= [0.0,0.0,0.0,out,0.0,0.0,step]
        rosmsg.data[a] = out 
        rosmsg.data[b] = out
        rosmsg.data[55] =step
        #[fe,y,lb,pitch,]
        pub.publish(rosmsg)
        step = step+1
        rate.sleep() # Wait to match the rate

        if step>dur:
            while TRUE:
                
                rosmsg.data[55] =step
                pub.publish(rosmsg)
                step = step+1
                rate.sleep() # Wait to match the rate
                if step>dur+offset:
                    break
            break
        


   # OUTPUT = amplitude * math.sin(frequency*dur)
    #msg = 'amp:' + str(amplitude)+' ,freq:' + str(frequency) + ', sine value :' + str(OUTPUT)
    #debug
    #rospy.loginfo(msg)





def send(xy):
    global msg,m1,m2,m3,m4,m5,l1

    #msg = 'S,' + str(m1.get()) + ',' + str(m2.get()) + ',' + str(m3.get()) + ',' + str(m4.get()) + ',' + str(m5.get()) + ',' + str(l1.get()) + ',F'
    rosmsg = Float32MultiArray()
    rosmsg.data = [m1.get(),l1.get(),0.0, m5.get(),m4.get(),m3.get()]
    rate = rospy.Rate(10)
    #while not rospy.is_shutdown():
    rospy.loginfo(rosmsg)
    #print(xy)
    pub.publish(rosmsg)
    #rate.sleep()

if __name__ == '__main__':
    window = Tk()
    window_component()
    rospy.init_node('frq_publisher')
    pub = rospy.Publisher("/head_command",Float32MultiArray,queue_size=1000)
    window.mainloop() 
    rospy.loginfo("Node was stopped")



