#!/usr/bin/env python

# A script to run a single drone around a single ring of the room

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
	
	# Moves along the first wall from y = -0.25 to y = 5.25, then rounds corner
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

	# Moves along the second wall from x = 4.5 to x = 0.75, then rounds corner
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

	# Moves along the third wall from y = 5.25 to y = -0.5, then rounds corner
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

	# Moves along the fourth wall from x = 0.75 to x = 4.5, then rounds corner
	# This one just goes for one loop, and closes the bag
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