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
from gui import *

backend = None
visualizationPub =  rospy.Publisher('backtomonitorvis', String, queue_size=10)
consolePub =        rospy.Publisher('backtomonitorconsole', String, queue_size=10)
destPub =           rospy.Publisher('backtosim', String, queue_size=10)
visPubObstacle =    rospy.Publisher('backtomonitorobstacles', String, queue_size=10)
visPubSensor =      rospy.Publisher('backtomonitorsensors', String, queue_size=10)

class BackendData:
    def __init__(self, droneList, dests, obstacles):
        # Main local vars
        self.droneList = droneList
        self.destList = dests
        self.obstacles = obstacles
        self.sensors = [[4.0,-4.0,0.0], [-4.0,-4.0,0.0], [4.0,4.0,0.0], [-4.0,4.0,0.0], [4.0,-4.0,8.0], [-4.0,-4.0,8.0], [4.0,4.0,8.0], [-4.0,4.0,8.0]]

        self.quitBool = False

        # Set up list of destination indices
        self.destIndexList = []
        for drone in droneList:
            self.destIndexList.append(0)

        # Set up first destinations
        self.currentDest = []
        for droneCount, drone in enumerate(self.destList):
            self.currentDest.append(drone[0])

        # Set up first locations
        self.currentLoc = []
        for drone in dests:
            self.currentLoc.append(drone[0])

        print("droneList ", self.droneList)
        print("destList  ", self.destList)
        print("obstacles ", self.obstacles)
        print("destIndexList ", self.destIndexList)
        print("currentDest ", self.currentDest)
        print("currentLoc ", self.currentLoc)

    # Counts number of drones at their destination
    def dronesAtDest(self):
        dronesAtDest = 0

        print(self.currentLoc)
        print(self.currentDest)

        # Assume snycbool is on, count numberr of drones at their destination
        for droneCount, drone in enumerate(self.droneList):
            if(self.currentLoc[droneCount] == self.currentDest[droneCount]):
                dronesAtDest += 1

        return dronesAtDest

    # Methods that check for events and return report strings
    def checkForEvents(self):
        self.checkObstacleCollide()
        self.checkOutOfBounds()
        return "No Events Yet"

    def checkObstacleCollide(self):
        errorFlag = False

        for obstacle in self.obstacles:
            for drone in self.currentLoc:
                #print "checking obstacle ",drone, self.obstacles[obstacle][0], self.obstacles[obstacle][1]
                if(pointWithinRectangle(drone, self.obstacles[obstacle][0], self.obstacles[obstacle][1])):
                    print(str(drone) + ' in obstacle ' + str(obstacle))

    def checkOutOfBounds(self):
        #Find 2 opposite Sensors
        sensor1 = self.sensors[0]
        sensor2 = self.sensors[-1]

        for sensor in self.sensors:
            if(sensor1[0] != sensor[0] and sensor1[1] != sensor[1] and sensor1[2] != sensor[2]):
                sensor2 = sensor

        # Feed each drone into pointWithinRectangle
        errorFlag = False
        for drone in self.currentLoc:
            errorFlag = errorFlag or not pointWithinRectangle(drone, sensor1, sensor2)

        # Drone was out of bounds
        if(errorFlag):
            self.activateQuitBool()
            #Publish to consolePub about flight ending because a drone flew out of bounds
            print "Drone flew out of bounds"

    #Updates current location of drones, whenever sim input is received
    def updateCurrentLoc(self, newLocs):
        self.currentLoc = newLocs

    # Activates wuit bool and sets all drones to land
    def activateQuitBool(self):
        global destPub
        self.quitBool = True
        # Update all destinations to fly straight down
        newDests = []
        for drone in self.currentLoc:
            newDests.append([drone[0], drone[1], 0.0])

        self.currentDest = newDests
        destPub.publish(str(newDests))


    # Checks which drones have reached dest and updates dests accordingly
    def checkAtDest(self):
        global destPub
        dronesAtDest = self.dronesAtDest()

        newDests = []
        # Assuming syncbool, check if all drones are at dest
        if(dronesAtDest == len(self.droneList)):
            #They are, update destlist
            for droneCount, drone in enumerate(self.destList):
                try:
                    newDests.append(self.destList[droneCount][self.destIndexList[droneCount] + 1])
                except:
                    newDests.append(self.destList[droneCount][-1])
                self.destIndexList[droneCount] += 1
            self.currentDest = newDests

            #publish new dests to sim
            destPub.publish(str(newDests))

        # Do nothing otherwise

        #print newDests

