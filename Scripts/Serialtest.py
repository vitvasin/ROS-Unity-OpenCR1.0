#!/usr/bin/env python

import serial
import time
pass_cmd =''
pre_cmd = ''


def serial_connection():
    global pass_cmd,pre_cmd

    opencr = serial.Serial('/dev/ttyACM0', 57600)
    
    x = True
    linact =0
    while opencr.isOpen():
        print(str(linact))  

        pass_cmd = "S,512,512,512,512,512," + str(linact)+",F" + '\n'
        opencr.write(pass_cmd.encode()) #S,1000,1000,512,512,512,512,F is the command protocal
        
        if x == True:
            linact +=100
            if linact >=1023:
                x= False
        else:
            linact -=100
            if linact <=0:
                x =True
        time.sleep(0.008)
                
    opencr.close()

    



if __name__ == '__main__':
    serial_connection()
