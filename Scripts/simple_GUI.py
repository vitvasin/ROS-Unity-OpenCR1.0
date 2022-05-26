#!/usr/bin/env python

import rospy
import Tkinter as tk

if __name__ == '__main__':
    rospy.init_node('GUI')
    window = tk.Tk()
    window.title('GUI_test')
    window.minsize(width=400,height=400)

    window.mainloop()