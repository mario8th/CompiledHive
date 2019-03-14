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
visualization_pub = rospy.Publisher('backtomonitorvis', String, queue_size=10)
console_pub = rospy.Publisher('backtomonitorconsole', String, queue_size=10)
dest_pub = rospy.Publisher('backtosim', String, queue_size=10)

class BackendData:
    def __init__(self, dronelist, dests, obstacles):
        # Main local vars
        self.droneList = dronelist
        self.destList = dests
        self.obstacles = obstacles

        self.quitBool = False

        # Set up list of destination indices
        self.destIndexList = []
        for drone in dronelist:
            self.destIndexList.append(0)

        # Set up first destinations
        self.currentDest = []
        for dronecount, drone in enumerate(self.destList):
            self.currentDest.append(drone[0])

        # Set up first locations
        self.currentLoc = []
        for drone in dests:
            self.currentLoc.append(drone[0])

        print("dronelist ", self.droneList)
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
        for dronecount, drone in enumerate(self.droneList):
            if(self.currentLoc[dronecount] == self.currentDest[dronecount]):
                dronesAtDest += 1

        return dronesAtDest

    # Methods that check for events and return report strings
    def checkForEvents(self):
        self.checkObstacleCollide()
        self.checkOutOfBounds()
        return "No Events Yet"

    def checkObstacleCollide(self):
        pass

    def checkOutOfBounds(self):
        pass

    #Updates current location of drones, whenever sim input is received
    def updateCurrentLoc(self, newLocs):
        self.currentLoc = newLocs

    # Activates wuit bool and sets all drones to land
    def activateQuitBool(self):
        self.quitBool = True
        # Update all destinations to fly straight down
        newDests = []
        for drone in self.currentDest:
            newDests.append([drone[0], drone[1], 0.0])

        self.destList = newDests

    # Checks which drones have reached dest and updates dests accordingly
    def checkAtDest(self):
        global dest_pub
        dronesAtDest = self.dronesAtDest()

        newDests = []
        # Assuming syncbool, check if all drones are at dest
        if(dronesAtDest == len(self.droneList)):
            #They are, update destlist
            for dronecount, drone in enumerate(self.destList):
                try:
                    newDests.append(self.destList[dronecount][self.destIndexList[dronecount] + 1])
                except:
                    newDests.append(self.destList[dronecount][-1])
                self.destIndexList[dronecount] += 1
            self.currentDest = newDests

            #publish new dests to sim
            dest_pub.publish(str(newDests))

        # Do nothing otherwise

        #print newDests


# Forwards drone locations to vis
def forwardDroneLocs():
    global backend, visualization_pub

    visualization_pub.publish(str(backend.currentLoc))


def receivedLocations(data):
    global backend, visualization_pub, dest_pub, console_pub
    eventString = ""

    # Update drone locations in backend
    newLocs = ast.literal_eval(data.data)

    backend.updateCurrentLoc(newLocs)

    # Check for Events
    eventString = backend.checkForEvents()


    # Publish events to console
    if(eventString):
        console_pub.publish(eventString)

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



def runBackend(dronelist, dests, obstacles):
    # Get global publishers
    global backend, visualization_pub, dest_pub, console_pub

    # Initialize backend data
    backend = BackendData(dronelist, dests, obstacles)

    # Setup subscribers + ros stuff
    rospy.init_node('backend', anonymous=True)

    # publish first point to sim and viz to init
    dest_pub.publish(str(backend.currentDest))

    rospy.Subscriber('simtoback', String, receivedLocations)
    rospy.Subscriber('monitortoback', String, receivedEStop)



    #

    rospy.spin()


def launchGui():
    app = QtGui.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    app.exec_()

    return gui.get_data()

def main():
    flightData = launchGui()
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
    runBackend(droneList, coordList, objectDict)
    #runBackend([1,2], [[[-4.0,-4.0,5.0],[4.0,-4.0,5.0],[4.0,4.0,5.0],[-4.0,4.0,5.0]],[[2.0,-2.0,3.0],[-2.0,-2.0,3.0],[-2.0,2.0,3.0],[2.0,2.0,3.0]]], {})

if __name__ == "__main__":
    main()


























# I want space
