#!/usr/bin/env python
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
import random
import rospy
import ast
from std_msgs.msg import String

# Constants

SHAPE_COLOR = 'red'
DRONE_COLOR = 'grey'
SENSOR_COLOR = 'blue'
OPATH_COLOR = 'lime'

XLAB = "X Label"
YLAB = "Y Label"
ZLAB = "Z Label"

REFRESH_RATE = 10
REFRESH_WAIT = 1.0/REFRESH_RATE

newValues = []
obstacles = [[[1,1,1],[4,4,8]]]
sensors = [[-4, -4, 4, 4, -4, -4, 4, 4], [4, -4, 4, -4, 4, -4, 4, -4], [0, 0, 0, 0, 8, 8, 8, 8]]
configList = [True, True,1,1,1,1]

class VisualizationData:
    def __init__(self):
        global obstacles
        global sensors
        # Class Variables
        self.sensors = sensors

        # List of all drones most recent location
        self.newLocs = []

        # List of lists of each drones location history
        self.allX = []
        self.allY = []
        self.allZ = []

        # Calculate obstacle paths
        # Initialize lists
        self.obstacleX = []
        self.obstacleY = []
        self.obstacleZ = []

        """
        for sh in obstacles:
            # Loop one face
            shapeX = [sh[0][0],sh[0][0],sh[0][0],sh[0][0],sh[0][0]]
            shapeY = [sh[0][1],sh[0][1],sh[1][1],sh[1][1],sh[0][1]]
            shapeZ = [sh[1][2],sh[0][2],sh[0][2],sh[1][2],sh[1][2]]
            # Loop opposite face, at each point jump to matching point on previous face
            shapeX.extend([sh[1][0],sh[1][0],sh[0][0],sh[1][0],sh[1][0],sh[0][0],sh[1][0],sh[1][0] ,sh[0][0],sh[1][0],sh[1][0]])
            shapeY.extend([sh[0][1],sh[1][1],sh[1][1],sh[1][1],sh[1][1],sh[1][1],sh[1][1],sh[0][1] ,sh[0][1],sh[0][1],sh[0][1]])
            shapeZ.extend([sh[1][2],sh[1][2],sh[1][2],sh[1][2],sh[0][2],sh[0][2],sh[0][2],sh[0][2] ,sh[0][2],sh[0][2],sh[1][2]])
            self.obstacleX.append(shapeX)
            self.obstacleY.append(shapeY)
            self.obstacleZ.append(shapeZ)
        """

        self.updateObstacles()


    def updateLocations(self, newLocs):

        if(self.newLocs == []):
            for drone in newLocs:
                self.allX.append([])
                self.allY.append([])
                self.allZ.append([])

        # Update most recent locations
        self.newLocs = newLocs

        # Place points into array for graphing
        for droneCount, drone in enumerate(newLocs):
            self.allX[droneCount].append(drone[0])
            self.allY[droneCount].append(drone[1])
            self.allZ[droneCount].append(drone[2])

    def updateObstacles(self):
        global obstacles
        # Calculate obstacle paths
        # Initialize lists
        self.obstacleX = []
        self.obstacleY = []
        self.obstacleZ = []

        for sh in obstacles:
            # Loop one face
            shapeX = [sh[0][0],sh[0][0],sh[0][0],sh[0][0],sh[0][0]]
            shapeY = [sh[0][1],sh[0][1],sh[1][1],sh[1][1],sh[0][1]]
            shapeZ = [sh[1][2],sh[0][2],sh[0][2],sh[1][2],sh[1][2]]

            # Loop opposite face, at each point jump to matching point on previous face
            shapeX.extend([sh[1][0],sh[1][0],sh[0][0],sh[1][0],sh[1][0],sh[0][0],sh[1][0],sh[1][0] ,sh[0][0],sh[1][0],sh[1][0]])
            shapeY.extend([sh[0][1],sh[1][1],sh[1][1],sh[1][1],sh[1][1],sh[1][1],sh[1][1],sh[0][1] ,sh[0][1],sh[0][1],sh[0][1]])
            shapeZ.extend([sh[1][2],sh[1][2],sh[1][2],sh[1][2],sh[0][2],sh[0][2],sh[0][2],sh[0][2] ,sh[0][2],sh[0][2],sh[1][2]])

            self.obstacleX.append(shapeX)
            self.obstacleY.append(shapeY)
            self.obstacleZ.append(shapeZ)


    def updatePlot(self, axis):
        global configList

        # Update obstacle positions
        self.updateObstacles()

        plt.cla()
        # Plot Drone locations
        if(configList[1]):
            for droneCount, drone in enumerate(self.allX):
                axis.scatter(self.allX[droneCount][-1], self.allY[droneCount][-1], self.allZ[droneCount][-1], c=DRONE_COLOR, marker='v', alpha = 1)

        # Plot drone paths
        if(configList[2]):
            for droneCount, drone in enumerate(self.allX):
                axis.plot(self.allX[droneCount], self.allY[droneCount], self.allZ[droneCount], c=OPATH_COLOR, linewidth = 1)

        # Plot expected paths
        if(configList[3]):
            #self.plot_expected_paths(axis)
            pass

        # Plot sensors
        if(configList[4]):
            axis.scatter(self.sensors[0], self.sensors[1], self.sensors[2], c=SENSOR_COLOR, marker='^')

        # Plot obstacles
        if(configList[5]):
            for obstacleCount, obstacle in enumerate(self.obstacleX):
                axis.plot(self.obstacleX[obstacleCount], self.obstacleY[obstacleCount], self.obstacleZ[obstacleCount], c=SHAPE_COLOR, linewidth = 0.75)



