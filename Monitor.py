#!/usr/bin/env python
import sys
import rospy
import ast
from std_msgs.msg import String
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *

monitor = None
notifList = []

class Monitor(QMainWindow):
    def __init__(self, parent = None):
        rospy.init_node('monitor', anonymous=True)
        # Set up window for console
        super(Monitor, self).__init__(parent)
        self.resize(420, 250)

        # Set text window params
        self.notifs = QPlainTextEdit(self)
        self.setWindowTitle("Monitor")
        self.notifs.move(10, 10)
        self.notifs.resize(400, 200)

        self.notifs.setReadOnly(True)

        self.endButtn = QPushButton("End Flight", self)
        self.endButtn.move(310, 215)
        self.endButtn.clicked.connect(self.endFlight)

        rospy.Subscriber('backtomonitorconsole', String, recieveNotif)
        '''rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.updateNotifs()
            rate.sleep()'''

    def updateNotifs(self):
        global notifList
        notifs = notifList
        notifList = []
        for string in notifs:
            self.notifs.appendPlainText(string)

    def endFlight(self):
        backendPub = rospy.Publisher('monitortoback', String, queue_size=10)
        print("Starting to end the flight II: Electric Boogaloo")
        backendPub.publish("END FLIGHT")

def launchMonitor():
    global monitor
    app = QtGui.QApplication(sys.argv)
    monitor = Monitor()
    monitor.show()
    app.exec_()

def recieveNotif(data):
    global notifList, monitor
    notifList.append(str(data.data))
    #monitor.updateNotifs()


if __name__ == "__main__":
    launchMonitor()
