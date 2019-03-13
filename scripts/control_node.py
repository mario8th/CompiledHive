from gui import *
from visros import *
#import rospy
#import simulator.py
#import backend.py

def main():
    app = QtGui.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    app.exec_()

    data_tuple = gui.get_data()
    print data_tuple

    # Start's Sim Stuffs
    #simListener()

    monitor = Monitor()
    monitor.show()

    # Start's Backend Stuffs
    '''droneList = []
    coordList = []
    objectDict = data_tuple[3]
    droneCoords = data_tuple[2]
    for drone in droneCoords:
        droneList.append(drone)
        coordList.append(droneCoords[drone])
    backListener(droneList, droneCoords, objectDict)'''

    app.exec_()

    # End Everything
if __name__ == '__main__':
    main()
