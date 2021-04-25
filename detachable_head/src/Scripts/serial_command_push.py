#!/usr/bin/env python
import rospy
import serial
import time
from std_msgs.msg import String

pass_cmd="Home\n"
pre_cmd =""
def callback_receive_cmd(msg):
    global pass_cmd
    pass_cmd = msg.data +'\n'


def serial_connection():
    global pass_cmd,pre_cmd
    rospy.init_node('serial_command_push')
    sub = rospy.Subscriber('/head_waist_motor_cmd',String, callback_receive_cmd) ## listen to same TOPIC
    
    rate = rospy.Rate(100) #100 Hz

    while not rospy.is_shutdown():
        opencr = serial.Serial('/dev/ttyACM0', 9600)
        rospy.loginfo(opencr.name + ' Serial_connected')
        x = True
        while opencr.isOpen():

            if pre_cmd != pass_cmd:
                opencr.write(pass_cmd.encode()) #S,1000,1000,512,512,512,512,F is the command protocal
                pre_cmd = pass_cmd

            
            #time.sleep()
            rate.sleep()
        opencr.close()

    rospy.spin()



if __name__ == '__main__':
    try:
        serial_connection()
    except rospy.ROSInterruptException:
        pass