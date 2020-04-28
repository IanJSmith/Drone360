#!/usr/bin/env python

# This file is used to drive one or two drones in layers of rectangles (rings) around
# a predetermined path in a room

# NOTE: To export the rosbag once done collecting run IN ORDER:
# - In one terminal start roscore
# - In another terminal in a temp folder inside youre workspace run
# 	"rosrun image_view extract_images _sec_per_fram:=0.1 image:=/drone_1_lap_1" (or whichever lap you want to pull)
# - In another terminal run "rosbag play image_bag"

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

# Controls how fine the movement and corner turn is
corner_tick = 0.0785
movement_increment = 0.05
room_height = 3

# flip is used to toggle what state each of the dual drones are in
# A ring is determined as four walls:
# In state 1 (flip = false) drone 1 moves along walls 1 and 2, drone 2 moves along walls 3 and 4
# In state 2 (flip = true) drone 1 moves along walls 3 and 4, drone 2 moves along walls 1 and 2
flip = False

# Drone topics and laps used to dynamically change what topics the image writes to in rosbag
# i.e. the first half ring of drone_1 is "drone_1_lap_1" in the rosbag, second half ring is "drone_1_lap_2" etc
# simplifies the extraction process
drone_topic = 'drone_'
drone_lap = 1
drone_1_topic = 'drone_1'
drone_2_topic = 'drone_2'
drone_1_lap = 1
drone_2_lap = 1

drone_image = Image()
drone_image_1 = Image()
drone_image_2 = Image()
bag = rosbag.Bag('image_bag', 'w') 

# Callbacks to set the drone's camera feed to a temp "drone_image" variable for one or double drones
# in order to write to rosbag
def image_callback(Image):

	global drone_image

	drone_image = Image

def image1_callback(Image):

	global drone_image_1

	drone_image_1 = Image

def image2_callback(Image):

	global drone_image_2

	drone_image_2 = Image

# Passing the namespace allows drone_ring to handle both single and double drone setup
# drone_ring increments drone around walls and around corners, and writes the immediate drone_image to the rosbag
def drone_ring(namespace):
	
	# Single drone setup
	global x, y, z, roll, pitch, yaw, wall, count, lap, drone_image, bag, flip

	# Double drone setup
	global x_1, y_1, z_1, yaw_1, wall_1, count_1, lap_1, drone_image_1
	global x_2, y_2, z_2, yaw_2, wall_2, count_2, lap_2, drone_image_2

	# drone topics to write to in rosbag
	global drone_topic, drone_1_topic, drone_2_topic

	########################## SINGLE DRONE ################################

	if namespace == 'drone':
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

		# Moves along the fourth wall from x = 0.75 to x = 4.5, then rounds corner, and resets
		# The lap variable is used in drone_layers to increment height
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

		# Teleport function uses xyz rpy to set model state
		# This was used because current pkg only has PID control and no reliable movement controls
		teleport(namespace, x, y, z, roll, pitch, yaw)
		# Writes the current image from camera to the current lap topic in image_bag
		bag.write(drone_topic, drone_image)

	########################################################################


	########################## DOUBLE DRONE ################################

	if namespace == 'drone_1':
		# Checks to see which of two paths the drone is currently on
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
		# Checks to see which of two paths the drone is currently on
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

	########################################################################


def drone_layer(self):

	# Single Drone setup
	global x, y, z, roll, pitch, yaw, namespace, wall, count, lap, flip, bag, room_height
	# Double Drone setup
	global x_1, y_1, z_1, yaw_1, wall_1, count_1, lap_1
	global x_2, y_2, z_2, yaw_2, wall_2, count_2, lap_2
	global drone_lap, drone_1_lap, drone_2_lap, drone_topic, drone_1_topic, drone_2_topic

	# Get number of drones from launch file to decide whether to use single drone or double drone setup
	drones = rospy.get_param('drone_number')

	if drones == 1:
		# If over the max height of room, reset the height and close the bag
		if z > room_height:
			z = 0.1
			bag.close()

		# Otherwise after every consecutive lap (a full ring) increment the drone_lap / topic, and run drone_ring
		elif lap == 1:
			drone_lap = drone_lap + lap
			drone_topic = 'drone_lap_' + str(drone_lap)
			lap = 0
			z = z + 0.1
			drone_ring('drone')

		# Initial run when a lap hasn't been completed yet
		else:
			drone_ring('drone')

	if drones == 2:
		# Waits for both drones to reach max height (they wont be concurrent), resets the height and closes the bag
		if z_1 > room_height and z_2 > room_height:
			z_1 = 0.1
			z_2 = 0.1
			bag.close()

		# Otherwise after both drones reach their next lap (half-rings), increment topics and run drone_ring for each drone
		elif lap_1 == 1 and lap_2 == 1:
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

		# Initial run before either drone completes a lap
		else:
			drone_1_topic = 'drone_1_lap_' + str(drone_1_lap)
			drone_2_topic = 'drone_2_lap_' + str(drone_2_lap)
			drone_ring('drone_1')
			drone_ring('drone_2')






if __name__ == '__main__':
    try:
    	rospy.init_node('determine_pose')
    	# Get number of drones from launch file to determine single or double drone setup
    	drone_number = rospy.get_param('drone_number')
    	# A timer that calls the drone_layer function every 100ms, meaning each drone moves and sends a frame to rosbag every 100ms
        rospy.Timer(rospy.Duration(0.1), drone_layer)
        if drone_number == 1:
        	rospy.Subscriber("drone/camera1/image_raw", Image, image_callback)
        elif drone_number == 2:
        	rospy.Subscriber("drone_1/camera1/image_raw", Image, image1_callback)
        	rospy.Subscriber("drone_2/camera1/image_raw", Image, image2_callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass