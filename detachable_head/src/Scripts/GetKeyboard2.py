#!/usr/bin/env python

import keyboard as ky
import rospy
import time
from std_msgs.msg import String

def get():
    key = ''
    
    if ky.is_pressed('up'):
        key = 'up'
    elif ky.is_pressed('down'):
        key = 'down'
    elif ky.is_pressed('left'):
        key = 'left'
    elif ky.is_pressed('right'):
        key = 'right'
    elif ky.is_pressed('space'):
        key = 'space'
    elif ky.is_pressed('q'):
        key = 'q'
    return key
    

def main():
    rospy.init_node('kb_node')
    pub = rospy.Publisher('kb_val', String, queue_size=10)
    while not rospy.is_shutdown():
        key= get()
        print(key)
        if key == 'q': break
        
        
        
        
    print('Quit keyboard node')

if __name__=='__main__':
        main()