import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

drone_counter = 0
drone_list = []
ready_drones = []
flight_list = []
flight_counter = 0
a = ''

def main():
    drone_module()

def drone_module():
    global textbox_drones
    global drone_list
    global a
    a = QApplication(sys.argv)
    w = QWidget()
    vbox = QVBoxLayout()
    w.resize(320,120)
    w.setWindowTitle("Add/Remove Drones")

    label_drones = QLabel()
    label_drones.setText("Enter a drone id:")
    label_drones.setAlignment(Qt.AlignLeft)

    textbox_drones = QLineEdit(w)
    textbox_drones.resize(280,40)
    textbox_drones.setAlignment(Qt.AlignCenter)

    button_add = QPushButton('Add Drone', w)

    button_remove = QPushButton('Remove Drone', w)

    button_goto_flight = QPushButton('Next', w)
    
    vbox.addWidget(label_drones)
    vbox.addWidget(textbox_drones)
    vbox.addWidget(button_add)
    vbox.addWidget(button_remove)
    vbox.addWidget(button_goto_flight)
    
    button_add.clicked.connect(add_drone_click) 

    button_remove.clicked.connect(remove_drone_click)

    button_goto_flight.clicked.connect(goto_flight)
    
    w.setLayout(vbox)

    w.show()

    sys.exit(a.exec_())

def flight_module():
    a = QApplication(sys.argv)
    w = QWidget()
    vbox = QVBoxLayout()
    w.resize(320,120)
    w.setWindowTitle("Add/Remove Flight Path")

    label_fp = QLabel()
    label_fp.setText('"Select" a Flight Path:')
    label_fp.setAlignment(Qt.AlignLeft)

    textbox_fp = QLineEdit(w)
    textbox_fp.resize(280,40)
    textbox_fp.setAlignment(Qt.AlignCenter)

    button_add = QPushButton('Add Flight Path', w)

    button_remove = QPushButton('Remove Flight Path', w)

    button_goto_connect = QPushButton('Next', w)
    
    vbox.addWidget(label_fp)
    vbox.addWidget(textbox_fp)
    vbox.addWidget(button_add)
    vbox.addWidget(button_remove)
    vbox.addWidget(button_goto_connect)
    
    button_add.clicked.connect(add_flight_click) 

    button_remove.clicked.connect(remove_flight_click)

    button_goto_connect.clicked.connect(goto_connect)
    
    w.setLayout(vbox)

    w.show()

    sys.exit(a.exec_())
    return
    
@pyqtSlot()
def add_drone_click():
    global drone_list
    global drone_counter
    global textbox_drones
    curr_drone = textbox_drones.text()
    if(curr_drone == ""):
        return
    if(curr_drone in drone_list):
        print "Drone already added"
    elif(drone_counter < 7):
        drone_list.append(curr_drone)
        drone_counter += 1
        display_list(drone_list)
    else:
        print("Max number of drones set")
    textbox_drones.setText("")

@pyqtSlot()
def remove_drone_click():
    global textbox_drones
    global drone_list
    global drone_counter
    curr_drone = textbox_drones.text()
    if(curr_drone == ""):
        return
    if(curr_drone in drone_list):
        drone_list.remove(curr_drone)
        drone_counter -= 1
    else:
        print "Drone not connected"
    display_list(drone_list)
    textbox_drones.setText("")

@pyqtSlot()
def goto_flight():
    global drone_list
    global ready_drones
    global a
    a.exit()
    ready_drones = drone_list[0:]
    flight_module()
  
@pyqtSlot()
def add_flight_click():
    global flight_list
    global flight_counter
    global textbox_fp
    curr_flight = textbox_drones.text()
    if(curr_flight in flight_list):
        print "Flight already added"
    elif(flight_counter < 7):
        flight_list.append(curr_flight)
        flight_counter += 1
        display(flight_list)
    else:
        print("Max number of flights set")
    textbox_fp.setText("")

@pyqtSlot()
def remove_flight_click():
    global textbox_fp
    global flight_list
    global flight_counter
    curr_flight = textbox_fp.text()
    if(curr_flight in flight_list):
        flight_list.remove(curr_flight)
        flight_counter -= 1
    else:
        print "Flight not connected"
    display_list(flight_list)
    textbox_fp.setText("")

@pyqtSlot()
def goto_connect():
    global drone_list
    global ready_drones
    print "to do"

def display_list(list):
    i = 0
    display = ""
    while i < len(list):
        display += list[i] + " "
        i += 1
    print display
        
if __name__ == "__main__":
    main()
