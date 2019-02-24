import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Global Vars
drone_list = []
ready_drones = []
flight_list = []
assigned_drones = [[],[],[],[],[],[],[]]
drone_coords = [[],[],[],[],[],[],[]]

# Window to input drones
class drone_window(QtGui.QMainWindow):
    # Sets up window with title, label, texbox, add and remove buttons
    def __init__(self, parent=None):
        super(drone_window, self).__init__(parent)
        self.resize(320,160)

        self.setWindowTitle("Add/Remove Drones")

        self.label_drones = QtGui.QLabel(self)
        self.label_drones.setText("Enter a drone id:")
        self.label_drones.move(20, 0)
        self.label_drones.resize(180, 20)

        self.textbox_drones = QLineEdit(self)
        self.textbox_drones.resize(280, 40)
        self.textbox_drones.move(20, 30)

        self.button_add = QPushButton('Add Drone', self)
        self.button_add.move(20, 80)
        
        self.button_remove = QPushButton('Remove Drone', self)
        self.button_remove.move(200, 80)
        
        self.button_goto_flight = QPushButton('Next', self)
        self.button_goto_flight.move(200, 120)

        self.button_add.clicked.connect(self.add_drone_click) 

        self.button_remove.clicked.connect(self.remove_drone_click)

        self.button_goto_flight.clicked.connect(self.goto_flight)
        self.fp_window = flight_window(self)
    # Adds drone to drone_list if max has not been hit
    def add_drone_click(self):
        global drone_list
        curr_drone = self.textbox_drones.text()
        if(curr_drone == ""):
            return
        if(curr_drone in drone_list):
            print "Drone already added"
        elif(len(drone_list) < 7):
            drone_list.append(curr_drone)
            display_list(drone_list)
        else:
            print "Max number of drones set"
        self.textbox_drones.setText("")
    # removes drone form drone_list if able        
    def remove_drone_click(self):
        global drone_list
        curr_drone = self.textbox_drones.text()
        if(curr_drone == ""):
            return
        if(curr_drone in drone_list):
            drone_list.remove(curr_drone)
            print "removed drone: " + curr_drone
        else:
            print "Drone not connected"
        display_list(drone_list)
        self.textbox_drones.setText("")
    # starts flight window     
    def goto_flight(self):
        self.fp_window.show()
        
# sets up window to input flights
class flight_window(QtGui.QMainWindow):
    # same as previous, but different names
    def __init__(self, parent=None):
        super(flight_window, self).__init__(parent)
        self.resize(320, 160)
        self.setWindowTitle("Add/Remove Flight Path")

        self.label_fp = QLabel(self)
        self.label_fp.setText("Enter a flight path:")
        self.label_fp.move(20, 0)
        self.label_fp.resize(180, 20)

        self.textbox_fp = QLineEdit(self)
        self.textbox_fp.resize(280, 40)
        self.textbox_fp.move(20, 30)

        self.button_add = QPushButton('Add Flight Path', self)
        self.button_add.move(20, 80)
        
        self.button_remove = QPushButton('Remove Flight Path', self)
        self.button_remove.move(200, 80)
        
        self.button_goto_connect = QPushButton('Next', self)
        self.button_goto_connect.move(200, 120)

        self.button_add.clicked.connect(self.add_fp_click) 

        self.button_remove.clicked.connect(self.remove_fp_click)

        self.button_goto_connect.clicked.connect(self.goto_connect)
        self.c_window = ""
    # adds flight if able
    def add_fp_click(self):
        global flight_list
        curr_flight = self.textbox_fp.text()
        if(curr_flight == ""):
            return
        if(curr_flight in flight_list):
            print "Flight already added"
        elif(len(flight_list) < 7):
            flight_list.append(curr_flight)
            display_list(flight_list)
        else:
            print "Max number of flights set"
        self.textbox_fp.setText("")
    # removes flight if able
    def remove_fp_click(self):
        global flight_list
        curr_flight = self.textbox_fp.text()
        if(curr_flight == ""):
            return
        if(curr_flight in flight_list):
            flight_list.remove(curr_flight)
            print "Removed flight path: " + curr_flight
        else:
            print "Flight not connected"
        display_list(flight_list)
        self.textbox_fp.setText("")
    # initiates connect window and starts it
    def goto_connect(self):
        self.c_window = connect_window(self)
        self.c_window.show()

