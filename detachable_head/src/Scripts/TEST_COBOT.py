#!/usr/bin/env python
import subprocess
import serial.tools.list_ports
from pymycobot import MyCobot
import time,os
### CHECK the Serial connection of mycobot
#

while 1:
    #x = subprocess.call('ls /dev/Mycobot',capture_output=True)
    #x = os.system('ls /dev/Mycobot')
    x = os.path.exists('/dev/Mycobot')
    if x==1:
        print('connected')
    else:
        print('disconnected')
    time.sleep(1)


