#!/usr/bin/env python
#---------------------------------------------------
from drone_pid import PID
import rospy
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Float64MultiArray, Float32
from geometry_msgs.msg import Pose
from tf.transformations import euler_from_quaternion
#---------------------------------------------------
def control_drone(msg, args):
	#Declare global variables as you dont want these to die, reset to zero and then re-initiate when the function is called again.
	global roll_1, pitch_1, yaw_1, err_roll_1, err_pitch_1, err_yaw_1
	
	#Assign the Float64MultiArray object to 'f_1' as we will have to send data of motor velocities to gazebo in this format
	f_1 = Float64MultiArray()
	f_2 = Float64MultiArray()
	
	#Convert the quaternion data to roll_1, pitch_1, yaw_1 data
	#The model_states contains the position, orientation, velocities of all objects in gazebo. In the simulation, there are objects like: ground, Contruction_cone, 
	#quadcopter (named as 'drone') etc. So 'msg.pose[ind]' will access the 'drone' object's pose information i.e the quadcopter's pose.
	ind = msg.name.index('drone_1')
	orientationObj = msg.pose[ind].orientation
	orientationList = [orientationObj.x, orientationObj.y, orientationObj.z, orientationObj.w]
	(roll_1, pitch_1, yaw_1) = (euler_from_quaternion(orientationList))

	ind = msg.name.index('drone_2')
	orientationObj = msg.pose[ind].orientation
	orientationList = [orientationObj.x, orientationObj.y, orientationObj.z, orientationObj.w]
	(roll_2, pitch_2, yaw_2) = (euler_from_quaternion(orientationList))
	
	#send roll_1, pitch_1, yaw_1 data to PID() for attitude-stabilisation, along with 'f_1', to obtain 'fUpdated_1'
	#Alternatively, you can add your 'control-file' with other algorithms such as Reinforcement learning, and import the main function here instead of PID().
	(fUpdated_1, err_roll_1, err_pitch_1, err_yaw_1) = PID(roll_1, pitch_1, yaw_1, f_1)
	(fUpdated_2, err_roll_2, err_pitch_2, err_yaw_2) = PID(roll_2, pitch_2, yaw_2, f_2)
	
	#The object args contains the tuple of objects (velPub, err_rollPub, err_pitchPub, err_yawPub. publish the information to namespace.
	args[0].publish(fUpdated_1)
	args[1].publish(err_roll_1)
	args[2].publish(err_pitch_1)
	args[3].publish(err_yaw_1)
	args[4].publish(fUpdated_2)
	args[5].publish(err_roll_2)
	args[6].publish(err_pitch_2)
	args[7].publish(err_yaw_2)
	#print("Roll_1: ",roll_1*(180/3.141592653),"Pitch_1: ", pitch_1*(180/3.141592653),"Yaw_1: ", yaw_1*(180/3.141592653))
	#print(orientationObj)
#----------------------------------------------------

#Initiate the node that will control the gazebo model
rospy.init_node("Control")

#initiate publishers that publish errors (roll_1, pitch_1,yaw_1 - setpoint) so that it can be plotted via rqt_plot /err_<name>  
err_rollPub_1 = rospy.Publisher('err_roll_1', Float32, queue_size=1)
err_pitchPub_1 = rospy.Publisher('err_pitch_1', Float32, queue_size=1)
err_yawPub_1 = rospy.Publisher('err_yaw_1', Float32, queue_size=1)
err_rollPub_2 = rospy.Publisher('err_roll_2', Float32, queue_size=1)
err_pitchPub_2 = rospy.Publisher('err_pitch_2', Float32, queue_size=1)
err_yawPub_2 = rospy.Publisher('err_yaw_2', Float32, queue_size=1)

#initiate publisher velPub that will publish the velocities of individual BLDC motors
velPub_1 = rospy.Publisher('/drone_1/joint_motor_controller/command', Float64MultiArray, queue_size=4)
velPub_2 = rospy.Publisher('/drone_2/joint_motor_controller/command', Float64MultiArray, queue_size=4)

#Subscribe to /gazebo/model_states to obtain the pose in quaternion form
#Upon receiveing the messages, the objects msg, velPub, err_rollPub, err_pitchPub and err_yawPub are sent to "control_drone" function.
PoseSub = rospy.Subscriber('/gazebo/model_states',ModelStates,control_drone,(velPub_1, err_rollPub_1, err_pitchPub_1, err_yawPub_1, velPub_2, err_rollPub_2, err_pitchPub_2, err_yawPub_2))

rospy.spin()
