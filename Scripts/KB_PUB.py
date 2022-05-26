#!/usr/bin/env python
import getch
import rospy
from rospy.impl.transport import DeadTransport
from std_msgs.msg import String #String message 
from std_msgs.msg import Int8



def keys():
    pub = rospy.Publisher('Manual_Wheel_Command',String,queue_size=10) # "key" is the publisher name
    msg = String()
    msg.data =''
    rospy.init_node('keypress',anonymous=True)
    rate = rospy.Rate(10)#try removing this line ans see what happens
    while not rospy.is_shutdown():
        #k=ord(getch.getch())# this is used to convert the keypress event in the keyboard or joypad , joystick to a ord value
        msg.data=getch.getch()
            #if ((k>=65)&(k<=68)|(k==115)|(k==113)|(k==97)):# to filter only the up , dowm ,left , right key /// this line can be removed or more key can be added to this
                #if (k==65): msg.data = 'forward'
                #if (k==66): msg.data = 'backward'
                #if (k==67): msg.data = 'right'
                #if (k==68): msg.data = 'left'
                #if (k==115): msg.data = 'stop'
        #else : msg.data = 'stop'
        rospy.loginfo(msg.data)# to print on  terminal 
        pub.publish(msg)#to publish
        msg.data = ''
                #rospy.loginfo(str(k))

        rate.sleep()

#s=115,e=101,g=103,b=98

if __name__=='__main__':
    try:
        keys()
    except rospy.ROSInterruptException:
        pass