#!/usr/bin/env python

from drone_teleport import teleport
import rospy, sys, rosbag
from gazebo_msgs.msg import ModelState
from sensor_msgs.msg import Image

# Single Drone Start
x = 4.5
y = -0.25
z = 0.1
roll = 0
pitch = 0
yaw = 0
wall = 1
count = 0
lap = 0

# Drone_1 Start
x_1 = 4.5
y_1 = -0.25
z_1 = 0.1
yaw_1 = 0
wall_1 = 1
count_1 = 0
lap_1 = 0

# Drone_2 Start
x_2 = 0.75
y_2 = 5.25
z_2 = 0.1
yaw_2 = 3.14
wall_2 = 3
count_2 = 0
lap_2 = 0

namespace = 'drone'
corner_tick = 0.0785
movement_increment = 0.05 

drone_image = Image()
bag = rosbag.Bag('image_bag', 'w')

def image_callback(Image):

	global drone_image

	drone_image = Image

def drone_ring_callback(self):

	global x, y, z, roll, pitch, yaw, namespace, wall, count, lap, drone_image, bag

	if wall == 1:
		if y > 5.2:
			if count == 20:
				wall = 2
				count = 0
			else:
				yaw = yaw + corner_tick
				count = count + 1
		elif y < 5.2:
			y = y + movement_increment

	elif wall == 2:
		if x < 0.80:
			if count == 20:
				wall = 3
				count = 0
			else:
				yaw = yaw + corner_tick
				count = count + 1
		elif x > 0.80:
			x = x - movement_increment

	elif wall == 3:
		if y < -0.45:
			if count == 20:
				wall = 4
				count = 0
			else:
				yaw = yaw + corner_tick
				count = count + 1
		elif y > -0.45:
			y = y - movement_increment

	elif wall == 4:
		if x < 4.45:
			x = x + movement_increment
		else:
			if count == 20:
				# wall = 1
				count = 0
				lap = lap + 1
				bag.close()
			else:
				yaw = yaw + corner_tick
				count = count + 1


	teleport(namespace, x, y, z, roll, pitch, yaw)
	bag.write('/drone', drone_image)

if __name__ == '__main__':
    try:
    	rospy.init_node('determine_pose')
        rospy.Timer(rospy.Duration(0.1), drone_ring_callback)
        rospy.Subscriber("drone/camera1/image_raw", Image, image_callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass