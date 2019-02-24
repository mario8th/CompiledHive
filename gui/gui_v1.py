import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MainWindow(QMainWindow):
   count = 0
	
   def __init__(self, parent = None):
      super(MainWindow, self).__init__(parent)
      self.mdi = QMdiArea()
      self.mdi.resize(1000,1000)
      self.setCentralWidget(self.mdi)
      self.setWindowTitle("GUI Demo 2")
      self.mdi.tileSubWindows()
      
      coords_sub = coordinates()
      self.mdi.addSubWindow(coords_sub)
      coords_sub.show()

      connect_sub = connect_drone_to_fp()
      self.mdi.addSubWindow(connect_sub)
      connect_sub.show()
      
      flight_sub = fp_select()
      self.mdi.addSubWindow(flight_sub)
      flight_sub.show()
         
      drone_sub = drone_select()
      self.mdi.addSubWindow(drone_sub)
      drone_sub.show()
      
      flight_sub2 = fp_select()
      self.mdi.addSubWindow(flight_sub2)
      flight_sub2.show()
      

class drone_select(QtGui.QMdiSubWindow):
    def __init__(self, parent=None):
        super(drone_select, self).__init__(parent)
        self.resize(320,160)
        self.setWindowTitle("Add/Remove Drones")
        self.label_drones = QtGui.QLabel(self)
        self.label_drones.setText("Enter a drone id:")
        self.label_drones.move(20, 25)
        self.label_drones.resize(110, 20)

        self.textbox_drones = QLineEdit(self)
        self.textbox_drones.resize(60, 40)
        self.textbox_drones.move(20, 50)

        self.button_add = QPushButton('Add Drone', self)
        self.button_add.move(90, 55)
        self.button_add.clicked.connect(self.add_drone_click)
        
        self.drone_combo = QComboBox(self)
        self.drone_combo.move(20, 95)
        self.drone_combo.resize(60,40)
        self.drone_combo.addItem("")
        self.drone_combo.addItem("ID:A")
        self.drone_combo.addItem("ID:B")

        self.button_remove = QPushButton('Remove Drone', self)
        self.button_remove.move(90, 100)
        self.button_remove.clicked.connect(self.remove_drone_click)

    def add_drone_click(self):
       print("adding drone")

    def remove_drone_click(self):
       drone_id = str(self.drone_combo.currentText())
       drone_index = self.drone_combo.currentIndex()
       print "removing drone {}".format(drone_id)
       self.drone_combo.removeItem(drone_index)

class fp_select(QtGui.QMdiSubWindow):
    # same as previous, but different names
    def __init__(self, parent=None):
        super(fp_select, self).__init__(parent)
        self.resize(320, 160)
        self.setWindowTitle("Add/Remove Flight Path")

        self.label_fp = QLabel(self)
        self.label_fp.setText("Enter a flight path:")
        self.label_fp.move(20, 25)
        self.label_fp.resize(180, 20)

        self.textbox_fp = QLineEdit(self)
        self.textbox_fp.resize(280, 40)
        self.textbox_fp.move(20, 30)

        self.button_add = QPushButton('Add Flight Path', self)
        self.button_add.move(20, 80)
        
        self.button_remove = QPushButton('Remove Flight Path', self)
        self.button_remove.move(200, 80)

class connect_drone_to_fp(QtGui.QMdiSubWindow):
   def __init__(self, parent=None):
      super(connect_drone_to_fp, self).__init__(parent)
      self.setWindowTitle("Connect Drones")
      self.label_fp = QtGui.QLabel(self)
      self.label_fp.setText("Select Flight Path:")
      self.label_fp.resize(150, 20)
      self.label_fp.move(20,25)
      self.combo_fp = QtGui.QComboBox(self)
      self.combo_fp.resize(110, 40)
      self.combo_fp.move(20, 45)

      self.label_connect = QtGui.QLabel(self)
      self.label_connect.setText("Select Drone:")
      self.label_connect.resize(150, 20)
      self.label_connect.move(150 ,25)
      self.combo_connect = QtGui.QComboBox(self)
      self.combo_connect.resize(110,40)
      self.combo_connect.move(150, 45)
      self.buttn_connect = QtGui.QPushButton('Add', self)
      self.buttn_connect.move(150, 90)
      self.buttn_connect.resize(110, 30)

      self.label_remove = QtGui.QLabel(self)
      self.label_remove.setText("Select Drone:")
      self.label_remove.resize(150, 20)
      self.label_remove.move(280, 25)
      self.combo_remove = QtGui.QComboBox(self)
      self.combo_remove.resize(110, 40)
      self.combo_remove.move(280, 45)
      self.buttn_remove = QtGui.QPushButton("Remove", self)
      self.buttn_remove.move(280, 90)
      self.buttn_remove.resize(110, 30)
        
class coordinates(QtGui.QMdiSubWindow):
   def __init__(self, parent=None):
      super(coordinates, self).__init__(parent)
      self.setWindowTitle("Connect Coordinates to Drones")

      self.label_drone = QtGui.QLabel(self)
      self.label_drone.setText("Choose Drone:")
      self.label_drone.resize(150, 20)
      self.label_drone.move(20, 25)
      self.combo_drone = QtGui.QComboBox(self)
      self.combo_drone.resize(110, 40)
      self.combo_drone.move(20, 45)
      self.label_coord = QtGui.QLabel(self)
      self.label_coord.setText("Enter Coordinate:")
      self.label_coord.resize(120, 20)
      self.label_coord.move(145, 25)
      self.label_x = QtGui.QLabel(self)
      self.label_x.move(145, 50)
      self.label_x.setText('X:')
      self.textbox_x = QtGui.QLineEdit(self)
      self.textbox_x.resize(60, 40)
      self.textbox_x.move(160, 45)
      self.label_y = QtGui.QLabel(self)
      self.label_y.setText("Y:")
      self.label_y.move(230, 50)
      self.textbox_y = QtGui.QLineEdit(self)
      self.textbox_y.resize(60, 40)
      self.textbox_y.move(245, 45)
      self.label_z = QtGui.QLabel(self)
      self.label_z.setText('Z:')
      self.label_z.move(315, 50)
      self.textbox_z = QtGui.QLineEdit(self)
      self.textbox_z.resize(60, 40)
      self.textbox_z.move(330, 45)
      self.add_coord = QtGui.QPushButton("Add", self)
      self.add_coord.move(160, 95)

      self.label_coord = QtGui.QLabel(self)
      self.label_coord.setText('Select Coordinate:')
      self.label_coord.resize(130, 20)
      self.label_coord.move(20, 120)
      self.combo_coord = QtGui.QComboBox(self)
      self.combo_coord.resize(110, 40)
      self.combo_coord.move(20, 140)
      self.rem_coord = QtGui.QPushButton('Remove', self)
      self.rem_coord.move(140, 145)

def main():
    app = QtGui.QApplication(sys.argv)
    start = MainWindow()
    start.resize(1000,1000)
    start.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
