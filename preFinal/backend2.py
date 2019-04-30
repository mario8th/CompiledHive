#!/usr/bin/env python
import numpy as np
import time
import rospy
import ast
from std_msgs.msg import String
from gui_ver2 import *
import math
import importlib

WARNDRONERADIUS = 0.2
STOPDRONERADIUS = 0.1

ERRORMARGIN = 0.0

backend = None
visualizationPub =  rospy.Publisher('backtomonitorvis', String, queue_size=10)
consolePub =        rospy.Publisher('backtomonitorconsole', String, queue_size=10)
destPub =           rospy.Publisher('backtosim', String, queue_size=10)
visPubObstacle =    rospy.Publisher('backtomonitorobstacles', String, queue_size=10)
visPubSensor =      rospy.Publisher('backtomonitorsensors', String, queue_size=10)
visPubConfig =      rospy.Publisher('backtomonitorconfig', String, queue_size=10)

logFile = ""

class BackendData:
    def __init__(self, fullDroneList, destDict, pathDict, obstDict, visConfig, logConfig):
        # Static Data
        # Official drone order
        self.fullDroneList = fullDroneList
        # Path information
        self.destDict = destDict
        self.pathDict = pathDict
        # obstacles and sesnsors
        self.obstDict = obstDict
        self.sensors = [[4.0,-4.0,0.0], [-4.0,-4.0,0.0], [4.0,4.0,0.0], [-4.0,4.0,0.0], [4.0,-4.0,8.0], [-4.0,-4.0,8.0], [4.0,4.0,8.0], [-4.0,4.0,8.0]]

        # Config files
        self.visConfig = visConfig
        self.logConfig = logConfig

        # Tracks major error occurence
        self.quitBool = False

        # Start locations
        self.startLocations = []
        pathDrones = 1.0
        for drone in fullDroneList:
            if drone in self.destDict:
                self.startLocations.append(self.destDict[drone][0])
            else:
                self.startLocations.append([pathDrones, 2.0, 0.0])
                pathDrones = round(pathDrones + 0.3, 2)

        # Tracks current dest for each drone
        self.destIndexDict = {}
        for drone in self.destDict:
            self.destIndexDict[drone] = 0

        # Start drones at start locations
        self.currentLocations = self.startLocations
        self.currentDests = self.startLocations

        # Import all flight path files
        self.importDict = {}
        for file in self.pathDict:
            self.importDict[file] = importlib.import_module(file)


    # Methods that check for events and return report strings
    def checkForEvents(self):
        self.checkObstacleCollide()
        self.checkOutOfBounds()
        self.checkDronesClose()

    # Checks if Drones are within collision radius
    def checkDronesClose(self):
        for droneCount1, drone1 in enumerate(self.currentLocations):
            for droneCount2, drone2 in enumerate(self.currentLocations):
                if(droneCount1 < droneCount2):
                    #Compare distances
                    dist = (((drone1[0] - drone2[0]) * (drone1[0] - drone2[0])) +
                            ((drone1[1] - drone2[1]) * (drone1[1] - drone2[1])) +
                            ((drone1[2] - drone2[2]) * (drone1[2] - drone2[2])))

                    dist = math.sqrt(dist)

                    #Check for potential drone collision
                    if(dist < STOPDRONERADIUS):
                        self.activateQuitBool()
                        logString = "Stopping: "
                        logString += "Drone " + str(self.fullDroneList[droneCount1]) + " and Drone " + str(self.fullDroneList[droneCount2])
                        logString += " within stop radius"
                        self.toLog('E', logString)
                    elif(dist < WARNDRONERADIUS):
                        logString = "Caution: "
                        logString += "Drone " + str(self.fullDroneList[droneCount1]) + " and Drone " + str(self.fullDroneList[droneCount2])
                        logString += " within warning radius"
                        self.toLog('E', logString)

    # Checks if a drone is within an obstacle
    def checkObstacleCollide(self):
        errorFlag = False

        for obstacle in self.obstDict:
            for drone in self.currentLocations:
                if(pointWithinRectangle(drone, self.obstDict[obstacle][0], self.obstDict[obstacle][1])):
                    logString = str(drone) + ' in obstacle ' + str(obstacle)
                    self.toLog('E', logString)

    # Checks if drone is out of bounds
    def checkOutOfBounds(self):
        #Find 2 opposite Sensors
        sensor1 = self.sensors[0]
        sensor2 = self.sensors[-1]

        for sensor in self.sensors:
            if(sensor1[0] != sensor[0] and sensor1[1] != sensor[1] and sensor1[2] != sensor[2]):
                sensor2 = sensor

        # Feed each drone into pointWithinRectangle
        errorFlag = False
        for drone in self.currentLocations:
            errorFlag = errorFlag or not pointWithinRectangle(drone, sensor1, sensor2)

        # Drone was out of bounds
        if(errorFlag):
            self.activateQuitBool()
            #Publish to consolePub about flight ending because a drone flew out of bounds
            logString = "Drone flew out of bounds"
            self.toLog('E', logString)


    # Activates wuit bool and sets all drones to land
    def activateQuitBool(self):
        global destPub
        self.quitBool = True

        newDests = self.startLocations

        self.currentDests = newDests
        destPub.publish(str(newDests))

    # Checks which drones have reached dest and updates dests accordingly
    def update(self):
        # Get destinations for point by point path, gets dict back
        pointDests = self.getPointDests()

        # Get destinations for each function path, gets dict back
        functionDests = self.getFunctionDests()

        # Combine dest lists, in order by self.fullDroneList
        newDests = []
        for drone in self.fullDroneList:
            if drone in pointDests:
                newDests.append(pointDests[drone])
            else:
                newDests.append(functionDests[drone])

        self.currentDests = newDests

    def getPointDests(self):
        pointDestDict = {}
        for droneCount, drone in enumerate(self.fullDroneList):
            if drone in self.destDict:
                # Test location against destination
                if(calcDistance(self.currentLocations[droneCount], self.currentDests[droneCount]) <= ERRORMARGIN):
                    # Drone within error margin, move to next to next destination
                    # Update Destination index
                    if(len(self.destDict[drone]) <=  self.destIndexDict[drone] + 1):
                        self.destIndexDict[drone] = self.destIndexDict[drone]
                    else:
                        self.destIndexDict[drone] = self.destIndexDict[drone] + 1
                pointDestDict[drone] = self.destDict[drone][self.destIndexDict[drone]]

        return pointDestDict

    def getFunctionDests(self):
        pathDestDict = {}
        # for each flight path
        for path in self.pathDict:
            # Package all drone locations for that path into one list
            paramLocations = []
            for drone in self.pathDict[path]:
                paramLocations.append(self.currentLocations[self.fullDroneList.index(drone)])

            # Send list to function and recieve new destinations
            print path
            newDests = self.importDict[path].flightPath(paramLocations)
            # Reassemble lists into single dictionary
            for droneCount, drone in enumerate(newDests):
                pathDestDict[self.pathDict[path][droneCount]] = drone

        return pathDestDict


    def toLog(self, commandLetter, logString):
        global logFile
        # Take in command + string
        # Test command against Config
        # if logging that command, log

        print logString

        # Test if logging
        if(self.logConfig[0]):
            # Open File to log
            log = open(logFile, 'a')
            # Test for events and logging config for events
            if(commandLetter == 'E' and self.logConfig[7]):
                log.write(logString + "\n")
                consolePub.publish(logString)
            elif(commandLetter == 'L' and self.logConfig[2]):
                log.write(logString + "\n")

            log.close()