# connect window to add drones to flight paths
class connect_window(QtGui.QMainWindow):
    # sets up title and warning message
    # checks size of flight list and adds buttons as needed
    # changes size of window as needed
    def __init__(self, parent=None):
        global flight_list
        global drone_list
        global ready_drones
        super(connect_window, self).__init__(parent)
        ready_drones = drone_list[0:]
        flight_len = len(flight_list)
        
        self.resize(320, 80)
        self.setWindowTitle("Connect Drones to Flights")

        self.label_title = QtGui.QLabel(self)
        self.label_title.setText("Add/Remove drones for each flight path")
        self.label_title.resize(300,20)
        self.label_title.move(20,10)
        self.label_warning = QtGui.QLabel(self)
        self.label_warning.setText("No Flights are Connected")
        self.label_warning.resize(300,20)
        self.label_warning.move(20,30)

        self.button_next = QtGui.QPushButton('next', self)
        self.button_next.move(210, 40)
        
        if(flight_len > 0):
            self.resize(320, 110)
            self.label1 = QtGui.QLabel(self)
            self.label1.setText("flight "+flight_list[0])
            self.label1.move(120, 40)
            self.rem_f1 = QPushButton('Remove',self)
            self.rem_f1.move(10, 40)
            self.add_f1 = QPushButton('Add',self)
            self.add_f1.move(180, 40)
            self.num_f1 = QtGui.QLabel(self)
            self.num_f1.setText("[0]")
            self.num_f1.move(290, 40)
            self.label_warning.setText("")
            self.label_warning.move(20,90)
            self.rem_f1.clicked.connect(self.c_rem_f1)
            self.add_f1.clicked.connect(self.c_add_f1)
            self.button_next.move(210, 80)

        if(flight_len > 1):
            self.resize(320, 150)
            self.label2 = QtGui.QLabel(self)
            self.label2.setText("flight "+flight_list[1])
            self.label2.move(120, 80)
            self.rem_f2 = QPushButton('Remove',self)
            self.rem_f2.move(10, 80)
            self.add_f2 = QPushButton('Add',self)
            self.add_f2.move(180, 80)
            self.num_f2 = QtGui.QLabel(self)
            self.num_f2.setText("[0]")
            self.num_f2.move(290, 80)
            self.label_warning.setText("")
            self.label_warning.move(20,130)
            self.rem_f2.clicked.connect(self.c_rem_f2)
            self.add_f2.clicked.connect(self.c_add_f2)
            self.button_next.move(210, 120)

        if(flight_len > 2):
            self.resize(320, 190)
            self.label3 = QtGui.QLabel(self)
            self.label3.setText("flight "+flight_list[2])
            self.label3.move(120, 120)
            self.rem_f3 = QPushButton('Remove',self)
            self.rem_f3.move(10, 120)
            self.add_f3 = QPushButton('Add',self)
            self.add_f3.move(180, 120)
            self.num_f3 = QtGui.QLabel(self)
            self.num_f3.setText("[0]")
            self.num_f3.move(290, 120)
            self.label_warning.setText("")
            self.label_warning.move(20,170)
            self.rem_f3.clicked.connect(self.c_rem_f3)
            self.add_f3.clicked.connect(self.c_add_f3)
            self.button_next.move(210, 160)

        if(flight_len > 3):
            self.resize(320, 230)
            self.label4 = QtGui.QLabel(self)
            self.label4.setText("flight "+flight_list[3])
            self.label4.move(120, 160)
            self.rem_f4 = QPushButton('Remove',self)
            self.rem_f4.move(10, 160)
            self.add_f4 = QPushButton('Add',self)
            self.add_f4.move(180, 160)
            self.num_f4 = QtGui.QLabel(self)
            self.num_f4.setText("[0]")
            self.num_f4.move(290, 160)
            self.label_warning.setText("")
            self.label_warning.move(20,210)
            self.rem_f4.clicked.connect(self.c_rem_f4)
            self.add_f4.clicked.connect(self.c_add_f4)
            self.button_next.move(210, 200)

        if(flight_len > 4):
            self.resize(320, 270)
            self.label5 = QtGui.QLabel(self)
            self.label5.setText("flight "+flight_list[4])
            self.label5.move(120, 200)
            self.rem_f5 = QPushButton('Remove',self)
            self.rem_f5.move(10, 200)
            self.add_f5 = QPushButton('Add',self)
            self.add_f5.move(180, 200)
            self.num_f5 = QtGui.QLabel(self)
            self.num_f5.setText("[0]")
            self.num_f5.move(290, 200)
            self.label_warning.setText("")
            self.label_warning.move(20,250)
            self.rem_f5.clicked.connect(self.c_rem_f5)
            self.add_f5.clicked.connect(self.c_add_f5)
            self.button_next.move(210, 240)

        if(flight_len > 5):
            self.resize(320, 310)
            self.label6 = QtGui.QLabel(self)
            self.label6.setText("flight "+flight_list[5])
            self.label6.move(120, 240)
            self.rem_f6 = QPushButton('Remove',self)
            self.rem_f6.move(10, 240)
            self.add_f6 = QPushButton('Add',self)
            self.add_f6.move(180, 240)
            self.num_f6 = QtGui.QLabel(self)
            self.num_f6.setText("[0]")
            self.num_f6.move(290, 240)
            self.label_warning.setText("")
            self.label_warning.move(20,290)
            self.rem_f6.clicked.connect(self.c_rem_f6)
            self.add_f6.clicked.connect(self.c_add_f6)
            self.button_next.move(210, 280)

        if(flight_len > 6):
            self.resize(320, 350)
            self.label7 = QtGui.QLabel(self)
            self.label7.setText("flight "+flight_list[6])
            self.label7.move(120, 280)
            self.rem_f7 = QPushButton('Remove',self)
            self.rem_f7.move(10, 280)
            self.add_f7 = QPushButton('Add',self)
            self.add_f7.move(180, 280)
            self.num_f7 = QtGui.QLabel(self)
            self.num_f7.setText("[0]")
            self.num_f7.move(290, 280)
            self.label_warning.setText("")
            self.label_warning.move(20,330)
            self.rem_f7.clicked.connect(self.c_rem_f7)
            self.add_f7.clicked.connect(self.c_add_f7)
            self.button_next.move(210, 320)

        self.button_next.clicked.connect(self.c_goto_coords)
        self.cd_window = ""
    # next sevon methods connect a drone to the respective flight
    # adds them to list assigned_drones in order of flights input
    def c_add_f1(self):
        global ready_drones
        global assigned_drones
        if(len(ready_drones) != 0):
            assigned_drones[0].append(ready_drones.pop())
            self.num_f1.setText("["+str(len(assigned_drones[0]))+"]")
            print "ready_drones:"
            display_list(ready_drones)
            print "assigned_drones 1:"
            display_list(assigned_drones[0])
        else:
            self.label_warning.setText("No Drones Available")

    def c_add_f2(self):
        global ready_drones
        global assigned_drones
        if(len(ready_drones) != 0):
            assigned_drones[1].append(ready_drones.pop())
            self.num_f2.setText("["+str(len(assigned_drones[1]))+"]")
            print "ready_drones:"
            display_list(ready_drones)
            print "assigned_drones 2:"
            display_list(assigned_drones[1])
        else:
            self.label_warning.setText("No Drones Available")
    
    def c_add_f3(self):
        global ready_drones
        global assigned_drones
        if(len(ready_drones) != 0):
            assigned_drones[2].append(ready_drones.pop())
            self.num_f3.setText("["+str(len(assigned_drones[2]))+"]")
            print "ready_drones:"
            display_list(ready_drones)
            print "assigned_drones 3:"
            display_list(assigned_drones[2])
        else:
            self.label_warning.setText("No Drones Available")


    def c_add_f4(self):
        global ready_drones
        global assigned_drones
        if(len(ready_drones) != 0):
            assigned_drones[3].append(ready_drones.pop())
            self.num_f4.setText("["+str(len(assigned_drones[3]))+"]")
            print "ready_drones:"
            display_list(ready_drones)
            print "assigned_drones 4:"
            display_list(assigned_drones[3])
        else:
            self.label_warning.setText("No Drones Available")


    def c_add_f5(self):
        global ready_drones
        global assigned_drones
        if(len(ready_drones) != 0):
            assigned_drones[4].append(ready_drones.pop())
            self.num_f5.setText("["+str(len(assigned_drones[4]))+"]")
            print "ready_drones:"
            display_list(ready_drones)
            print "assigned_drones 5:"
            display_list(assigned_drones[4])
        else:
            self.label_warning.setText("No Drones Available")


    def c_add_f6(self):
        global ready_drones
        global assigned_drones
        if(len(ready_drones) != 0):
            assigned_drones[5].append(ready_drones.pop())
            self.num_f6.setText("["+str(len(assigned_drones[5]))+"]")
            print "ready_drones:"
            display_list(ready_drones)
            print "assigned_drones 6:"
            display_list(assigned_drones[5])
        else:
            self.label_warning.setText("No Drones Available")


    def c_add_f7(self):
        global ready_drones
        global assigned_drones
        if(len(ready_drones) != 0):
            assigned_drones[6].append(ready_drones.pop())
            self.num_f7.setText("["+str(len(assigned_drones[6]))+"]")
            print "ready_drones:"
            display_list(ready_drones)
            print "assigned_drones 7:"
            display_list(assigned_drones[6])
        else:
            self.label_warning.setText("No Drones Available")

    # removes drones from flights if able
    # removes from assigned_drones and puts back into ready_drones
    def c_rem_f1(self):
        global ready_drones
        global assigned_drones
        if(len(assigned_drones[0]) > 0):
            ready_drones.append(assigned_drones[0].pop())
            self.num_f1.setText("["+str(len(assigned_drones[0]))+"]")
            print "ready_drones:"
            display_list(ready_drones)
            print "assigned_drones 1:"
            display_list(assigned_drones[0])
        else:
            self.label_warning.setText("No Drones Connected")
    

    def c_rem_f2(self):
        global ready_drones
        global assigned_drones
        if(len(assigned_drones[1]) > 0):
            ready_drones.append(assigned_drones[1].pop())
            self.num_f2.setText("["+str(len(assigned_drones[1]))+"]")
            print "ready_drones:"
            display_list(ready_drones)
            print "assigned_drones 2:"
            display_list(assigned_drones[1])
        else:
            self.label_warning.setText("No Drones Connected")

    def c_rem_f3(self):
        global ready_drones
        global assigned_drones
        if(len(assigned_drones[2]) > 0):
            ready_drones.append(assigned_drones[2].pop())
            self.num_f3.setText("["+str(len(assigned_drones[2]))+"]")
            print "ready_drones:"
            display_list(ready_drones)
            print "assigned_drones 3:"
            display_list(assigned_drones[2])
        else:
            self.label_warning.setText("No Drones Connected")

    def c_rem_f4(self):
        global ready_drones
        global assigned_drones
        if(len(assigned_drones[3]) > 0):
            ready_drones.append(assigned_drones[3].pop())
            self.num_f4.setText("["+str(len(assigned_drones[3]))+"]")
            print "ready_drones:"
            display_list(ready_drones)
            print "assigned_drones 4:"
            display_list(assigned_drones[3])
        else:
            self.label_warning.setText("No Drones Connected")

    def c_rem_f5(self):
        global ready_drones
        global assigned_drones
        if(len(assigned_drones[4]) > 0):
            ready_drones.append(assigned_drones[4].pop())
            self.num_f5.setText("["+str(len(assigned_drones[4]))+"]")
            print "ready_drones:"
            display_list(ready_drones)
            print "assigned_drones 5:"
            display_list(assigned_drones[4])
        else:
            self.label_warning.setText("No Drones Connected")

    def c_rem_f6(self):
        global ready_drones
        global assigned_drones
        if(len(assigned_drones[5]) > 0):
            ready_drones.append(assigned_drones[5].pop())
            self.num_f6.setText("["+str(len(assigned_drones[5]))+"]")
            print "ready_drones:"
            display_list(ready_drones)
            print "assigned_drones 6:"
            display_list(assigned_drones[5])
        else:
            self.label_warning.setText("No Drones Connected")

    def c_rem_f7(self):
        global ready_drones
        global assigned_drones
        if(len(assigned_drones[6]) > 0):
            ready_drones.append(assigned_drones[6].pop())
            self.num_f7.setText("["+str(len(assigned_drones[6]))+"]")
            print "ready_drones:"
            display_list(ready_drones)
            print "assigned_drones 7:"
            display_list(assigned_drones[6])
        else:
            self.label_warning.setText("No Drones Connected")
    # createds and initiates cordinate window
    def c_goto_coords(self):
        self.c_window = coord_window(self)
        self.c_window.show()

