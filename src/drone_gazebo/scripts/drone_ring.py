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
wall = 1
reset = 1

def drone_ring(self):

	global x, y, z, roll, pitch, yaw, namespace, wall, reset

	if reset > 0:
		x = 5
		y = -0.75
		z = 0.1
		yaw = 0
		reset = 0

	elif wall == 1:
		if y > 5.45:
			yaw = 1.57
			wall = 2
		elif y < 5.45:
			y = y + 0.05

	elif wall == 2:
		if x < 0.55:
			yaw = 3.14
			wall = 3
		elif x > 0.55:
			x = x - 0.05

	elif wall == 3:
		if y < -0.70:
			yaw = -1.57
			wall = 4
		elif y > -0.70:
			y = y - 0.05

	elif wall == 4:
		if x < 4.95:
			x = x + 0.05

	else:
		reset = 1

	



	teleport(namespace, x, y, z, roll, pitch, yaw)

if __name__ == '__main__':
    try:
    	rospy.init_node('determine_pose')
        rospy.Timer(rospy.Duration(0.1), drone_ring)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass