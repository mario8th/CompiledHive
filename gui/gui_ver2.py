import sys
import re
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from functools import partial


#==============================================================================
class WidgetGallery(QtGui.QDialog):
    count = 0
    def get_data(self):
      drone_count = 1.0
      for drone in self.drone_coords:
         self.drone_coords[drone] = [(drone_count, 0, 0)] + self.drone_coords[drone]
         drone_count = round(drone_count + .3,2)
      return (self.drones_connected, self.fp_connected, self.drone_coords, self.object_dict)

    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.dronesConnected = {}
        self.dronesAvailable = []
        self.fpConnected = {}
        self.droneCoords = {}
        self.objectDict = {}
        self.fileNames = "flights.txt"
        #self.flights = []
        self.flightList = QtGui.QListView()
      
        self.originalPalette = QtGui.QApplication.palette()

        styleComboBox = QtGui.QComboBox()
        styleComboBox.addItems(QtGui.QStyleFactory.keys())

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftGroupBox()
        self.createBottomRightGroupBox()

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftGroupBox, 2, 0)
        mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("CrazySwarm Flight Setup")
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Plastique'))
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QtGui.QGroupBox("Flight Paths")
        self.flightList = QtGui.QListView()
        self.model = QStandardItemModel(self.flightList)
        
        uploadButton = QtGui.QPushButton("Upload")
        uploadButton.clicked.connect(self.uploadClick)
        removeButton = QtGui.QPushButton("Remove")
        removeButton.clicked.connect(self.removeClick)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.flightList)
        layout.addWidget(uploadButton)
        layout.addWidget(removeButton)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def uploadClick(self):
      message = QMessageBox()
      self.currentFile = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
      temp = self.getFileName(self.currentFile)
      #checks if file is import if so error message
      if self.checkFileImportant(str(temp))  == False:
          #check file is python file
          if temp[-2:] == 'py':
             temp = temp.remove(".py")
             #if self.check_for_file(str(temp)) == False:
             #self.flights.append(temp)
             # create an item with a caption
             item = QStandardItem(temp)
             # Add the item to the model
             self.model.appendRow(item)
             # Apply the model to the list view
             self.flightList.setModel(self.model)
             temp = str(temp)
             #self.fp_connected[temp] = []
             file = open(self.fileNames, 'a')
             file.write(" " + temp)
             file.close()
             self.createFile(temp)
          else:
             message.setText("File must be python file ")
             message.setWindowTitle("Error")

             message.setStandardButtons(QMessageBox.Ok)
             retval = message.exec_()
      else:
          #user selects invalid file name or fie that will mess up progrram
          message.setText("Not valid file name and or file")
          message.setWindowTitle("Error Message")

          message.setStandardButtons(QMessageBox.Ok)
          retval = message.exec_()
      return
    
    def getFileName(self, myFile):
        temp = myFile
        if temp.contains("/") == True:
            temp = temp.section('/', -1)
        return temp

    def checkFileImportant(self, myFile):
        important = False
        if myFile.lower() == "gui.py":
            important = True
        if myFile.lower() == "backend.py":
            important = True
        if myFile.lower() == "control_node.py":
            important = True
        if myFile.lower() == "simulator.py":
            important = True
        if myFile.lower() == "visros.py":
            important = True
        return important

    def createFile(self, myFile):
        with open(self.currentFile) as fileIn:
            with open(myFile + ".py", "w") as fileOut:
                for line in fileIn:
                   fileOut.write(line)
        return
    
    def removeClick(self):
      file = open(self.fileNames, 'r+')
      temp_line = ""
      for line in file:
        temp = line.split(" ")
        index = 0;
        for value in temp:
           if value != '':
               if value == self.getFileName(self.currentFile.remove(".py")):
                   #TO DO remove file from computer=
                   #self.flightList.model().removeRow(index)
                   #self.flightList.setModel(self.model)
                   print index
                   print str(self.model)
                   #print str(self.model.index(0,0))
                   self.model.removeRow(index)
                   # Apply the model to the list view
                   self.flightList.setModel(self.model)
                   #remove file name from line and save to line
                   temp_line = re.sub(value, "", line)
                   print temp_line
               else:
                   index += 1
      #close and open as write to write over file
      file.close()
      file = open(self.fileNames, 'w')
      file.write(temp_line)
      file.close()
      return

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QtGui.QGroupBox("Drones")
        self.droneList = QtGui.QListView()
        self.model2 = QStandardItemModel(self.droneList)
        
        uploadButton = QtGui.QPushButton("Add")
        uploadButton.clicked.connect(self.addDroneClick)
        removeButton = QtGui.QPushButton("Remove")
        removeButton.clicked.connect(self.removeDroneClick)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.droneList)
        layout.addWidget(uploadButton)
        layout.addWidget(removeButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def addDroneClick(self):
        self.droneWin = WidgetDrone()
        self.droneWin.show()
        return

    def editDroneClick(self):
        self.droneSettings = WidgetDrone()
        self.droneSettings.show()
        return
        
    def removeDroneClick(self):
        self.model2.appendRow(self)
        self.droneList.setModel(self.model2)
        return

    def createBottomLeftGroupBox(self):
        self.bottomLeftGroupBox = QtGui.QGroupBox("Obstacles")
        self.obsList = QtGui.QListView()
        self.model3 = QStandardItemModel(self.obsList)
        
        uploadButton = QtGui.QPushButton("Add")
        uploadButton.clicked.connect(self.addObstaclesClick)
        removeButton = QtGui.QPushButton("Remove")
        removeButton.clicked.connect(self.removeDroneClick)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.obsList)
        layout.addWidget(uploadButton)
        layout.addWidget(removeButton)
        self.bottomLeftGroupBox.setLayout(layout)
        
    #def addCoordinateClick(currDrone, self):
        
    def addObstaclesClick(self):
        self.obsWin = WidgetObs(self)
        self.obsWin.show()
        return

    def updateObs(self, name, coord1, coord2):
        self.objectDict[name] = (coord1, coord2)
        item = QStandardItem(name)
        self.modelObs.appendRow(item)
        self.obsList.setModel(self.modelObs)
        return
        
    
    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QtGui.QGroupBox()
        ToggleVisButton = QtGui.QPushButton("Open Visualzation")
        ToggleVisButton.clicked.connect(self.openVis)
        ToggleLogButton = QtGui.QPushButton("Open Log FileS")
        ToggleLogButton.clicked.connect(self.openLog)
        
        startButton = QtGui.QPushButton("Start Flight")
        startButton.clicked.connect(self.startFlight)

        layout = QtGui.QGridLayout()
        layout.addWidget(ToggleVisButton)
        layout.addWidget(ToggleLogButton)
        layout.addWidget(startButton)
        self.bottomRightGroupBox.setLayout(layout)
        
    def startFlight(self):
        print self.dronesConnected
        print self.dronesAvailable
        print self.fpConnected
        print self.droneCoords
        print self.objectDict
        self.close()

    def openVis(self):
        self.visWin = toggle_vis_window()
        self.visWin.show()
        return
        
    def openLog(self):
        self.logWin = toggle_log_window()
        self.logWin.show()
        return
#==============================================================================
class WidgetObs(WidgetGallery, QtGui.QDialog):
     def __init__(self, parent=WidgetGallery):
        super(WidgetGallery, self).__init__(parent)
        self.originalPalette = QtGui.QApplication.palette()
        #self.flightList = WidgetGallery.self.flightList
        self.version = WidgetGallery
        self.setWindowTitle("Obstacle Setup")

        styleComboBox = QtGui.QComboBox()
        styleComboBox.addItems(QtGui.QStyleFactory.keys())

        self.createObsInfoBox()

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.obsInfoBox)
        self.setLayout(mainLayout)
        
     def createObsInfoBox(self):
        self.obsInfoBox = QtGui.QGroupBox("Obstacle Informations")
        obsNameLabel = QtGui.QLabel("Enter a obstacle name:")
        self.obsName = QLineEdit()
        
        obsCorLabel1 = QtGui.QLabel("Enter a obstacle coordinates 1 (format: x,y,z):")
        self.obsCor1 =  QLineEdit()
        obsCorLabel2 = QtGui.QLabel("Enter a obstacle coordinates 2 (format: x,y,z):")
        self.obsCor2 =  QLineEdit()

        addButton = QtGui.QPushButton("Add")
        addButton.clicked.connect(self.addClick)

        cancelButton = QtGui.QPushButton("Cancel")
        cancelButton.clicked.connect(self.cancelClick)

        layout = QtGui.QGridLayout()

        layout.addWidget(obsNameLabel)
        layout.addWidget(self.obsName)
        layout.addWidget(obsCorLabel1)
        layout.addWidget(self.obsCor1)
        layout.addWidget(obsCorLabel2)
        layout.addWidget(self.obsCor2)
        layout.addWidget(addButton)
        layout.addWidget(cancelButton)
        self.obsInfoBox.setLayout(layout)
        
     def cancelClick(self):
         self.close()
         return
         
     def addClick(self):
        message = QMessageBox()
        if self.obsName.text() != "" and self.obsCor1.text() != "" and self.obsCor2.text() != "":
            name = self.obsName.text()
            coord1 = (self.obsCor1.text()).split(',')
            coord2 = (self.obsCor2.text()).split(',')
        else:
            message.setText("Missing information please enter a name and two coordinates.")
            message.setWindowTitle("Error Message")
            message.setStandardButtons(QMessageBox.Ok)
            retval = message.exec_()
            return
        try:
            x1Coord = float(coord1[0])
            x2Coord = float(coord2[0])
            y1Coord = float(coord1[1])
            y2Coord = float(coord2[1])
            z1Coord = float(coord1[2])
            z2Coord = float(coord2[2])
        except:
            message.setText("Invaild format please retry again.Please try agin using format: x,y,z")
            message.setWindowTitle("Error Message")
            message.setStandardButtons(QMessageBox.Ok)
            retval = message.exec_()
            return
        x1Bool = x1Coord >= 0 and x1Coord <= 3.4
        y1Bool = y1Coord >= 0 and y1Coord <= 4.25
        z1Bool = z1Coord >= 0 and z1Coord <= 2.43
        x2Bool = x2Coord >= 0 and x2Coord <= 3.4
        y2Bool = y2Coord >= 0 and y2Coord <= 4.25
        z2Bool = z2Coord >= 0 and z2Coord <= 2.43
        if x1Bool and x2Bool and y1Bool and y2Bool and z1Bool and z2Bool:
            WidgetGallery.updateObs(self.version, name, coord1, coord2)
            self.close()
        else:
            message.setText("Obstacles coordinates out of range.")
            message.setWindowTitle("Error Message")
            message.setStandardButtons(QMessageBox.Ok)
            retval = message.exec_()
            return
        return
#==============================================================================

class WidgetDrone(WidgetGallery, QtGui.QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        self.originalPalette = QtGui.QApplication.palette()
        #self.flightList = WidgetGallery.self.flightList
        self.setWindowTitle("Drone Setup")
        
        styleComboBox = QtGui.QComboBox()
        styleComboBox.addItems(QtGui.QStyleFactory.keys())

        self.createFileBox()
        self.createCoordinatesBox()
        self.createDroneInfoBox()

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.droneInfoBox)
        mainLayout.addWidget(self.coordinatesBox)
        mainLayout.addWidget(self.fileBox)
        self.setLayout(mainLayout)

    def createDroneInfoBox(self):
        self.droneInfoBox = QtGui.QGroupBox("Drones Informations")
        droneNameLabel = QtGui.QLabel("Enter a drone name:")
        self.droneName = QLineEdit()
        
        droneIDLabel = QtGui.QLabel("Enter a drone id:")
        self.droneID =  QLineEdit()
        droneChoiceLabel = QtGui.QLabel("File or coordinates:")
        self.choiceComboBox = QtGui.QComboBox()
        self.choiceComboBox.addItems(["Please Select","Flight File","Coordinates"])
        self.coordinatesBox.setDisabled(True)
        self.fileBox.setDisabled(True)
        self.choiceComboBox.activated[str].connect(self.disableBox)

        layout = QtGui.QGridLayout()

        layout.addWidget(droneNameLabel)
        layout.addWidget(self.droneName)
        layout.addWidget(droneIDLabel)
        layout.addWidget(self.droneID)
        layout.addWidget(droneChoiceLabel)
        layout.addWidget(self.choiceComboBox)
        self.droneInfoBox.setLayout(layout)
        
    def disableBox(self):
        if self.choiceComboBox.currentText() == "Flight File":
            self.fileBox.setDisabled(False)
            self.coordinatesBox.setDisabled(True)
        elif self.choiceComboBox.currentText() == "Please Select":
            self.coordinatesBox.setDisabled(True)
            self.coordinatesBox.setDisabled(True)
        else:
            self.fileBox.setDisabled(True)
            self.coordinatesBox.setDisabled(False)
        return
    
    def cancelClick(self):
         self.close()
         return
    def removeClick(self):
         print "TO DO REMOVE COORDINATE"
         self.close()
         return
        
    def fileClick(self):
        message = QMessageBox()
        self.close()
        return

    def corClick(self):
        message = QMessageBox()
        if self.droneName.text().remove(" ") != "":
            if self.droneID.text().remove(" ") != "":
                if self.checkCor() == True:
                    item = QStandardItem(self.droneCor.text())
                    self.corModel.appendRow(item)
                    self.droneCorList.setModel(self.corModel)
            else:
                message.setText("Please enter a ID for the drone")
                message.setWindowTitle("Error Message")
                message.setStandardButtons(QMessageBox.Ok)
                retval = message.exec_()
        else:
            message.setText("Please enter a name for the drone")
            message.setWindowTitle("Error Message")
            message.setStandardButtons(QMessageBox.Ok)
            retval = message.exec_()
        return

    def checkCor(self):
        message = QMessageBox()
        print self.droneCor.text()
        if self.droneCor.text() != "":
            coord = (self.droneCor.text()).split(',')
        else:
                message.setText("Please enter coordinatess for the drone in x,z,y format")
                message.setWindowTitle("Error Message")
                message.setStandardButtons(QMessageBox.Ok)
                retval = message.exec_()
                return False
        try:
            x1Coord = float(coord[0])
            y1Coord = float(coord[1])
            z1Coord = float(coord[2])

        except:
            message.setText("Invaild format please retry again.Please try agin using format: x,y,z")
            message.setWindowTitle("Error Message")
            message.setStandardButtons(QMessageBox.Ok)
            retval = message.exec_()
            return False
        x1Bool = x1Coord >= 0 and x1Coord <= 3.4
        y1Bool = y1Coord >= 0 and y1Coord <= 4.25
        z1Bool = z1Coord >= 0 and z1Coord <= 2.43
        if x1Bool and y1Bool and z1Bool:
            #WidgetGallery update
            self.close()
        else:
            message.setText("Drone coordinates out of range.")
            message.setWindowTitle("Error Message")
            message.setStandardButtons(QMessageBox.Ok)
            retval = message.exec_()
            return False
        return True
    
        
    def createFileBox(self):
        self.fileBox = QtGui.QGroupBox("Fight Path File")
        fileNameLabel = QtGui.QLabel("Select a flight path file:")
        droneFile = QtGui.QComboBox()
        file = open("flights.txt", 'r+')
        for line in file:
            temp = line.split(" ")
            for name in temp:
                if name != "":
                    droneFile.addItem(name)
                
        fileButton = QtGui.QPushButton("Done")
        fileButton.clicked.connect(self.fileClick)        
        cancelButton = QtGui.QPushButton("Cancel")
        cancelButton.clicked.connect(self.cancelClick)
            

        layout = QtGui.QGridLayout()

        layout.addWidget(droneFile)
        layout.addWidget(fileButton)
        layout.addWidget(cancelButton)
        self.fileBox.setLayout(layout)
        
    def createCoordinatesBox(self):
        self.coordinatesBox = QtGui.QGroupBox("Drone Coordinates")
        self.droneCorList = QtGui.QListView()
        self.corModel = QStandardItemModel(self.droneCorList)
        droneCorLabel = QtGui.QLabel("Enter a drone coordinates using x,y,z format:")
        self.droneCor =  QLineEdit()

        corButton = QtGui.QPushButton("Add")
        corButton.clicked.connect(self.corClick)
        removeButton = QtGui.QPushButton("Remove")
        removeButton.clicked.connect(self.removeClick)
        closeButton = QtGui.QPushButton("Close")
        closeButton.clicked.connect(self.cancelClick)
        
        layout = QtGui.QGridLayout()
        layout.addWidget(self.droneCorList)
        layout.addWidget(droneCorLabel)
        layout.addWidget(self.droneCor)
        layout.addWidget(corButton)
        layout.addWidget(removeButton)
        layout.addWidget(closeButton)
        
        self.coordinatesBox.setLayout(layout)