"""def testing():
    configList = [1,0,1,1,1,1]
    vd = VisualizationData([[[1,4,0],[3,2,2]], [[4,0,5],[0,1,7]]],
            [[-4, -4, 4, 4, -4, -4, 4, 4],
            [4, -4, 4, -4, 4, -4, 4, -4],
            [0, 0, 0, 0, 8, 8, 8, 8]], configList)
    # Set up plotting stuff
    fig = plt.figure()
    fig.canvas.set_window_title('Drone Visualization')
    ax = fig.add_subplot(111, projection='3d')
    vd.updateLocations([[0,0,4], [0,2,0]])
    vd.updatePlot(ax, configList)
    plt.pause(1)
    vd.updateLocations([[0,0,3], [0,1,0]])
    vd.updatePlot(ax, configList)
    plt.pause(1)
    vd.updateLocations([[0,0,2], [0,0,0]])
    vd.updatePlot(ax, configList)
    # ani = animation.FuncAnimation(fig, vd.updatePlot, interval=100)
    vd.updatePlot(ax, configList)
    plt.pause(5)
    plt.show()"""

def callback(data):
    global newValues
    newValues = ast.literal_eval(data.data)

def updateVis(vd, axis):
    # Get most recent location and store in local then update
    global newValues
    localNewVal = newValues
    print localNewVal
    vd.updateLocations(localNewVal)
    vd.updatePlot(axis)
    plt.pause(REFRESH_WAIT)

def obstacleReceive(data):
    global obstacles
    obstacles = ast.literal_eval(data.data)
    print obstacles

def sensorReceive(data):
    global sensors
    sensors = ast.literal_eval(data.data)

def configReceive(data):
    global configList
    print "COP: " + data.data
    configList = ast.literal_eval(data.data)
    #print configList
def main():

    """
    vd = VisualizationData([[[1,4,0],[3,2,2]], [[4,0,5],[0,1,7]]],
            [[-4, -4, 4, 4, -4, -4, 4, 4],
            [4, -4, 4, -4, 4, -4, 4, -4],
            [0, 0, 0, 0, 8, 8, 8, 8]], configList)
    """
    """
    vd = VisualizationData([[[1,1,4],[4,4,8]]],
            [[-4, -4, 4, 4, -4, -4, 4, 4],
            [4, -4, 4, -4, 4, -4, 4, -4],
            [0, 0, 0, 0, 8, 8, 8, 8]], configList)
    """

    vd = VisualizationData()

    # Set up plotting stuff
    fig = plt.figure()
    fig.canvas.set_window_title('Drone Visualization')
    ax = fig.add_subplot(111, projection='3d')

    rospy.init_node("monitornode", anonymous=True)

    rospy.Subscriber('backtomonitorvis', String, callback)
    rospy.Subscriber('backtomonitorobstacles', String, obstacleReceive)
    rospy.Subscriber('backtomonitorsensors', String, sensorReceive)
    rospy.Subscriber('backtomonitorconfig', String, configReceive)

    rate = rospy.Rate(REFRESH_RATE)
    while (not rospy.is_shutdown()):
        #Fetch most recent newValues and update plot with them
        updateVis(vd, ax)

        rate.sleep()





if __name__ == "__main__":
    main()
















# I want space
