#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import WrenchStamped
from std_msgs.msg import Float64
from filterpy.kalman import ExtendedKalmanFilter
import numpy as np
from collections import deque

def HJacobian_at(x):
    """ compute Jacobian of H matrix at x """
    return np.array([[1]])

def hx(x):
    """ compute measurement for slant range that would correspond to state x.
    """
    return np.array([x[0]])

class ZForceFilter:
    def __init__(self, window_size=10):
        # Initialize Extended Kalman Filter
        self.ekf = ExtendedKalmanFilter(dim_x=1, dim_z=1)
        self.ekf.x = np.array([0])  # Initial state
        self.ekf.F = np.array([[1]])  # State transition matrix
        self.ekf.P *= 1  # Covariance matrix
        self.ekf.R = 0.1  # Measurement noise
        self.ekf.Q = 0.1  # Process noise

        # Initialize moving average variables
        self.window_size = window_size
        self.data_window = deque(maxlen=self.window_size)
        
        rospy.init_node('z_force_filter_node', anonymous=True)
        
        self.subscriber = rospy.Subscriber('/leptrino_force_torque/force_torque', WrenchStamped, self.callback)
        self.publisher = rospy.Publisher('/filtered_z_force', Float64, queue_size=10)

    def callback(self, data):
        # Extended Kalman Filter update
        self.ekf.predict()
        self.ekf.update(np.array([data.wrench.force.z]), HJacobian=HJacobian_at, Hx=hx)

        # Moving average post-processing
        self.data_window.append(self.ekf.x[0])
        filtered_data = sum(self.data_window) / len(self.data_window)
        
        self.publisher.publish(filtered_data)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    filter_node = ZForceFilter()
    filter_node.run()
