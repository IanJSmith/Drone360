#!/usr/bin/env python

from drone_teleport import teleport
import rospy, sys
from gazebo_msgs.msg import ModelState
from std_msgs.msg import Float64MultiArray, Float32
from geometry_msgs.msg import Pose
from tf.transformations import euler_from_quaternion

x = 0
y = 0
z = 0
roll = 0
pitch = 0
yaw = 0
namespace = 'drone'
count = 1

def move_drone_callback(self):

	global x, y, z, roll, pitch, yaw, namespace, count	

	#Once matlab script to define points of helix etc is running, get target pose using subscriber instead of timer

	if count == 1:
		x = 2.5
		y = 2.5
		z = 0.1
		roll = 0
		pitch = 0
		yaw = 0
		count = 2
	elif count == 2:
		x = 2.5
		y = 2.7
		z = 0.1
		roll = 0
		pitch = 0
		yaw = 0
		count = 3
	elif count == 3:
		x = 2.5
		y = 2.9
		z = 0.1
		roll = 0
		pitch = 0
		yaw = 0
		count = 4
	elif count == 4:
		x = 2.5
		y = 2.9
		z = 0.3
		roll = 0
		pitch = 0
		yaw = 0
		count = 5
	elif count == 5:
		x = 2.5
		y = 2.7
		z = 0.3
		roll = 0
		pitch = 0
		yaw = 0
		count = 6
	elif count == 6:
		x = 2.5
		y = 2.5
		z = 0.3
		roll = 0
		pitch = 0
		yaw = 0
		count = 1

	teleport(namespace, x, y, z, roll, pitch, yaw)

if __name__ == '__main__':
    try:
    	rospy.init_node('determine_pose')
        rospy.Timer(rospy.Duration(0.25), move_drone_callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass