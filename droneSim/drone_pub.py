#! /usr/bin/env python

#------------ Publisher Node -------------#
#### To run: "rosrun my_new_topic drone_pub.py"
## open new shell: 'rostopic list' -> '/my_new_topic' should be shown
####### THIS WILL RUN ROS: 'rostopic echo /my_new_topic'
# Pointing to the interpreter to use

    # Import ros-python
import rospy
    # Import positioning
from geometry_msgs.msg import Pose

# Create new ros topic
rospy.init_node('new_topic')

my_pub = rospy.Publisher('/my_new_topic', Pose, queue_size=10)

# 'rosmsg show Pose' will show:
    # Position variables
    # Position: x,y,z
pose_msg = Pose()
pose_msg.position.x = 0
pose_msg.position.y = 0
pose_msg.position.z = 0


# We will go through the loop 30 times per second
# as long as processing time doesn't exceed 1/30th of a second
rate = rospy.Rate(30)

while not rospy.is_shutdown():
    my_pub.publish(pose_msg)
    rate.sleep()
    # increment positions by one **for testing**
    pose_msg.position.x += 1
    pose_msg.position.y += 1
    pose_msg.position.z += 1
    # This loop will continue until ctrl-c

#----------- Subscriber Node ------------#
# Will recieve and display data from the publisher node
# This will be a separate file

# If we want to launch the publisher and subscriber:
# ---- In a .launch file:
#
# <launch>
# <node name = "drone_pub" pkg = "my_new_topic" type = "drone_pub.py" output = "screen" />
# <node name = "drone_sub" pkg = "my_new_topic" type = "drone_sub.py" output = "screen" />
# </launch>
