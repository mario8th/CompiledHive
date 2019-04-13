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
from gui_ver2 import *
import math

WARNDRONERADIUS = 0.1
STOPDRONERADIUS = 0.05

backend = None
visualizationPub =  rospy.Publisher('backtomonitorvis', String, queue_size=10)
consolePub =        rospy.Publisher('backtomonitorconsole', String, queue_size=10)
destPub =           rospy.Publisher('backtosim', String, queue_size=10)
visPubObstacle =    rospy.Publisher('backtomonitorobstacles', String, queue_size=10)
visPubSensor =      rospy.Publisher('backtomonitorsensors', String, queue_size=10)

class BackendData:
    def __init__(self, fullDroneList, droneList, dests, obstacles, pathDict):
        # Main local vars
        self.fullDroneList = fullDroneList
         # Coords vars
        self.droneList = droneList
        self.destList = dests

         #flight path vars
        self.droneListPaths = []
        for path in pathDict:
            self.droneListPaths.extend(pathDict[path])
            #import file of flight path

        self.pathDict = pathDict

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
        self.checkDronesClose()
        return "No Events Yet"

    # Checks if Drones are within collision radius
    def checkDronesClose(self):
        for droneCount1, drone1 in enumerate(self.currentLoc):
            for droneCount2, drone2 in enumerate(self.currentLoc):
                if(droneCount1 < droneCount2):
                    #Compare distances
                    dist = (((drone1[0] - drone2[0]) * (drone1[0] - drone2[0])) +
                            ((drone1[1] - drone2[1]) * (drone1[1] - drone2[1])) +
                            ((drone1[2] - drone2[2]) * (drone1[2] - drone2[2])))

                    dist = math.sqrt(dist)

                    #Check for potential drone collision
                    if(dist < STOPDRONERADIUS*2):
                        self.activateQuitBool()
                        logString = "Stopping: "
                        logString += "Drone " + str(self.droneList[droneCount1]) + " and Drone " + str(self.droneList[droneCount2])
                        logString += " within stop radius"
                        print(logString)
                    elif(dist < WARNDRONERADIUS*2):
                        logString = "Caution: "
                        logString += "Drone " + str(self.droneList[droneCount1]) + " and Drone " + str(self.droneList[droneCount2])
                        logString += " within warning radius"
                        print(logString)

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
            return newDests


        # Do nothing otherwise

        #print newDests

    def getNewPathDests(self):
        # for each flight path
        #for path in self.pathDict:
        # Assemble all associated drone locations into list

        # Send list to flight path function in imported file

        # Get back list
        # Reassemble into one list of new dests
        # return list of new dests
        pass

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
        # Checks if coord drones are at dest
        coordDests = backend.checkAtDest()
        # Sends locations to functions for new dests
        pathDests = backend.getNewPathDests()
        # Combines 2 lists into full destination list with order based on full drone list
        print("DESTINATION LISTS: ")
        print(coordDests)
        print(pathDests)

#
def receivedEStop(data):
    global backend
    # Publish receipt of Estop to console


    backend.activateQuitBool()



def runBackend(fullDroneList, droneList, dests, obstacles, pathDict):
    # Get global publishers
    global backend, visualizationPub, destPub, consolePub, visPubObstacle, visPubSensor

    # Initialize backend data
    backend = BackendData(fullDroneList, droneList, dests, obstacles, pathDict)

    # Setup subscribers + ros stuff
    rospy.init_node('backend', anonymous=True)

    # Parse and publish obstacles and sensors to visualization to Initialize
    obstaclePacket = []
    for obstacleKey in obstacles:
        obstaclePacket.append(obstacles[obstacleKey])

    visPubObstacle.publish(str(obstaclePacket))
    visPubObstacle.publish(str(obstaclePacket))
    time.sleep(0.1)
    visPubObstacle.publish(str(obstaclePacket))
    visPubObstacle.publish(str(obstaclePacket))

    sensorPacket = []


    # publish first point to sim and viz to init
    destPub.publish(str(backend.currentDest))
    destPub.publish(str(backend.currentDest))
    time.sleep(0.1)
    destPub.publish(str(backend.currentDest))
    destPub.publish(str(backend.currentDest))

    rospy.Subscriber('simtoback', String, receivedLocations)
    rospy.Subscriber('monitortoback', String, receivedEStop)




    #

    rospy.spin()


def launchGui():
    app = QtGui.QApplication(sys.argv)
    gui = WidgetGallery()
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
    droneCoords = flightData[0]

    for drone in droneCoords:
        droneList.append(drone)
        coordList.append(droneCoords[drone])
    print("coordList: ", coordList)

    for listCount, clist in enumerate(coordList):
        for tupleCount, tuple in enumerate(clist):
            coordList[listCount][tupleCount] = list(tuple)
    print("coordList: ", coordList)
    print("\n")

    # Start backend with entered user data
    #runBackend(droneList, coordList, o)bjectDict)
    # Drone list, dest list, obstacle dictionary, dronelist for paths, path dictionary
    runBackend([1,2,3,4,5,6],
    [4,2],
    [[[-4.0,-4.0,5.0],[4.0,-4.0,5.0],[4.0,4.0,5.0],[-4.0,4.0,5.0],[1.0,1.0,1.0]],[[2.0,-2.0,3.0],[-2.0,-2.0,3.0],[-2.0,2.0,3.0],[2.0,2.0,3.0],[1.0,1.0,1.0]]],
    {'object_0': ((1.0, 2.0, 1.0), (3.0, 3.0, 3.0))},
    {'loopout.py': [3,1,5,6]})

if __name__ == "__main__":
    main()


























# I want space
