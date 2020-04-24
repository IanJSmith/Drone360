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
flip = False

drone_1_topic = 'drone_1'
drone_2_topic = 'drone_2'
drone_1_lap = 1
drone_2_lap = 1

drone_image = Image()
drone_image_1 = Image()
drone_image_2 = Image()
bag = rosbag.Bag('image_bag', 'w') 

def image_callback(Image):

	global drone_image

	drone_image = Image

def image1_callback(Image):

	global drone_image_1

	drone_image_1 = Image

def image2_callback(Image):

	global drone_image_2

	drone_image_2 = Image

def drone_ring(namespace):
	
	global x, y, z, roll, pitch, yaw, wall, count, lap, drone_image, bag, flip
	global x_1, y_1, z_1, yaw_1, wall_1, count_1, lap_1, drone_image_1
	global x_2, y_2, z_2, yaw_2, wall_2, count_2, lap_2, drone_image_2
	global drone_topic, drone_1_topic, drone_2_topic

	if namespace == 'drone':
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
					wall = 1
					count = 0
					lap = 1
				else:
					yaw = yaw + corner_tick
					count = count + 1

		teleport(namespace, x, y, z, roll, pitch, yaw)
		bag.write(drone_topic, drone_image)

	if namespace == 'drone_1':
		if flip == False:	
			if wall_1 == 1:
				if y_1 > 5.2:
					if count_1 == 20:
						wall_1 = 2
						count_1 = 0
					elif count_1 < 20:
						yaw_1 = yaw_1 + corner_tick
						count_1 = count_1 + 1
				else:
					y_1 = y_1 + movement_increment

			elif wall_1 == 2:
				if x_1 < 0.80:
					if count_1 == 20:
						lap_1 = 1
						wall_1 = 3
					elif count_1 < 20:
						yaw_1 = yaw_1 + corner_tick
						count_1 = count_1 + 1
						
				else:
					x_1 = x_1 - movement_increment

		elif flip == True:
			if wall_1 == 3:
				if y_1 < -0.45:
					if count_1 == 20:
						wall_1 = 4
						count_1 = 0
					else:
						yaw_1 = yaw_1 + corner_tick
						count_1 = count_1 + 1
				else:
					y_1 = y_1 - movement_increment

			elif wall_1 == 4:
				if x_1 < 4.45:
					x_1 = x_1 + movement_increment
				else:
					if count_1 == 20:
						lap_1 = 1
						wall_1 = 1
					else:
						yaw_1 = yaw_1 + corner_tick
						count_1 = count_1 + 1

		teleport(namespace, x_1, y_1, z_1, roll, pitch, yaw_1)
		bag.write(drone_1_topic, drone_image_1)

	if namespace == 'drone_2':
		if flip == False:
			if wall_2 == 3:
				if y_2 < -0.45:
					if count_2 == 20:
						wall_2 = 4
						count_2 = 0
					else:
						yaw_2 = yaw_2 + corner_tick
						count_2 = count_2 + 1
				else:
					y_2 = y_2 - movement_increment

			elif wall_2 == 4:
				if x_2 < 4.45:
					x_2 = x_2 + movement_increment
				else:
					if count_2 == 20:
						lap_2 = 1
						wall_2 = 1
					else:
						yaw_2 = yaw_2 + corner_tick
						count_2 = count_2 + 1

		elif flip == True:
			if wall_2 == 1:
				if y_2 > 5.2:
					if count_2 == 20:
						wall_2 = 2
						count_2 = 0
					elif count_2 < 20:
						yaw_2 = yaw_2 + corner_tick
						count_2 = count_2 + 1
				else:
					y_2 = y_2 + movement_increment

			elif wall_2 == 2:
				if x_2 < 0.80:
					if count_2 == 20:
						lap_2 = 1
						wall_2 = 3
					elif count_2 < 20:
						yaw_2 = yaw_2 + corner_tick
						count_2 = count_2 + 1
						
				else:
					x_2 = x_2 - movement_increment

		teleport(namespace, x_2, y_2, z_2, roll, pitch, yaw_2)
		bag.write(drone_2_topic, drone_image_2)

def drone_layer(self):

	global x, y, z, roll, pitch, yaw, namespace, wall, count, lap, flip, bag
	global x_1, y_1, z_1, yaw_1, wall_1, count_1, lap_1
	global x_2, y_2, z_2, yaw_2, wall_2, count_2, lap_2
	global drone_lap, drone_1_lap, drone_2_lap, drone_topic, drone_1_topic, drone_2_topic

	drones = rospy.get_param('drone_number')

	if drones == 1:
		if z > 3:
			z = 0.1

		elif lap == 1:
			# bag.close()
			drone_lap = drone_lap + lap
			drone_topic = 'drone_lap_' + str(drone_lap)
			lap = 0
			z = z + 0.1
			drone_ring('drone')


		else:
			drone_ring('drone')

	if drones == 2:
		if z_1 > 3 and z_2 > 3:
			z_1 = 0.1
			z_2 = 0.1
			bag.close()

		elif lap_1 == 1 and lap_2 == 1:
			# bag.close()
			drone_1_lap = drone_1_lap + lap_1
			drone_1_topic = 'drone_1_lap_' + str(drone_1_lap)
			drone_2_lap = drone_2_lap + lap_2
			drone_2_topic = 'drone_2_lap_' + str(drone_2_lap)
			lap_1 = 0
			lap_2 = 0
			count_1 = 0
			count_2 = 0
			flip = not flip
			z_1 = z_1 + 0.5
			z_2 = z_2 + 0.5
			drone_ring('drone_1')
			drone_ring('drone_2')

		else:
			drone_1_topic = 'drone_1_lap_' + str(drone_1_lap)
			drone_2_topic = 'drone_2_lap_' + str(drone_2_lap)
			drone_ring('drone_1')
			drone_ring('drone_2')






if __name__ == '__main__':
    try:
    	rospy.init_node('determine_pose')
    	drone_number = rospy.get_param('drone_number')
        rospy.Timer(rospy.Duration(0.1), drone_layer)
        if drone_number == 1:
        	rospy.Subscriber("drone/camera1/image_raw", Image, image_callback)
        elif drone_number == 2:
        	rospy.Subscriber("drone_1/camera1/image_raw", Image, image1_callback)
        	rospy.Subscriber("drone_2/camera1/image_raw", Image, image2_callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass