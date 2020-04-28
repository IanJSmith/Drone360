# Drone360
Using Gazebo to simulate a multi-agent drone system to stitch a 360deg image of an room

To launch a single drone:
roslaunch drone_gazebo drone.launch

To launch two drones:
roslaunch drone_gazebo drone_double.launch

To run a single ring around the room (only works for one drone):
rosrun drone_gazebo drone_ring.py

To run several ascending rings around the room (works for either one or two drones):
rosrun drone_gazebo drone_layers.py

If one wants to run a single ring with two drones, use the above drone_layers.py but change "room_height" in line 49

To play a recorded rosbag (image_bag) and record a single lap:
1. In one terminal, start roscore
roscore
2. In another terminal, run the following command (image_view package must be downloaded):
rosrun image_view extract_images _sec_per_frame:=0.1 image:=/drone_1_lap_1
3. In a final terminal, run the following command:
rosbag play image_bag

Change /drone_1_lap_1 to whatever lap or topic to record that topic