#==============================================================================
class toggle_vis_window(QtGui.QMainWindow):
   def __init__(self, parent=None):
      super(toggle_vis_window, self).__init__(parent)
      self.resize(250, 185)
      self.file= "vis_config.txt"
       
      self.main_label = QtGui.QLabel(self)
      self.main_label.setText('Toggle Elements Shown in Visualzation')
      self.main_label.resize(300, 20)
      self.setWindowTitle('Toggle Visualization')

      self.vis_group = QButtonGroup()
      self.vis_on = QRadioButton('On', self)
      self.vis_on.move(20,20)
      self.vis_off = QRadioButton('Off', self)
      self.vis_off.move(60,20)
      self.vis_group.addButton(self.vis_on, 0)
      self.vis_group.addButton(self.vis_off, 0)
      self.vis_label = QtGui.QLabel(self)
      self.vis_label.setText('Visualization')
      self.vis_label.resize(200,20)
      self.vis_label.move(105, 25)

      self.drone_loc_group = QButtonGroup()
      self.drone_loc_on = QRadioButton('On', self)
      self.drone_loc_on.move(20,40)
      self.drone_loc_off = QRadioButton('Off', self)
      self.drone_loc_off.move(60,40)
      self.drone_loc_off.setChecked(True)
      self.drone_loc_group.addButton(self.drone_loc_on, 0)
      self.drone_loc_group.addButton(self.drone_loc_off, 0)
      self.drone_loc_label = QtGui.QLabel(self)
      self.drone_loc_label.setText('Drone Locations')
      self.drone_loc_label.resize(200,20)
      self.drone_loc_label.move(105, 45)

      self.drone_path_group = QButtonGroup()
      self.drone_path_on = QRadioButton('On', self)
      self.drone_path_on.move(20,60)
      self.drone_path_off = QRadioButton('Off', self)
      self.drone_path_off.move(60,60)
      self.drone_path_off.setChecked(True)
      self.drone_path_group.addButton(self.drone_path_on, 0)
      self.drone_path_group.addButton(self.drone_path_off, 0)
      self.drone_path_label = QtGui.QLabel(self)
      self.drone_path_label.setText('Drone Paths Expected')
      self.drone_path_label.resize(200,20)
      self.drone_path_label.move(105, 65)

      self.drone_flown_group = QButtonGroup()
      self.drone_flown_on = QRadioButton('On', self)
      self.drone_flown_on.move(20,80)
      self.drone_flown_off = QRadioButton('Off', self)
      self.drone_flown_off.move(60,80)
      self.drone_flown_off.setChecked(True)
      self.drone_flown_group.addButton(self.drone_flown_on, 0)
      self.drone_flown_group.addButton(self.drone_flown_off, 0)
      self.drone_flown_label = QtGui.QLabel(self)
      self.drone_flown_label.setText('Drone Paths Flown')
      self.drone_flown_label.resize(200,20)
      self.drone_flown_label.move(105, 85)

      self.sensor_group = QButtonGroup()
      self.sensor_on = QRadioButton('On', self)
      self.sensor_on.move(20,100)
      self.sensor_off = QRadioButton('Off', self)
      self.sensor_off.move(60,100)
      self.sensor_off.setChecked(True)
      self.sensor_group.addButton(self.sensor_on, 0)
      self.sensor_group.addButton(self.sensor_off, 0)
      self.sensor_label = QtGui.QLabel(self)
      self.sensor_label.setText('Sensors')
      self.sensor_label.resize(200,20)
      self.sensor_label.move(105, 105)

      self.objects_group = QButtonGroup()
      self.objects_on = QRadioButton('On', self)
      self.objects_on.move(20,120)
      self.objects_off = QRadioButton('Off', self)
      self.objects_off.move(60,120)
      self.objects_off.setChecked(True)
      self.objects_group.addButton(self.objects_on, 0)
      self.objects_group.addButton(self.objects_off, 0)
      self.objects_label = QtGui.QLabel(self)
      self.objects_label.setText('Objects')
      self.objects_label.resize(200,20)
      self.objects_label.move(105, 125)
      self.save = QPushButton('save', self)
      self.save.move(130, 150)
      self.save.clicked.connect(self.save_vis_config)
      self.open_vis_config()

   def open_vis_config(self):
      config = open(self.file, 'r')
      line = config.readline().strip()
      if line == 'on':
         self.vis_on.setChecked(True)
      else:
         self.vis_off.setChecked(True)
      line = config.readline().strip()
      if line == 'on':
         self.drone_loc_on.setChecked(True)
      else:
         self.drone_loc_off.setChecked(True)
      line = config.readline().strip()
      if line == 'on':
         self.drone_path_on.setChecked(True)
      else:
         self.drone_path_off.setChecked(True)
      line = config.readline().strip()
      if line == 'on':
         self.drone_flown_on.setChecked(True)
      else:
         self.drone_flown_off.setChecked(True)
      line = config.readline().strip()
      if line == 'on':
         self.sensor_on.setChecked(True)
      else:
         self.sensor_off.setChecked(True)
      line = config.readline().strip()
      if line == 'on':
         self.objects_on.setChecked(True)
      else:
         self.objects_off.setChecked(True)
      config.close()
      return

   def save_vis_config(self):
      config = open(self.file, 'w')
      if self.vis_on.isChecked():
         config.write('on\n')
      else:
         config.write('off\n')
      if self.drone_loc_on.isChecked():
         config.write('on\n')
      else:
         config.write('off\n')
      if self.drone_path_on.isChecked():
         config.write('on\n')
      else:
         config.write('off\n')
      if self.drone_flown_on.isChecked():
         config.write('on\n')
      else:
         config.write('off\n')
      if self.sensor_on.isChecked():
         config.write('on\n')
      else:
         config.write('off\n')
      if self.objects_on.isChecked():
         config.write('on\n')
      else:
         config.write('off\n')
      config.close()
      return
