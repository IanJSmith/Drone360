#!/usr/bin/env python

from drone_teleport import teleport
import rospy, sys, rosbag
from gazebo_msgs.msg import ModelState
from sensor_msgs.msg import Image

x = 2.5
y = 2.25
z = 0.1
roll = 0
pitch = 0
yaw = 0
namespace = 'drone'
wall = 1
count = 0
lap = 0
lap_1 = 0
lap_2 = 0
drone_image = Image()
bag = rosbag.Bag('image_bag', 'w')

def image_callback(Image):

	global drone_image

	drone_image = Image

# def drone_ring(namespace, x, y, z, roll, pitch, yaw, lap):
# 	global 

def drone_ring_callback(self):

	global x, y, z, roll, pitch, yaw, namespace, wall, count, lap, drone_image, bag

	if yaw < 6.28:
		yaw = yaw + 0.087265

	else:
		yaw = 0

	teleport(namespace, x, y, z, roll, pitch, yaw)
	bag.write('/drone', drone_image)

if __name__ == '__main__':
    try:
    	rospy.init_node('determine_pose')
        rospy.Timer(rospy.Duration(0.01), drone_ring_callback)
        rospy.Subscriber("drone/camera1/image_raw", Image, image_callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass