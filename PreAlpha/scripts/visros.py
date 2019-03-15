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

new_values = []

class VisualizationData:
    def __init__(self, obstacles, sensors, configlist):
        # Class Variables
        self.sensors = sensors

        # List of all drones most recent location
        self.newlocs = []

        # List of lists of each drones location history
        self.allx = []
        self.ally = []
        self.allz = []

        # Calculate obstacle paths
        # Initialize lists
        self.obstaclex = []
        self.obstacley = []
        self.obstaclez = []

        for sh in obstacles:
            # Loop one face
            shapex = [sh[0][0],sh[0][0],sh[0][0],sh[0][0],sh[0][0]]
            shapey = [sh[0][1],sh[0][1],sh[1][1],sh[1][1],sh[0][1]]
            shapez = [sh[1][2],sh[0][2],sh[0][2],sh[1][2],sh[1][2]]

            # Loop opposite face, at each point jump to matching point on previous face
            shapex.extend([sh[1][0],sh[1][0],sh[0][0],sh[1][0],sh[1][0],sh[0][0],sh[1][0],sh[1][0] ,sh[0][0],sh[1][0],sh[1][0]])
            shapey.extend([sh[0][1],sh[1][1],sh[1][1],sh[1][1],sh[1][1],sh[1][1],sh[1][1],sh[0][1] ,sh[0][1],sh[0][1],sh[0][1]])
            shapez.extend([sh[1][2],sh[1][2],sh[1][2],sh[1][2],sh[0][2],sh[0][2],sh[0][2],sh[0][2] ,sh[0][2],sh[0][2],sh[1][2]])

            self.obstaclex.append(shapex)
            self.obstacley.append(shapey)
            self.obstaclez.append(shapez)


    def update_locations(self, newlocs):

        if(self.newlocs == []):
            for drone in newlocs:
                self.allx.append([])
                self.ally.append([])
                self.allz.append([])

        # Update most recent locations
        self.newlocs = newlocs

        # Place points into array for graphing
        for dronecount, drone in enumerate(newlocs):
            self.allx[dronecount].append(drone[0])
            self.ally[dronecount].append(drone[1])
            self.allz[dronecount].append(drone[2])

    def update_plot(self, axis, configlist):

        # Plot Drone locations
        if(configlist[1]):
            for dronecount, drone in enumerate(self.allx):
                axis.scatter(self.allx[dronecount][-1], self.ally[dronecount][-1], self.allz[dronecount][-1], c=DRONE_COLOR, marker='v', alpha = 1)

        # Plot drone paths
        if(configlist[2]):
            for dronecount, drone in enumerate(self.allx):
                axis.plot(self.allx[dronecount], self.ally[dronecount], self.allz[dronecount], c=OPATH_COLOR, linewidth = 0.75)

        # Plot expected paths
        if(configlist[3]):
            #self.plot_expected_paths(axis)
            pass

        # Plot sensors
        if(configlist[4]):
            axis.scatter(self.sensors[0], self.sensors[1], self.sensors[2], c=SENSOR_COLOR, marker='^')

        # Plot obstacles
        if(configlist[5]):
            for obstaclecount, obstacle in enumerate(self.obstaclex):
                axis.plot(self.obstaclex[obstaclecount], self.obstacley[obstaclecount], self.obstaclez[obstaclecount], c=SHAPE_COLOR, linewidth = 0.75)



"""def testing():
    configlist = [1,0,1,1,1,1]
    vd = VisualizationData([[[1,4,0],[3,2,2]], [[4,0,5],[0,1,7]]],
            [[-4, -4, 4, 4, -4, -4, 4, 4],
            [4, -4, 4, -4, 4, -4, 4, -4],
            [0, 0, 0, 0, 8, 8, 8, 8]], configlist)
    # Set up plotting stuff
    fig = plt.figure()
    fig.canvas.set_window_title('Drone Visualization')
    ax = fig.add_subplot(111, projection='3d')
    vd.update_locations([[0,0,4], [0,2,0]])
    vd.update_plot(ax, configlist)
    plt.pause(1)
    vd.update_locations([[0,0,3], [0,1,0]])
    vd.update_plot(ax, configlist)
    plt.pause(1)
    vd.update_locations([[0,0,2], [0,0,0]])
    vd.update_plot(ax, configlist)
    # ani = animation.FuncAnimation(fig, vd.update_plot, interval=100)
    vd.update_plot(ax, configlist)
    plt.pause(5)
    plt.show()"""

def callback(data):
    global new_values
    new_values = ast.literal_eval(data.data)

def update_vis(vd, axis, configlist):
    # Get most recent location and store in local then update
    global new_values
    local_new_val = new_values
    print local_new_val
    vd.update_locations(local_new_val)
    vd.update_plot(axis, configlist)
    plt.pause(REFRESH_WAIT)

def main():

    configlist = [1,0,1,1,1,1]

    """
    vd = VisualizationData([[[1,4,0],[3,2,2]], [[4,0,5],[0,1,7]]],
            [[-4, -4, 4, 4, -4, -4, 4, 4],
            [4, -4, 4, -4, 4, -4, 4, -4],
            [0, 0, 0, 0, 8, 8, 8, 8]], configlist)
    """

    vd = VisualizationData([[[1,1,4],[4,4,8]]],
            [[-4, -4, 4, 4, -4, -4, 4, 4],
            [4, -4, 4, -4, 4, -4, 4, -4],
            [0, 0, 0, 0, 8, 8, 8, 8]], configlist)

    # Set up plotting stuff
    fig = plt.figure()
    fig.canvas.set_window_title('Drone Visualization')
    ax = fig.add_subplot(111, projection='3d')

    rospy.init_node("monitornode", anonymous=True)

    rospy.Subscriber('backtomonitorvis', String, callback)

    rate = rospy.Rate(REFRESH_RATE)
    while (not rospy.is_shutdown()):
        #Fetch most recent new_values and update plot with them
        update_vis(vd, ax, configlist)

        rate.sleep()





if __name__ == "__main__":
    main()
















# I want space
