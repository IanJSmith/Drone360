#!/usr/bin/env python

import rospy, sys

from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from tf.transformations import quaternion_from_euler

def teleport(drone_name, x, y, z, roll, pitch, yaw):

    quaternion = quaternion_from_euler(roll,pitch,yaw)

    state_msg = ModelState()
    state_msg.model_name = drone_name
    state_msg.pose.position.x = x
    state_msg.pose.position.y = y
    state_msg.pose.position.z = z
    state_msg.pose.orientation.x = quaternion[0]
    state_msg.pose.orientation.y = quaternion[1]
    state_msg.pose.orientation.z = quaternion[2]
    state_msg.pose.orientation.w = quaternion[3]

    rospy.wait_for_service('/gazebo/set_model_state')
    try:
        set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        resp = set_state( state_msg )

    except rospy.ServiceException, e:
        print "Service call failed: %s" % e

if __name__ == '__main__':
    try:
    	rospy.init_node('set_pose')
    	namespace = 'drone'
    	x = 0
    	y = 0
    	z = 0.3
    	roll = 0
    	pitch = 0
    	yaw = 0
        teleport(namespace, x, y, z, roll, pitch, yaw)
    except rospy.ROSInterruptException:
        pass