#==============================================================================
class toggle_log_window(QtGui.QMainWindow):
   def __init__(self, parent=None):
      super(toggle_log_window, self).__init__(parent)
      self.resize(250, 230)
      self.main_label = QtGui.QLabel(self)
      self.main_label.setText('Toggle Elements Logged')
      self.main_label.resize(300, 20)
      self.setWindowTitle('Toggle Log File')

      self.log_group = QButtonGroup()
      self.log_on = QRadioButton('On', self)
      self.log_on.move(20,20)
      self.log_off = QRadioButton('Off', self)
      self.log_off.move(60,20)
      self.log_off.setChecked(True)
      self.log_group.addButton(self.log_on, 0)
      self.log_group.addButton(self.log_off, 0)
      self.log_label = QtGui.QLabel(self)
      self.log_label.setText('Logging')
      self.log_label.resize(200,20)
      self.log_label.move(105, 25)

      self.drone_group = QButtonGroup()
      self.drone_on = QRadioButton('On', self)
      self.drone_on.move(20,40)
      self.drone_off = QRadioButton('Off', self)
      self.drone_off.move(60,40)
      self.drone_off.setChecked(True)
      self.drone_group.addButton(self.drone_on, 0)
      self.drone_group.addButton(self.drone_off, 0)
      self.drone_label = QtGui.QLabel(self)
      self.drone_label.setText('Drones Flown')
      self.drone_label.resize(200,20)
      self.drone_label.move(105, 45)

      self.drone_loc_group = QButtonGroup()
      self.drone_loc_on = QRadioButton('On', self)
      self.drone_loc_on.move(20,60)
      self.drone_loc_off = QRadioButton('Off', self)
      self.drone_loc_off.move(60,60)
      self.drone_loc_off.setChecked(True)
      self.drone_loc_group.addButton(self.drone_loc_on, 0)
      self.drone_loc_group.addButton(self.drone_loc_off, 0)
      self.drone_loc_label = QtGui.QLabel(self)
      self.drone_loc_label.setText('Drone Locations')
      self.drone_loc_label.resize(200,20)
      self.drone_loc_label.move(105, 65)

      self.drone_freq_textbox = QLineEdit(self)
      self.drone_freq_textbox.move(20, 85)
      self.drone_freq_textbox.resize(50, 30)
      self.drone_freq_label = QLabel(self)
      self.drone_freq_label.setText("Frequency (in seconds)")
      self.drone_freq_label.resize(200,20)
      self.drone_freq_label.move(80, 90)

      self.objects_group = QButtonGroup()
      self.objects_on = QRadioButton('On', self)
      self.objects_on.move(20,110)
      self.objects_off = QRadioButton('Off', self)
      self.objects_off.move(60,110)
      self.objects_off.setChecked(True)
      self.objects_group.addButton(self.objects_on, 0)
      self.objects_group.addButton(self.objects_off, 0)
      self.objects_label = QtGui.QLabel(self)
      self.objects_label.setText('Objects')
      self.objects_label.resize(200,20)
      self.objects_label.move(105, 115)

      self.fp_group = QButtonGroup()
      self.fp_on = QRadioButton('On', self)
      self.fp_on.move(20,130)
      self.fp_off = QRadioButton('Off', self)
      self.fp_off.move(60,130)
      self.fp_off.setChecked(True)
      self.fp_group.addButton(self.fp_on, 0)
      self.fp_group.addButton(self.fp_off, 0)
      self.fp_label = QtGui.QLabel(self)
      self.fp_label.setText('Flight Paths')
      self.fp_label.resize(200,20)
      self.fp_label.move(105, 135)

      self.coord_group = QButtonGroup()
      self.coord_on = QRadioButton('On', self)
      self.coord_on.move(20,150)
      self.coord_off = QRadioButton('Off', self)
      self.coord_off.move(60,150)
      self.coord_off.setChecked(True)
      self.coord_group.addButton(self.coord_on, 0)
      self.coord_group.addButton(self.coord_off, 0)
      self.coord_label = QtGui.QLabel(self)
      self.coord_label.setText('Coordinates')
      self.coord_label.resize(200,20)
      self.coord_label.move(105, 155)

      self.events_group = QButtonGroup()
      self.events_on = QRadioButton('On', self)
      self.events_on.move(20,170)
      self.events_off = QRadioButton('Off', self)
      self.events_off.move(60,170)
      self.events_off.setChecked(True)
      self.events_group.addButton(self.events_on, 0)
      self.events_group.addButton(self.events_off, 0)
      self.events_label = QtGui.QLabel(self)
      self.events_label.setText('Major Events')
      self.events_label.resize(200,20)
      self.events_label.move(105, 175)

      self.save = QPushButton('save', self)
      self.save.move(130, 200)
      self.save.clicked.connect(self.save_log_config)
      self.open_log_config()

   def open_log_config(self):
      config = open('log_config.txt', 'r')
      line = config.readline().strip()
      if line == 'on':
         self.log_on.setChecked(True)
      else:
         self.log_off.setChecked(True)
      line = config.readline().strip()
      if line == 'on':
         self.drone_on.setChecked(True)
      else:
         self.drone_off.setChecked(True)
      line = config.readline().strip()
      if line == 'on':
         self.drone_loc_on.setChecked(True)
      else:
         self.drone_loc_off.setChecked(True)
      line = config.readline().strip()
      self.drone_freq_textbox.setText(line)
      line = config.readline().strip()
      if line == 'on':
         self.objects_on.setChecked(True)
      else:
         self.objects_off.setChecked(True)
      line = config.readline().strip()
      if line == 'on':
         self.fp_on.setChecked(True)
      else:
         self.fp_off.setChecked(True)
      line = config.readline().strip()
      if line == 'on':
         self.coord_on.setChecked(True)
      else:
         self.coord_off.setChecked(True)
      line = config.readline().strip()
      if line == 'on':
         self.events_on.setChecked(True)
      else:
         self.events_off.setChecked(True)
      config.close()
      return

   def save_log_config(self):
      config = open('log_config.txt', 'w')
      if self.log_on.isChecked():
         config.write('on\n')
      else:
         config.write('off\n')
      if self.drone_on.isChecked():
         config.write('on\n')
      else:
         config.write('off\n')
      if self.drone_loc_on.isChecked():
         config.write('on\n')
      else:
         config.write('off\n')
      freq = self.drone_freq_textbox.text()
      try:
         freq = float(freq)
      except:
         freq = 0.0;
      config.write(str(freq) + '\n')
      if self.objects_on.isChecked():
         config.write('on\n')
      else:
         config.write('off\n')
      if self.fp_on.isChecked():
         config.write('on\n')
      else:
         config.write('off\n')
      if self.coord_on.isChecked():
         config.write('on\n')
      else:
         config.write('off\n')
      if self.events_on.isChecked():
         config.write('on\n')
      else:
         config.write('off\n')
      config.close()
      return
#==============================================================================
class Monitor(QMainWindow):
    def __init__(self, parent = None):
        # Set up window for console
        super(Monitor, self).__init__(parent)
        self.resize(420, 250)

        # Set text window params
        self.notifs = QPlainTextEdit(self)
        self.setWindowTitle("Monitor")
        self.notifs.move(10, 10)
        self.notifs.resize(400, 200)

        self.notifs.setReadOnly(True)
        self.notifs.appendPlainText("text1")
        self.notifs.appendPlainText("text3\n")

        self.endButtn = QPushButton("End Flight", self)
        self.endButtn.move(310, 215)
        self.endButtn.clicked.connect(self.endFlight)

    def endFlight(self):
        print("Starting to end the flight crapidoodle II: Electric Boogaloo")
        # publish
#==============================================================================

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    start = WidgetGallery()
    start.show()
    app.exec_()

    monitor = Monitor()
    monitor.show()
    app.exec_()
