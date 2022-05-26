#!/usr/bin/env python
import keyboard
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
        a = keyboard.get_hotkey_name()
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