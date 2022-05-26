#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray, Bool


class HubNode():
    count=0

    def __init__(self):
        self.sub = rospy.Subscriber('/head_command', Float32MultiArray, self.callback)
        self.pub = rospy.Publisher('hand_flag', Float32MultiArray, queue_size=10)
        self.pub2 = rospy.Publisher('gripper', Bool, queue_size=10)


    def Gripper(self, data):
        self.pub2.publish(data)

    def Publisher(self, data):
        self.pub.publish(data)

    def callback(self, data):
        if data.data[20]==1:
            self.Gripper(True)
        else:
            self.Gripper(False)
            
        #if self.count>=1: #original 50
        self.Publisher(data)
            #self.Gripper(data) # pass gripper state


        #    self.count=0
        #else:
        #    self.count+=1


        #return data

if __name__ == '__main__':
    rospy.init_node('hub_node')
    node = HubNode()

    while not rospy.is_shutdown():
        rospy.sleep(0)
