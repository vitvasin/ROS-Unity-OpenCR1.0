#!/usr/bin/env python3

import sys,tty,os,termios
import rospy
from std_msgs.msg import Float32MultiArray, Bool, String
def getkey():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            b = os.read(sys.stdin.fileno(), 3).decode()
            if len(b) == 3:
                k = ord(b[2])
            else:
                k = ord(b)
            key_mapping = {
                127: 'backspace',
                10: 'return',
                32: 'space',
                9: 'tab',
                27: 'esc',
                65: 'up',
                66: 'down',
                67: 'right',
                68: 'left'
            }
            return key_mapping.get(k, chr(k))
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

''''''
def main():
    rospy.init_node('kb_node')
    kb_pub = rospy.Publisher("/key_pub",String,queue_size=1)
    try:
        while not rospy.is_shutdown():
            k = getkey()
            if k == 'esc':
                quit()
            else:
                print(k)
                kb_pub.publish(k)
                
    except (KeyboardInterrupt, SystemExit):
        os.system('stty sane')
        print('stopping.')
        ''''''
        
        
if __name__=='__main__':
    main()