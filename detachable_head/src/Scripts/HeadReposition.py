#!/usr/bin/env python
import rospy
from std_msgs.msg import Int8MultiArray

def talker():
    global pub
    
    pub = rospy.Publisher('/head_setup', Int8MultiArray, queue_size=10)
    return
    rospy.init_node('RePos',anonymous=True)
    rate=rospy.Rate(10)
    a=Int8MultiArray()
    a.data = [0]*5
    a.data[0] =0
    
    while not rospy.is_shutdown():
        rospy.loginfo('Standby')
        rate.sleep()
        pub.publish(a)
    

def onshut():
    a=Int8MultiArray()
    a.data = [0]*5
    a.data[0] =0
    rospy.loginfo('Restart')
    a.data[0] =1
    pub.publish(a)

if __name__ == '__main__':
    try:
        talker()
        rospy.on_shutdown(onshut)
    except rospy.ROSInterruptException:
        pass