# Tests if point is within rectangle bounded by 2 opposite corners
def pointWithinRectangle(point, corner1, corner2):
    withinRect = True

    print point, corner1, corner2

    # Check X values within range
    for xyzIndex in range(3):
        if((point[xyzIndex] >= corner1[xyzIndex] and point[xyzIndex] <= corner2[xyzIndex]) or (point[xyzIndex] <= corner1[xyzIndex] and point[xyzIndex] >= corner2[xyzIndex])):
            pass
        else:
            withinRect = False

    return withinRect

# Forwards drone locations to vis
def forwardDroneLocs():
    global backend, visualizationPub

    visualizationPub.publish(str(backend.currentLoc))


def receivedLocations(data):
    global backend, visualizationPub, destPub, consolePub
    eventString = ""

    # Update drone locations in backend
    newLocs = ast.literal_eval(data.data)

    backend.updateCurrentLoc(newLocs)

    # Check for Events
    eventString = backend.checkForEvents()


    # Publish events to console
    if(eventString):
        consolePub.publish(eventString)

    # Forward drone locations, publishing to vis
    forwardDroneLocs()

    #Check for quitbool, Only check for destinations if it hasnt been updated
    if(not backend.quitBool):
        backend.checkAtDest()


#
def receivedEStop(data):
    global backend
    # Publish receipt of Estop to console


    backend.activateQuitBool()



def runBackend(droneList, dests, obstacles):
    # Get global publishers
    global backend, visualizationPub, destPub, consolePub, visPubObstacle, visPubSensor

    # Initialize backend data
    backend = BackendData(droneList, dests, obstacles)

    # Setup subscribers + ros stuff
    rospy.init_node('backend', anonymous=True)

    # Parse and publish obstacles and sensors to visualization to Initialize
    obstaclePacket = []
    for obstacleKey in obstacles:
        obstaclePacket.append(obstacles[obstacleKey])

    visPubObstacle.publish(str(obstaclePacket))

    sensorPacket = []


    # publish first point to sim and viz to init
    destPub.publish(str(backend.currentDest))

    rospy.Subscriber('simtoback', String, receivedLocations)
    rospy.Subscriber('monitortoback', String, receivedEStop)



    #

    rospy.spin()


def launchGui():
    app = QtGui.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    app.exec_()

    return gui.getData()

def main():
    # Launch GUI to gather user input
    flightData = launchGui()

    # Parse user input
    droneList = []
    coordList = []
    objectDict = flightData[3]
    droneCoords = flightData[2]

    for drone in droneCoords:
        droneList.append(drone)
        coordList.append(droneCoords[drone])
    print("coordList: ", coordList)

    for listCount, clist in enumerate(coordList):
        for tupleCount, tuple in enumerate(clist):
            coordList[listCount][tupleCount] = list(tuple)
    print("coordList: ", coordList)

    # Start backend with entered user data
    #runBackend(droneList, coordList, objectDict)
    runBackend([1,2], [[[-4.0,-4.0,5.0],[4.0,-4.0,5.0],[4.0,4.0,5.0],[-4.0,4.0,5.0]],[[2.0,-2.0,3.0],[-2.0,-2.0,3.0],[-2.0,2.0,3.0],[2.0,2.0,3.0]]], {'object_0': ((1.0, 2.0, 1.0), (3.0, 3.0, 3.0))})

if __name__ == "__main__":
    main()


























# I want space