# window to add coordinates to drones not connected to flights
class coord_window(QtGui.QMainWindow):
    # sets up buttons dynamically to size of ready_drones
    def __init__(self, parent=None):
        global ready_drones
        super(coord_window, self).__init__(parent)
        drone_len = len(ready_drones)

        self.resize(320,80)
        self.setWindowTitle("Add Coordinates")
        self.label_title = QtGui.QLabel(self)
        self.label_title.setText("Add/Remove Drone Coordinates")
        self.label_title.resize(300,20)
        self.label_title.move(20,10)
        self.label_warning = QtGui.QLabel(self)
        self.label_warning.setText("No remaining drones")
        self.label_warning.resize(300,20)
        self.label_warning.move(20,40)
        self.button_next = QtGui.QPushButton('next', self)
        self.button_next.move(210,40)
        self.button_next.clicked.connect(self.goto_start)

        if(drone_len > 0):
            self.resize(320, 155)
            self.label1 = QtGui.QLabel(self)
            self.label1.setText("Drone "+ready_drones[0])
            self.label1.move(20,40)
            self.label1.resize(60,30)
            self.labelx1 = QtGui.QLabel(self)
            self.labelx1.setText("X")
            self.labelx1.move(85,40)
            self.boxx1 = QLineEdit(self)
            self.boxx1.resize(60,30)
            self.boxx1.move(100,40)
            self.labely1 = QtGui.QLabel(self)
            self.labely1.setText("Y")
            self.labely1.move(165,40)
            self.boxy1 = QLineEdit(self)
            self.boxy1.resize(60,30)
            self.boxy1.move(180,40)
            self.labelz1 = QtGui.QLabel(self)
            self.labelz1.setText("Z")
            self.labelz1.move(245,40)
            self.boxz1 = QLineEdit(self)
            self.boxz1.resize(60,30)
            self.boxz1.move(260,40)
            self.add1 = QtGui.QPushButton('add', self)
            self.add1.move(80,80)
            self.rem1 = QtGui.QPushButton('remove most\nrecent', self)
            self.rem1.move(200,80)
            self.label_warning.setText("")
            self.label_warning.move(20,120)
            self.button_next.move(210,120)
            self.rem1.clicked.connect(self.c_rem1)
            self.add1.clicked.connect(self.c_add1)

        if(drone_len > 1):
            self.resize(320, 235)
            self.label2 = QtGui.QLabel(self)
            self.label2.setText("Drone "+ready_drones[1])
            self.label2.move(20,120)
            self.label2.resize(60,20)
            self.labelx2 = QtGui.QLabel(self)
            self.labelx2.setText("X")
            self.labelx2.move(85,120)
            self.boxx2 = QLineEdit(self)
            self.boxx2.resize(60,30)
            self.boxx2.move(100,120)
            self.labely2 = QtGui.QLabel(self)
            self.labely2.setText("Y")
            self.labely2.move(165,120)
            self.boxy2 = QLineEdit(self)
            self.boxy2.resize(60,30)
            self.boxy2.move(180,120)
            self.labelz2 = QtGui.QLabel(self)
            self.labelz2.setText("Z")
            self.labelz2.move(245,120)
            self.boxz2 = QLineEdit(self)
            self.boxz2.resize(60,30)
            self.boxz2.move(260,120)
            self.add2 = QtGui.QPushButton('add', self)
            self.add2.move(80,160)
            self.rem2 = QtGui.QPushButton('remove most\nrecent', self)
            self.rem2.move(200,160)
            self.label_warning.setText("")
            self.label_warning.move(20,200)
            self.button_next.move(210,200)
            self.rem2.clicked.connect(self.c_rem2)
            self.add2.clicked.connect(self.c_add2)

        if(drone_len > 2):
            self.resize(320, 315)
            self.label3 = QtGui.QLabel(self)
            self.label3.setText("Drone "+ready_drones[2])
            self.label3.move(20,200)
            self.label3.resize(60,30)
            self.labelx3 = QtGui.QLabel(self)
            self.labelx3.setText("X")
            self.labelx3.move(85,200)
            self.boxx3 = QLineEdit(self)
            self.boxx3.resize(60,30)
            self.boxx3.move(100,200)
            self.labely3 = QtGui.QLabel(self)
            self.labely3.setText("Y")
            self.labely3.move(165,200)
            self.boxy3 = QLineEdit(self)
            self.boxy3.resize(60,30)
            self.boxy3.move(180,200)
            self.labelz3 = QtGui.QLabel(self)
            self.labelz3.setText("Z")
            self.labelz3.move(245,200)
            self.boxz3 = QLineEdit(self)
            self.boxz3.resize(60,30)
            self.boxz3.move(260,200)
            self.add3 = QtGui.QPushButton('add', self)
            self.add3.move(80,240)
            self.rem3 = QtGui.QPushButton('remove most\nrecent', self)
            self.rem3.move(200,240)
            self.label_warning.setText("")
            self.label_warning.move(20,280)
            self.button_next.move(210,280)
            self.rem3.clicked.connect(self.c_rem3)
            self.add3.clicked.connect(self.c_add3)

        if(drone_len > 3):
            self.resize(320, 395)
            self.label4 = QtGui.QLabel(self)
            self.label4.setText("Drone "+ready_drones[3])
            self.label4.move(20,280)
            self.label4.resize(60,30)
            self.labelx4 = QtGui.QLabel(self)
            self.labelx4.setText("X")
            self.labelx4.move(85,280)
            self.boxx4 = QLineEdit(self)
            self.boxx4.resize(60,30)
            self.boxx4.move(100,280)
            self.labely4 = QtGui.QLabel(self)
            self.labely4.setText("Y")
            self.labely4.move(165,280)
            self.boxy4 = QLineEdit(self)
            self.boxy4.resize(60,30)
            self.boxy4.move(180,280)
            self.labelz4 = QtGui.QLabel(self)
            self.labelz4.setText("Z")
            self.labelz4.move(245,280)
            self.boxz4 = QLineEdit(self)
            self.boxz4.resize(60,30)
            self.boxz4.move(260,280)
            self.add4 = QtGui.QPushButton('add', self)
            self.add4.move(80,320)
            self.rem4 = QtGui.QPushButton('remove most\nrecent', self)
            self.rem4.move(200,320)
            self.label_warning.setText("")
            self.label_warning.move(20,360)
            self.button_next.move(210,360)
            self.rem4.clicked.connect(self.c_rem4)
            self.add4.clicked.connect(self.c_add4)

        if(drone_len > 4):
            self.resize(640, 395)
            self.label5 = QtGui.QLabel(self)
            self.label5.setText("Drone "+ready_drones[4])
            self.label5.move(340,40)
            self.label5.resize(60,30)
            self.labelx5 = QtGui.QLabel(self)
            self.labelx5.setText("X")
            self.labelx5.move(405,40)
            self.boxx5 = QLineEdit(self)
            self.boxx5.resize(60,30)
            self.boxx5.move(420,40)
            self.labely5 = QtGui.QLabel(self)
            self.labely5.setText("Y")
            self.labely5.move(485,40)
            self.boxy5 = QLineEdit(self)
            self.boxy5.resize(60,30)
            self.boxy5.move(500,40)
            self.labelz5 = QtGui.QLabel(self)
            self.labelz5.setText("Z")
            self.labelz5.move(565,40)
            self.boxz5 = QLineEdit(self)
            self.boxz5.resize(60,30)
            self.boxz5.move(580,40)
            self.add5 = QtGui.QPushButton('add', self)
            self.add5.move(400,80)
            self.rem5 = QtGui.QPushButton('remove most\nrecent', self)
            self.rem5.move(520,80)
            self.label_warning.setText("")
            self.label_warning.move(20,360)
            self.button_next.move(530,360)
            self.rem5.clicked.connect(self.c_rem5)
            self.add5.clicked.connect(self.c_add5)

        if(drone_len > 5):
            self.resize(640, 395)
            self.label6 = QtGui.QLabel(self)
            self.label6.setText("Drone "+ready_drones[5])
            self.label6.move(340,120)
            self.label6.resize(60,30)
            self.labelx6 = QtGui.QLabel(self)
            self.labelx6.setText("X")
            self.labelx6.move(405,120)
            self.boxx6 = QLineEdit(self)
            self.boxx6.resize(60,30)
            self.boxx6.move(420,120)
            self.labely6 = QtGui.QLabel(self)
            self.labely6.setText("Y")
            self.labely6.move(485,120)
            self.boxy6 = QLineEdit(self)
            self.boxy6.resize(60,30)
            self.boxy6.move(500,120)
            self.labelz6 = QtGui.QLabel(self)
            self.labelz6.setText("Z")
            self.labelz6.move(565,120)
            self.boxz6 = QLineEdit(self)
            self.boxz6.resize(60,30)
            self.boxz6.move(580,120)
            self.add6 = QtGui.QPushButton('add', self)
            self.add6.move(400,160)
            self.rem6 = QtGui.QPushButton('remove most\nrecent', self)
            self.rem6.move(520,160)
            self.label_warning.setText("")
            self.label_warning.move(20,360)
            self.button_next.move(530,360)
            self.rem6.clicked.connect(self.c_rem6)
            self.add6.clicked.connect(self.c_add6)

        if(drone_len > 6):
            self.resize(640, 395)
            self.label7 = QtGui.QLabel(self)
            self.label7.setText("Drone "+ready_drones[6])
            self.label7.move(340,200)
            self.label7.resize(60,30)
            self.labelx7 = QtGui.QLabel(self)
            self.labelx7.setText("X")
            self.labelx7.move(405,200)
            self.boxx7 = QLineEdit(self)
            self.boxx7.resize(60,30)
            self.boxx7.move(420,200)
            self.labely7 = QtGui.QLabel(self)
            self.labely7.setText("Y")
            self.labely7.move(485,200)
            self.boxy7 = QLineEdit(self)
            self.boxy7.resize(60,30)
            self.boxy7.move(500,200)
            self.labelz7 = QtGui.QLabel(self)
            self.labelz7.setText("Z")
            self.labelz7.move(565,200)
            self.boxz7 = QLineEdit(self)
            self.boxz7.resize(60,30)
            self.boxz7.move(580,200)
            self.add7 = QtGui.QPushButton('add', self)
            self.add7.move(400,240)
            self.rem7 = QtGui.QPushButton('remove most\nrecent', self)
            self.rem7.move(520,240)
            self.label_warning.setText("")
            self.label_warning.move(20,360)
            self.button_next.move(530,360)
            self.rem7.clicked.connect(self.c_rem7)
            self.add7.clicked.connect(self.c_add7)
    # next 7 add coordinates if they are numbers and in the range of 0-10
    def c_add1(self):
        global drone_coords
        try:
            x = float(self.boxx1.text())
            y = float(self.boxy1.text())
            z = float(self.boxz1.text())
            if(x<0 or x>10 or y<0 or y>10 or z<0 or z>10):
                throwanerror
        except:
            self.label_warning.setText("Invalid Parameters")
            return
        drone_coords[0].append((x,y,z))
        print drone_coords[0]
        self.label_warning.setText("")
        self.boxx1.setText("")
        self.boxy1.setText("")
        self.boxz1.setText("")

    def c_add2(self):
        global drone_coords
        try:
            x = float(self.boxx2.text())
            y = float(self.boxy2.text())
            z = float(self.boxz2.text())
            if(x<0 or x>10 or y<0 or y>10 or z<0 or z>10):
                throwanerror
        except:
            self.label_warning.setText("Invalid Parameters")
            return
        drone_coords[1].append((x,y,z))
        print drone_coords[1]
        self.label_warning.setText("")
        self.boxx2.setText("")
        self.boxy2.setText("")
        self.boxz2.setText("")

    def c_add3(self):
        global drone_coords
        try:
            x = float(self.boxx3.text())
            y = float(self.boxy3.text())
            z = float(self.boxz3.text())
            if(x<0 or x>10 or y<0 or y>10 or z<0 or z>10):
                throwanerror
        except:
            self.label_warning.setText("Invalid Parameters")
            return
        drone_coords[2].append((x,y,z))
        print drone_coords[2]
        self.label_warning.setText("")
        self.boxx3.setText("")
        self.boxy3.setText("")
        self.boxz3.setText("")

    def c_add4(self):
        global drone_coords
        try:
            x = float(self.boxx4.text())
            y = float(self.boxy4.text())
            z = float(self.boxz4.text())
            if(x<0 or x>10 or y<0 or y>10 or z<0 or z>10):
                throwanerror
        except:
            self.label_warning.setText("Invalid Parameters")
            return
        drone_coords[3].append((x,y,z))
        print drone_coords[3]
        self.label_warning.setText("")
        self.boxx4.setText("")
        self.boxy4.setText("")
        self.boxz4.setText("")

    def c_add5(self):
        global drone_coords
        try:
            x = float(self.boxx5.text())
            y = float(self.boxy5.text())
            z = float(self.boxz5.text())
            if(x<0 or x>10 or y<0 or y>10 or z<0 or z>10):
                throwanerror
        except:
            self.label_warning.setText("Invalid Parameters")
            return
        drone_coords[4].append((x,y,z))
        print drone_coords[4]
        self.label_warning.setText("")
        self.boxx5.setText("")
        self.boxy5.setText("")
        self.boxz5.setText("")

    def c_add6(self):
        global drone_coords
        try:
            x = float(self.boxx6.text())
            y = float(self.boxy6.text())
            z = float(self.boxz6.text())
            if(x<0 or x>10 or y<0 or y>10 or z<0 or z>10):
                throwanerror
        except:
            self.label_warning.setText("Invalid Parameters")
            return
        drone_coords[5].append((x,y,z))
        print drone_coords[5]
        self.label_warning.setText("")
        self.boxx6.setText("")
        self.boxy6.setText("")
        self.boxz6.setText("")

    def c_add7(self):
        global drone_coords
        try:
            x = float(self.boxx7.text())
            y = float(self.boxy7.text())
            z = float(self.boxz7.text())
            if(x<0 or x>10 or y<0 or y>10 or z<0 or z>10):
                throwanerror
        except:
            self.label_warning.setText("Invalid Parameters")
            return
        drone_coords[6].append((x,y,z))
        print drone_coords[6]
        self.label_warning.setText("")
        self.boxx7.setText("")
        self.boxy7.setText("")
        self.boxz7.setText("")
    # next seven remove coordinates if able
    def c_rem1(self):
        global drone_coords
        if(len(drone_coords[0])>0):
            print "removed:"
            print drone_coords[0].pop()
            self.label_warning.setText("")
            return
        self.label_warning.setText("No Coordinates Set")

    def c_rem2(self):
        global drone_coords
        if(len(drone_coords[1])>0):
            print "removed:"
            print drone_coords[1].pop()
            self.label_warning.setText("")
            return
        self.label_warning.setText("No Coordinates Set")

    def c_rem3(self):
        global drone_coords
        if(len(drone_coords[2])>0):
            print "removed:"
            print drone_coords[2].pop()
            self.label_warning.setText("")
            return
        self.label_warning.setText("No Coordinates Set")

    def c_rem4(self):
        global drone_coords
        if(len(drone_coords[3])>0):
            print "removed:"
            print drone_coords[3].pop()
            self.label_warning.setText("")
            return
        self.label_warning.setText("No Coordinates Set")

    def c_rem5(self):
        global drone_coords
        if(len(drone_coords[4])>0):
            print "removed:"
            print drone_coords[4].pop()
            self.label_warning.setText("")
            return
        self.label_warning.setText("No Coordinates Set")

    def c_rem6(self):
        global drone_coords
        if(len(drone_coords[5])>0):
            print "removed:"
            print drone_coords[5].pop()
            self.label_warning.setText("")
            return
        self.label_warning.setText("No Coordinates Set")

    def c_rem7(self):
        global drone_coords
        if(len(drone_coords[6])>0):
            print "removed:"
            print drone_coords[6].pop()
            self.label_warning.setText("")
            return
        self.label_warning.setText("No Coordinates Set")
    # what would start the 3d visualization and flights, instead
    # prints out all information about the would-be flight
    def goto_start(self):
        global drone_list
        global ready_drones
        global flight_list
        global assigned_drones
        global drone_coords
        print "\nAll drones connected:"
        display_list(drone_list)
        print "\nAll flight paths w/ drones connected:"
        i = 0
        while(i < len(flight_list)):
            print "flight path:"
            print flight_list[i]
            print "drones connected to fp:"
            display_list(assigned_drones[i])
            i += 1
        print "\ndrones with coordinates:"
        i = 0
        while(i < len(ready_drones)):
            print "drone:"
            print ready_drones[i]
            print "coordinates:"
            print drone_coords[i]
            i += 1
        QtCore.QCoreApplication.instance().quit()
# main innitiates the first GUI window        
def main():
    app = QtGui.QApplication(sys.argv)
    start = drone_window()
    start.show()
    sys.exit(app.exec_())
# displays a list of strings
def display_list(list):
    i = 0
    display = ""
    while i < len(list):
        display += list[i] + " "
        i += 1
    print display
    
if __name__ == "__main__":
    main()
