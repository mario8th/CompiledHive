#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that listens to std_msgs/Strings published
## to the 'chatter' topic

import rospy
from std_msgs.msg import String
import ast
import math

REFRESHRATE = 2

#Class to hold math info for simulator
class Siminfo:
    def __init__(self, speedMax):
        self.currentLocs = []
        self.vectors = []
        self.speedMax = speedMax
        self.dest = []
        self.refreshRate = REFRESHRATE

    def updateLocs(self, droneData):
        if(self.currentLocs == []):
            self.currentLocs = droneData
        else:
            self.dest = droneData
            self.updateVectors()

    def updateVectors(self):
        #Calculate unit vector in direction of dest
        tempVectors = []
        for droneCount, drone in enumerate(self.currentLocs):
            newVect = ([ self.dest[droneCount][0] - drone[0] ,self.dest[droneCount][1] - drone[1] ,self.dest[droneCount][2] - drone[2]])
            #Change newVect to unit vector
            lengthVect = 0.0
            for xyz in newVect:
                lengthVect += xyz * xyz

            lengthVect = math.sqrt(lengthVect)

            for xyzcount, xyz in enumerate(newVect):
                newVect[xyzcount] = xyz/lengthVect

            tempVectors.append(newVect)

        self.vectors = tempVectors


    def update(self):
        moveDistMax = self.speedMax/self.refreshRate
        newLocs = []

        if(self.dest):
            for droneCount, drone in enumerate(self.currentLocs):
                #Check if drone is within movedist of destination

                newVect = ([ self.dest[droneCount][0] - drone[0] ,self.dest[droneCount][1] - drone[1] ,self.dest[droneCount][2] - drone[2]])


                lengthVect = 0.0
                for xyz in newVect:
                    lengthVect += xyz * xyz

                lengthVect = math.sqrt(lengthVect)


                #it is, go to dest
		# Small error added to prevent overshooting or extra steps due to inaccuracies in floating point ops
                if(lengthVect <= moveDistMax + 0.000000001):
                    newLocs.append(self.dest[droneCount])

                #otherwise, add vector times movedist to currentloc
                else:
                    tempvect = drone
                    tempvect[0] += self.vectors[droneCount][0]*moveDistMax
                    tempvect[1] += self.vectors[droneCount][1]*moveDistMax
                    tempvect[2] += self.vectors[droneCount][2]*moveDistMax

                    newLocs.append(tempvect)

            #print("vect", self.vectors)
            #print("dest", self.dest)
            #print("curr", self.currentLocs)

            self.currentLocs = newLocs


pub = rospy.Publisher('simtoback', String, queue_size=10)
simData = Siminfo(2)

def callback(data):

    print(data.data)
    droneData = ast.literal_eval(data.data)

    simData.updateLocs(droneData)




def simListener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('backtosim', String, callback)

    rate = rospy.Rate(REFRESHRATE)
    while not rospy.is_shutdown():
        simData.update()
        pub.publish(str(simData.currentLocs))
        rate.sleep()


if __name__ == '__main__':
    simListener()