# Tests if point is within rectangle bounded by 2 opposite corners
def pointWithinRectangle(point, corner1, corner2):
    withinRect = True

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

    visualizationPub.publish(str(backend.currentLocations))


def receivedLocations(data):
    global backend, visualizationPub, destPub, consolePub
    # Update currentlocs in backend
    backend.currentLocations = ast.literal_eval(data.data)
    backend.toLog('L', str(backend.currentLocations))

    # Forward drone locations to vis
    forwardDroneLocs()

    backend.checkForEvents()

    if(not backend.quitBool):
        # Do calculations based on new locations, building new destinations
        backend.update()

        #Send destinations to sim
        destPub.publish(str(backend.currentDests))


#
def receivedEStop(data):
    global backend
    # Publish receipt of Estop to console

    backend.activateQuitBool()

def calcDistance(point1, point2):
    dist = 0
    dist += ((point1[0] - point2[0]) * (point1[0] - point2[0]))
    dist += ((point1[1] - point2[1]) * (point1[1] - point2[1]))
    dist += ((point1[2] - point2[2]) * (point1[2] - point2[2]))
    return math.sqrt(dist)

def runBackend(fullDroneList, destDict, pathDict, obstDict, visConfig, logConfig):
    # Get global publishers
    global backend, visualizationPub, destPub, consolePub, visPubObstacle, visPubSensor, visPubConfig

    # Initialize backend data
    backend = BackendData(fullDroneList, destDict, pathDict, obstDict, visConfig, logConfig)

    # Setup subscribers + ros stuff
    rospy.init_node('backend', anonymous=True)

    # Parse and publish obstacles and sensors to visualization to Initialize
    obstaclePacket = []
    for obstacleKey in obstDict:
        obstaclePacket.append(obstDict[obstacleKey])

    # Publish obstacles to initialize
    visPubObstacle.publish(str(obstaclePacket))
    visPubObstacle.publish(str(obstaclePacket))
    time.sleep(0.1)
    visPubObstacle.publish(str(obstaclePacket))
    visPubObstacle.publish(str(obstaclePacket))

    # Publish start locations to initialize
    destPub.publish(str(backend.currentDests))
    destPub.publish(str(backend.currentDests))
    time.sleep(0.1)
    destPub.publish(str(backend.currentDests))
    destPub.publish(str(backend.currentDests))

    visPubConfig.publish(str(visConfig))
    visPubConfig.publish(str(visConfig))
    time.sleep(0.1)
    visPubConfig.publish(str(visConfig))
    visPubConfig.publish(str(visConfig))

    rospy.Subscriber('simtoback', String, receivedLocations)
    rospy.Subscriber('monitortoback', String, receivedEStop)

    rospy.spin()




def main():
    global logFile
    # Launch GUI to gather user input
    flightData = launchGui()
    print flightData

    logFile = flightData[6]

    # Parse user input
    fullDroneList = []
    # Dest list
    for drone in flightData[0]:
        fullDroneList.append(drone)
    # Path list
    for path in flightData[2]:
        fullDroneList.extend(flightData[2][path])

    runBackend(fullDroneList, flightData[0], flightData[2], flightData[3], flightData[4], flightData[5])

    '''runBackend([2,1,3,4],
    { 2:[[2.0,-2.0,0.0],[2.0,-2.0,3.0],[-2.0,-2.0,3.0],[-2.0,2.0,3.0],[2.0,2.0,3.0],[1.0,1.0,1.0]],1:[[-4.0,-4.0,0.0],[-4.0,-4.0,5.0],[4.0,-4.0,5.0],[4.0,4.0,5.0],[-4.0,4.0,5.0],[1.0,1.0,1.0]]},
    {"loopout": [3,4]},
    {'object_0': ((1.0, 2.0, 1.0), (3.0, 3.0, 3.0))},
    [True, 1,1,1,1,1],
    [True, True, True, 2.0, True, False, False, True])'''

if __name__ == "__main__":
    main()


























# I want space
