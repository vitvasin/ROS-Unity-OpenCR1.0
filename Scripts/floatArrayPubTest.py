#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32MultiArray

if __name__ == '__main__':
    rospy.init_node('floatArray')

    pub = rospy.Publisher("/head_waist_motor_cmd",Float32MultiArray, queue_size = 7)

    rate = rospy.Rate(125)
    x=1.0
    while not rospy.is_shutdown():
        x+=1
        msg = Float32MultiArray()
        msg.data = [x,2.0,32.8,4.0,5.0,48.0]
        pub.publish(msg)
        rospy.loginfo(str(msg.data) +' Send')
        rate.sleep()

    rospy.loginfo('Node was stopped')