import os
import time
import sys
from pymycobot.mycobot import MyCobot

sys.path.append(os.path.dirname(__file__))
from port_setup import setup


def gripper_test(mc):
    print("Start check IO part of api\n")
    # print()

    flag = mc.is_gripper_moving()
    print("Is gripper moving: {}".format(flag))
    time.sleep(1)

    # Set the current position to (2048).
    # Use it when you are sure you need it.
    # Gripper has been initialized for a long time. Generally, there
    # is no need to change the method.
    #mc.set_gripper_ini()

    mc.set_encoder(7, 2000)
    time.sleep(2)
    mc.set_encoder(7, 1300)
    time.sleep(2)
    mc.set_encoder(7, 2000)
    time.sleep(2)
    # set_gripper_value has some bug, just can close.
    #mc.set_gripper_value(100, 70)
    #time.sleep(3)
    #mc.set_gripper_value(0, 70)
    #time.sleep(3)

    #mc.set_gripper_state(0, 70)
    #time.sleep(3)
    #mc.set_gripper_state(1, 70)
    #time.sleep(3)

    print("")
    print(mc.get_gripper_value())


if __name__ == "__main__":
    mycobot = setup()
    gripper_test(mycobot)
