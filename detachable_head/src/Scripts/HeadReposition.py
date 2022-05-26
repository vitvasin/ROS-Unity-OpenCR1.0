#!/usr/bin/env python
import rospy
from std_msgs.msg import Int8MultiArray

def talker():
    pub = rospy.Publisher('/head_setup', Int8MultiArray, queue_size=1)
    rospy.init_node('RePos',anonymous=True)
    rate=rospy.Rate(10)
    while not rospy.is_shutdown():
        rospy.loginfo('Standby')
        rate.sleep()
    rospy.loginfo('Restart')
    a=Int8MultiArray()
    a.data = [0]*5
    a.data[0] =1
    pub.publish(a)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass