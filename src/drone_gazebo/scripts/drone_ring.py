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

def drone_ring(self):

	global x, y, z, roll, pitch, yaw, namespace, count

	if count == 1:
		x = 5
		y = -0.75
		z = 0.1
		yaw = 0
		count = count + 1

	elif count == 2:
		y = -0.5
		count = count + 1
	elif count < 15:
		y = y + 0.5
		count = count + 1
	elif count == 15:
		yaw = 1.57
		count = count + 1
	elif count < 25:
		x = x - 0.5
		count = count + 1
	elif count == 25:
		yaw = 3.14
		count = count + 1
	elif count < 38:
		y = y - 0.5
		count = count + 1
	elif count == 38:
		y = -0.75
		count = count + 1
	elif count == 39:
		yaw = -1.57
		count = count + 1
	elif count < 49:
		x = x + 0.5
		count = count + 1
	elif count == 49:
		count = 1
	# elif count == 2:
	# 	y = -0.5
	# 	count = 3
	# elif count == 3:
	# 	y = 0
	# 	count = 4
	# elif count == 4:
	# 	y = 0.5
	# 	count = 5
	# elif count == 5:
	# 	y = 1
	# 	count = 6
	# elif count == 6:
	# 	y = 1.5
	# 	count = 7
	# elif count == 7:
	# 	y = 2
	# 	count = 8
	# elif count == 8:
	# 	y = 2.5
	# 	count = 9
	# elif count == 9:
	# 	y = 3
	# 	count = 10
	# elif count == 10:
	# 	y = 3.5
	# 	count = 11
	# elif count == 11:
	# 	y = 4
	# 	count = 12
	# elif count == 12:
	# 	y = 4.5
	# 	count = 13
	# elif count  == 13:
	# 	y = 5
	# 	count = 14
	# elif count == 14:
	# 	y = 5.5
	# 	count = 15
	# elif count == 15:
	# 	x = 4.5
	# 	yaw = 1.57
	# 	count = 16
	# elif count == 16:
	# 	x = 4
	# 	count = 17
	# elif count == 17:
	# 	x = 3.5
	# 	count = 18
	# elif count == 18:
	# 	x = 3
	# 	count = 19
	# elif count == 19:
	# 	x = 2.5
	# 	count = 20
	# elif count == 20:
	# 	x = 2
	# 	count = 21
	# elif count == 21:
	# 	x = 1.5
	# 	count = 22
	# elif count == 22:
	# 	x = 1
	# 	count = 23
	# elif count == 23:
	# 	x = 0.5
	# 	count = 24

	# elif count == 24:
	# 	yaw = 3.14
	# 	count = 25

	# elif count == 25:
	# 	y = 5
	# 	count = 26
	# elif count == 26:
	# 	y = 4.5
	# 	count = 27
	# elif count == 27:
	# 	y = 4
	# 	count = 28
	# elif count == 29:
	# 	y = 3.5
	# 	count = 30
	# elif count == 30:
	# 	y = 3
	# 	count = 31
	# elif count == 31:
	# 	y = 2.5
	# 	count = 32
	# elif count == 32:
	# 	y = 2
	# 	count = 33
	# elif count == 33:
	# 	y = 1.5
	# 	count = 34
	# elif count == 34:
	# 	y = 1
	# 	count = 35
	# elif count == 35:
	# 	y = 0.5
	# 	count = 36
	# elif count == 36:
	# 	y = 0
	# 	count = 37
	# elif count == 37:
	# 	y = -0.5
	# 	count = 38
	# elif count == 38:
	# 	y = -0.75
	# 	count = 39

	# elif count == 39:
	# 	yaw = -1.57
	# 	count = 40

	# elif count == 40:
	# 	x = 1
	# 	count = 41
	# elif count == 41:
	# 	x = 1.5
	# 	count = 42
	# elif count == 42:
	# 	x = 2
	# 	count = 43
	# elif count == 43:
	# 	x = 2.5
	# 	count = 44
	# elif count == 44:
	# 	x = 3
	# 	count = 45
	# elif count == 45:
	# 	x = 3.5
	# 	count = 46
	# elif count == 46:
	# 	x = 4
	# 	count = 47
	# elif count == 47:
	# 	x = 4.5
	# 	count = 48
	# elif count == 48:
	# 	x = 5
	# 	count = 1



	teleport(namespace, x, y, z, roll, pitch, yaw)

if __name__ == '__main__':
    try:
    	rospy.init_node('determine_pose')
        rospy.Timer(rospy.Duration(0.5), drone_ring)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass