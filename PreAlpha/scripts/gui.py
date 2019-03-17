import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Main window for user input
class MainWindow(QMainWindow):
    count = 0

    # Collects user input data and returns it as a tuple
    # Logs all data before returning
    def getData(self):
        droneCount = 1.0
        # Starts initial drone at (1,1,0), adds .3 to x value for every additional drone
        for drone in self.droneCoords:
            self.droneCoords[drone] = [(droneCount, 1, 0)] + self.droneCoords[drone]
            droneCount = round(droneCount + .3,2)
        self.logInfo()
        return (self.dronesConnected, self.fpConnected, self.droneCoords, self.objectDict)

    # Initializes GUI for user input
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.resize(1000,800)
        self.setWindowTitle("CrazySwarm Flight Path Stuff")

        # Initialize field variables for user input storage
        self.dronesConnected = []
        self.dronesAvailable = []
        self.fpConnected = {}
        self.droneCoords = {}
        self.objectDict = {}
        self.fileNames = "flights.txt"

        # Sub methods initialize respective sub modules
        self.droneSelect()
        self.fpSelect()
        self.connectDroneToFP()
        self.coordinates()
        self.objects()

        # Add buttons for vis and log toggles and start buttons
        # Connects buttons to method listeners
        self.toggleVis = QPushButton('Toggle Vis', self)
        self.toggleVis.move(520, 250)
        self.toggleVis.clicked.connect(self.openToggleVis)
        self.toggleLog = QPushButton('Toggle Log', self)
        self.toggleLog.move(520, 300)
        self.toggleLog.clicked.connect(self.openToggleLog)
        self.startFlight = QPushButton('Start Flight', self)
        self.startFlight.move(520, 400)
        self.startFlight.clicked.connect(self.startFlightAction)

    # Initializes area for selection of drones
    # Connects add and remove buttons to respective listeners
    def droneSelect(self):
        self.labelDS = QtGui.QLabel(self)
        self.labelDS.setText("Enter a drone id:")
        self.labelDS.move(20, 25)
        self.labelDS.resize(110, 20)

        self.textboxDS = QLineEdit(self)
        self.textboxDS.resize(60, 40)
        self.textboxDS.move(20, 50)

        self.dsAdd = QPushButton('Add Drone', self)
        self.dsAdd.move(90, 55)
        self.dsAdd.clicked.connect(self.addDroneClick)

        self.dsCombo = QComboBox(self)
        self.dsCombo.move(20, 95)
        self.dsCombo.resize(60,40)
        self.dsCombo.addItem("")

        self.dsRemove = QPushButton('Remove Drone', self)
        self.dsRemove.move(90, 100)
        self.dsRemove.clicked.connect(self.removeDroneClick)

    # Adds drone from user text box to dronesConnected list
    # to the dronesAvailable list
    # to the drone select combo box
    # to the add drone to flight path combo box
    # to the droneCoords dict as a new key
    def addDroneClick(self):
        # TODO Connect to Drone Location System
        currDrone = str(self.textboxDS.text())
        self.textboxDS.setText('')
        if(currDrone == ''):
            return
        if(currDrone in self.dronesConnected):
            return
        if(len(self.dronesConnected) < 7):
            self.dronesConnected.append(currDrone)
            self.dronesAvailable.append(currDrone)
            self.dsCombo.addItem(currDrone)
            self.cdtfpAvailCombo.addItem(currDrone)
            self.comboCDrone.addItem(currDrone)
            self.droneCoords[currDrone] = []

    # removes drone from all previously mentioned places from previous method
    # if the drone is not in dronesAvailable, it goes and removes it from
    # the flight path it is connected to as well
    def removeDroneClick(self):
        droneID = str(self.dsCombo.currentText())
        if(droneID == ''):
            return
        droneIndex = self.dsCombo.currentIndex()
        print "removing drone {}".format(droneID)
        self.dsCombo.removeItem(droneIndex)
        self.dronesConnected.remove(droneID)
        if droneID in self.dronesAvailable:
            droneIndex = self.cdtfpAvailCombo.findText(droneID)
            self.cdtfpAvailCombo.removeItem(droneIndex)
            droneIndex = self.comboCDrone.findText(droneID)
            self.comboCDrone.removeItem(droneIndex)
            print self.droneCoords
            self.droneCoords.pop(droneID)
        else:
            droneIndex = self.cdtfpRemCombo.findText(droneID)
            if droneIndex >= 0:
                self.cdtfpRemCombo.remove(droneIndex)
            for key in self.fpConnected:
                if droneID in self.fpConnected[key]:
                    self.fpConnected[key].remove(droneID)

    # Initializes areas for user to import a flight path and connects needed listners
    def fpSelect(self):
        self.labelFPs = QLabel(self)
        self.labelFPs.setText("Select a flight path:")
        self.labelFPs.move(20, 150)
        self.labelFPs.resize(180, 20)

        self.comboFPs = QtGui.QComboBox(self)
        self.comboFPs.move(20, 170)

        self.fpsAdd = QPushButton('Upload', self)
        self.fpsAdd.move(20, 220)
        self.fpsAdd.clicked.connect(self.addFPClick)

        self.fpsRemove = QPushButton('Remove', self)
        self.fpsRemove.move(200, 220)
        self.fpsRemove.clicked.connect(self.remFPClick)

    # Allows user to import a python file, checks if valid, and saves it
    # into comboFPs, comboFPcdtfp, and adds it as a key to fpConnected
    def addFPClick(self):
        message = QMessageBox()
        self.currentFile = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        #if self.checkForFile(self.currentFile) == False:
        tempName = self.getFileName(self.currentFile)
        if tempName[-2:] == 'py':
            #check file is python file
            tempName = tempName.remove(".py")
            self.comboFPs.addItem(tempName)
            self.comboFPcdtfp.addItem(tempName)
            tempName = str(tempName)
            self.fpConnected[tempName] = []
            file = open(self.fileNames, 'a')
            file.write(" " + tempName)
            file.close()
            self.create_file(tempName)
        else:
            # Give error if not
            message.setText("File must be python file ")
            message.setWindowTitle("Error")

            message.setStandardButtons(QMessageBox.Ok)
            retval = message.exec_()
        return

    # Checks if file already in comboFPs
    def checkForFile(self, myFile):
        for count in range(self.comboFPs.count()):
            if self.comboBox.itemText(count) == myFile:
                return True
            else:
                return False

    # Writes all lines from file into fileOut
    def create_file(self, file):
        with open(self.currentFile) as fileIn:
            with open(file + ".py", "w") as fileOut:
                for line in fileIn:
                    fileOut.write(line)
        return

    # Lexie I don't know what this is doing
    def getFileName(self, file):
        tempFile = file
        if tempFile.contains("/") == True:
            tempFile = tempFile.section('/', -1)
        return tempFile

    # Removes file from comboFPS and fileNames
    def remFPClick(self):
        file = open(self.fileNames, 'w+')
        for line in file:
            temp = line.split(" ")
            for name in temp:
                index = 0;
                if name == self.currentFile:
                    index += 1
                    #TO DO remove file from computer
                    self.comboFPs.removeItem(index)
                    file.write(" ")
                else:
                    index += 1
                    file.write(name)
        file.close()
        return

    # Initializes all areas for user input to connect drones to a flight path
    # connects all respective button listeners
    def connectDroneToFP(self):
        self.labelFPcdtfp = QtGui.QLabel(self)
        self.labelFPcdtfp.setText("Select Flight Path:")
        self.labelFPcdtfp.resize(150, 20)
        self.labelFPcdtfp.move(20,255)
        self.comboFPcdtfp = QtGui.QComboBox(self)
        self.comboFPcdtfp.resize(110, 40)
        self.comboFPcdtfp.move(20, 275)
        self.comboFPcdtfp.currentIndexChanged.connect(self.fpComboChanged)

        self.cdtfpAvailLabel = QtGui.QLabel(self)
        self.cdtfpAvailLabel.setText("Select Drone:")
        self.cdtfpAvailLabel.resize(150, 20)
        self.cdtfpAvailLabel.move(150 ,255)
        self.cdtfpAvailCombo = QtGui.QComboBox(self)
        self.cdtfpAvailCombo.resize(110,40)
        self.cdtfpAvailCombo.move(150, 275)
        self.cdtfpAdd = QtGui.QPushButton('Add', self)
        self.cdtfpAdd.move(150, 320)
        self.cdtfpAdd.resize(110, 30)
        self.cdtfpAdd.clicked.connect(self.addDroneToFPClick)

        self.cdtfpRemLabel = QtGui.QLabel(self)
        self.cdtfpRemLabel.setText("Select Drone:")
        self.cdtfpRemLabel.resize(150, 20)
        self.cdtfpRemLabel.move(280, 255)
        self.cdtfpRemCombo = QtGui.QComboBox(self)
        self.cdtfpRemCombo.resize(110, 40)
        self.cdtfpRemCombo.move(280, 275)
        self.cdtfpRemove = QtGui.QPushButton("Remove", self)
        self.cdtfpRemove.move(280, 320)
        self.cdtfpRemove.resize(110, 30)
        self.cdtfpRemove.clicked.connect(self.remDroneFromFPClick)

    # Adds drone to selected flight path
    # adds to dictionary keyd to fp
    # removes from dronesAvailable and necessary combo box
    def addDroneToFPClick(self):
        currFP = str(self.comboFPcdtfp.currentText())
        currDrone = str(self.cdtfpAvailCombo.currentText())
        currIndex = self.cdtfpAvailCombo.currentIndex()
        self.cdtfpAvailCombo.removeItem(currIndex)
        self.dronesAvailable.remove(currDrone)
        self.fpConnected[currFP].append(currDrone)
        self.droneCoords.pop(currDrone)
        currIndex = self.comboCDrone.findText(currDrone)
        self.comboCDrone.removeItem(currIndex)
        self.cdtfpRemCombo.addItem(currDrone)
        return

    # Removes drone from selected flight path
    # removes from fpConnected dictionary, and adds to
    # dronesAvailable and necessary combo boxes
    def remDroneFromFPClick(self):
        currFP = str(self.comboFPcdtfp.currentText())
        currDrone = str(self.cdtfpRemCombo.currentText())
        currIndex = self.cdtfpRemCombo.currentIndex()
        if currDrone != '':
            self.cdtfpRemCombo.removeItem(currIndex)
            self.fpConnected[currFP].remove(currDrone)
            self.dronesAvailable.append(currDrone)
            self.droneCoords[currDrone] = []
            self.cdtfpAvailCombo.addItem(currDrone)
            self.comboCDrone.addItem(currDrone)
        return

    # Detects if the flight path selection combo box has changed
    # if so, changes the drone remove combo to display drones connected to
    # the newly selected flight path
    def fpComboChanged(self):
        self.cdtfpRemCombo.clear()
        currFP = str(self.comboFPcdtfp.currentText())
        if currFP != '':
            for drone in self.fpConnected[currFP]:
                self.cdtfpRemCombo.addItem(drone)
        return

    # Initiates all areas for user to input coordinats for drones to fly to
    def coordinates(self):
        self.labelCDrone = QtGui.QLabel(self)
        self.labelCDrone.setText("Choose Drone:")
        self.labelCDrone.resize(150, 20)
        self.labelCDrone.move(20, 375)
        self.comboCDrone = QtGui.QComboBox(self)
        self.comboCDrone.resize(110, 40)
        self.comboCDrone.move(20, 395)
        self.comboCDrone.currentIndexChanged.connect(self.coordComboChanged)
        self.labelCCoordEnter = QtGui.QLabel(self)
        self.labelCCoordEnter.setText("Enter Coordinate:")
        self.labelCCoordEnter.resize(120, 20)
        self.labelCCoordEnter.move(145, 375)
        self.labelCX = QtGui.QLabel(self)
        self.labelCX.move(145, 400)
        self.labelCX.setText('X:')
        self.textboxCX = QtGui.QLineEdit(self)
        self.textboxCX.resize(60, 40)
        self.textboxCX.move(160, 395)
        self.labelCY = QtGui.QLabel(self)
        self.labelCY.setText("Y:")
        self.labelCY.move(230, 400)
        self.textboxCY = QtGui.QLineEdit(self)
        self.textboxCY.resize(60, 40)
        self.textboxCY.move(245, 395)
        self.labelCZ = QtGui.QLabel(self)
        self.labelCZ.setText('Z:')
        self.labelCZ.move(315, 400)
        self.textboxCZ = QtGui.QLineEdit(self)
        self.textboxCZ.resize(60, 40)
        self.textboxCZ.move(330, 395)
        self.addCCoord = QtGui.QPushButton("Add", self)
        self.addCCoord.move(160, 445)
        self.addCCoord.clicked.connect(self.addCoord)

        self.labelCCoordSelect = QtGui.QLabel(self)
        self.labelCCoordSelect.setText('Select Coordinate:')
        self.labelCCoordSelect.resize(130, 20)
        self.labelCCoordSelect.move(20, 470)
        self.comboCCoord = QtGui.QComboBox(self)
        self.comboCCoord.resize(110, 40)
        self.comboCCoord.move(20, 490)
        self.remCCoord = QtGui.QPushButton('Remove', self)
        self.remCCoord.move(140, 495)
        self.remCCoord.clicked.connect(self.remCoord)

    # Adds coordinates to the flight path of the current selected drone
    # and adds to droneCoords dictionary
    def addCoord(self):
        xCoord = self.textboxCX.text()
        yCoord = self.textboxCY.text()
        zCoord = self.textboxCZ.text()
        currDrone = str(self.comboCDrone.currentText())
        # Checks all inputs are filled
        if xCoord != '' and yCoord != '' and zCoord != '' and currDrone != '':
            self.textboxCX.setText('')
            self.textboxCY.setText('')
            self.textboxCZ.setText('')

            # Checks all inputs are numbers
            try:
                xCoord = float(xCoord)
                yCoord = float(yCoord)
                zCoord = float(zCoord)
            except:
                return
            # Checks if inputs in bounds, then adds to droneCoords and coord combo box
            x_bool = xCoord >= -4 and xCoord <= 4
            y_bool = yCoord >= -4 and yCoord <= 4
            z_bool = zCoord >= 0 and zCoord <= 9
            if x_bool and y_bool and z_bool:
                coordinate = (xCoord, yCoord, zCoord)
                self.droneCoords[currDrone].append(coordinate)
                coordinate = '(' + str(xCoord) + ',' + str(yCoord) + ','  + str(zCoord) + ')'
                self.comboCCoord.addItem(coordinate)
        return

    # Removes selected coordinate from droneCoords
    def remCoord(self):
        currCoord = str(self.comboCCoord.currentText())
        currIndex = self.comboCCoord.currentIndex()
        currDrone = str(self.comboCDrone.currentText())
        self.comboCCoord.removeItem(currIndex)
        currCoord = currCoord[1:-1].split(',')
        currCoord = (float(currCoord[0]), float(currCoord[1]), float(currCoord[2]))
        self.droneCoords[currDrone].remove(currCoord)
        return

    # Detects if another drone has been selected and displays the coordinates
    # connected to it
    def coordComboChanged(self):
        self.comboCCoord.clear()
        currDrone = str(self.comboCDrone.currentText())
        for coord in self.droneCoords[currDrone]:
            coordinate = '(' + str(coord[0]) + ',' + str(coord[1]) + ',' + str(coord[2]) + ')'
            self.comboCCoord.addItem(coordinate)
        return

    # Initializes the input areas for adding objects
    def objects(self):
        self.labelOCoord = QtGui.QLabel(self)
        self.labelOCoord.setText("Enter Corner Coordinates:")
        self.labelOCoord.resize(200, 20)
        self.labelOCoord.move(520, 25)
        self.labelOX1 = QtGui.QLabel(self)
        self.labelOX1.move(520, 50)
        self.labelOX1.setText('X:')
        self.textboxOX1 = QtGui.QLineEdit(self)
        self.textboxOX1.resize(60, 40)
        self.textboxOX1.move(535, 45)
        self.labelOY1 = QtGui.QLabel(self)
        self.labelOY1.setText("Y:")
        self.labelOY1.move(605, 50)
        self.textboxOY1 = QtGui.QLineEdit(self)
        self.textboxOY1.resize(60, 40)
        self.textboxOY1.move(620, 45)
        self.labelOZ1 = QtGui.QLabel(self)
        self.labelOZ1.setText('Z:')
        self.labelOZ1.move(690, 50)
        self.textboxOZ1 = QtGui.QLineEdit(self)
        self.textboxOZ1.resize(60, 40)
        self.textboxOZ1.move(705, 45)

        self.labelOX2 = QtGui.QLabel(self)
        self.labelOX2.move(520, 100)
        self.labelOX2.setText('X:')
        self.textboxOX2 = QtGui.QLineEdit(self)
        self.textboxOX2.resize(60, 40)
        self.textboxOX2.move(535, 95)
        self.labelOY2 = QtGui.QLabel(self)
        self.labelOY2.setText("Y:")
        self.labelOY2.move(605, 100)
        self.textboxOY2 = QtGui.QLineEdit(self)
        self.textboxOY2.resize(60, 40)
        self.textboxOY2.move(620, 95)
        self.labelOZ2 = QtGui.QLabel(self)
        self.labelOZ2.setText('Z:')
        self.labelOZ2.move(690, 100)
        self.textboxOZ2 = QtGui.QLineEdit(self)
        self.textboxOZ2.resize(60, 40)
        self.textboxOZ2.move(705, 95)

        self.labelOName = QtGui.QLabel(self)
        self.labelOName.setText('Choose a Name:')
        self.labelOName.resize(200, 20)
        self.labelOName.move(535, 140)
        self.textboxOName = QtGui.QLineEdit(self)
        self.textboxOName.resize(100, 40)
        self.textboxOName.move(535, 165)
        self.textboxOName.setText('object_' + str(len(self.objectDict)))
        self.addOCoord = QtGui.QPushButton("Add", self)
        self.addOCoord.move(650, 170)
        self.addOCoord.clicked.connect(self.addObj)

        self.labelORem = QLabel(self)
        self.labelORem.setText('Select an Object:')
        self.labelORem.resize(200, 20)
        self.labelORem.move(800, 25)
        self.comboObj = QtGui.QComboBox(self)
        self.comboObj.move(800, 50)
        self.objRem = QtGui.QPushButton("Remove", self)
        self.objRem.move(800, 100)
        self.objRem.clicked.connect(self.remObj)

    # Adds object name as new key in objectDict pointing to a list of the
    # two input coordinates
    def addObj(self):
        x1Coord = self.textboxOX1.text()
        y1Coord = self.textboxOY1.text()
        z1Coord = self.textboxOZ1.text()
        x2Coord = self.textboxOX2.text()
        y2Coord = self.textboxOY2.text()
        z2Coord = self.textboxOZ2.text()
        obj_name = str(self.textboxOName.text())
        # Checks if name is valid
        if obj_name in self.objectDict:
            obj_name = obj_name + '(1)'
        # Checks if all points are input
        if x1Coord != '' and x2Coord != '' and y1Coord != '' and y2Coord != '' and z1Coord != '' and z2Coord != '':
            self.textboxOX1.setText('')
            self.textboxOX2.setText('')
            self.textboxOY1.setText('')
            self.textboxOY2.setText('')
            self.textboxOZ1.setText('')
            self.textboxOZ2.setText('')
            # Checks if all points are numbers
            try:
                x1Coord = float(x1Coord)
                x2Coord = float(x2Coord)
                y1Coord = float(y1Coord)
                y2Coord = float(y2Coord)
                z1Coord = float(z1Coord)
                z2Coord = float(z2Coord)
                self.textboxOName.setText('object_' + str(len(self.objectDict)))
            except:
                return
            # Checks if all points are in bounds then adds to dictionary
            x1Bool = x1Coord >= -4 and x1Coord <= 4
            y1Bool = y1Coord >= -4 and y1Coord <= 4
            z1Bool = z1Coord >= 0 and z1Coord <= 8
            x2Bool = x2Coord >= -4 and x2Coord <= 4
            y2Bool = y2Coord >= -4 and y2Coord <= 4
            z2Bool = z2Coord >= 0 and z2Coord <= 8
            if x1Bool and x2Bool and y1Bool and y2Bool and z1Bool and z2Bool:
                coord1 = (x1Coord, y1Coord, z1Coord)
                coord2 = (x2Coord, y2Coord, z2Coord)
                self.objectDict[obj_name] = (coord1, coord2)
                self.comboObj.addItem(obj_name)
        return

    # Removes selected object from objectDict
    def remObj(self):
        curr_obj = str(self.comboObj.currentText())
        currIndex = self.comboObj.currentIndex()
        self.comboObj.removeItem(currIndex)
        self.objectDict.pop(curr_obj)
        return

    # Creates and displayes the visualization toggle screen
    def openToggleVis(self):
        self.toggleViswin = ToggleVisWindow()
        self.toggleViswin.show()
        return

    # Creates and displayes the log toggle screen
    def openToggleLog(self):
        self.toggleLogwin = ToggleLogWindow()
        self.toggleLogwin.show()
        return

    # Closes window to allow backend to start flight
    def startFlightAction(self):
        self.close()
        return

    # Logs all requested data input
    def logInfo(self):
        log = open("LogData.txt", 'w')
        config = open("log_config.txt", 'r')
        # Checks if log is on
        line = config.readline().strip()
        if line == "on":
            # Checks if requested to save drones
            line = config.readline().strip()
            if line == "on":
                log.write("Drones Connected:\n")
                for drone in self.dronesConnected:
                    log.write(drone + ' ')
                log.write('\n\n')
            # Checks if requested to save drone locs
            line = config.readline().strip()
            # Checks for frequency of drone locs
            line = config.readline().strip()
            # Checks if requested to save objects
            line = config.readline().strip()
            if line == "on":
                log.write("Objects and outer corners:\n")
                for obj in self.objectDict:
                    log.write(obj + ' ')
                    log.write(str(self.objectDict[obj][0]) + ' ')
                    log.write(str(self.objectDict[obj][1]) + '\n')
                log.write('\n')
            # Checks if requested to save flight Paths
            line = config.readline().strip()
            if line == "on":
                log.write("Flight Paths and Connected Drones:\n")
                for fp in self.fpConnected:
                    log.write(fp + ': ')
                    for drone in self.fpConnected[fp]:
                        log.write(drone + ' ')
                    log.write('\n')
                log.write('\n')
            # checks if requested to save drone coords
            line = config.readline().strip()
            if line == 'on':
                log.write("Drones and connected coordinates:\n")
                log.write(str(self.droneCoords))
                log.write('\n')
            # Checks if requested to save events
            line = config.readline().strip()

# Window to allow users to toggle which elements they wish to be displayed in the visualization
class ToggleVisWindow(QtGui.QMainWindow):
    # Initializes all radio options for user to toggle
    def __init__(self, parent=None):
        super(ToggleVisWindow, self).__init__(parent)
        self.resize(250, 185)
        self.mainLabel = QtGui.QLabel(self)
        self.mainLabel.setText('Toggle Elements Shown in Visualzation')
        self.mainLabel.resize(300, 20)
        self.setWindowTitle('Toggle Visualization')

        self.visGroup = QButtonGroup()
        self.visOn = QRadioButton('On', self)
        self.visOn.move(20,20)
        self.visOff = QRadioButton('Off', self)
        self.visOff.move(60,20)
        self.visGroup.addButton(self.visOn, 0)
        self.visGroup.addButton(self.visOff, 0)
        self.visLabel = QtGui.QLabel(self)
        self.visLabel.setText('Visualization')
        self.visLabel.resize(200,20)
        self.visLabel.move(105, 25)

        self.droneLocGroup = QButtonGroup()
        self.droneLocOn = QRadioButton('On', self)
        self.droneLocOn.move(20,40)
        self.droneLocOff = QRadioButton('Off', self)
        self.droneLocOff.move(60,40)
        self.droneLocOff.setChecked(True)
        self.droneLocGroup.addButton(self.droneLocOn, 0)
        self.droneLocGroup.addButton(self.droneLocOff, 0)
        self.droneLocLabel = QtGui.QLabel(self)
        self.droneLocLabel.setText('Drone Locations')
        self.droneLocLabel.resize(200,20)
        self.droneLocLabel.move(105, 45)

        self.dronePathGroup = QButtonGroup()
        self.dronePathOn = QRadioButton('On', self)
        self.dronePathOn.move(20,60)
        self.dronePathOff = QRadioButton('Off', self)
        self.dronePathOff.move(60,60)
        self.dronePathOff.setChecked(True)
        self.dronePathGroup.addButton(self.dronePathOn, 0)
        self.dronePathGroup.addButton(self.dronePathOff, 0)
        self.dronePathLabel = QtGui.QLabel(self)
        self.dronePathLabel.setText('Drone Paths Expected')
        self.dronePathLabel.resize(200,20)
        self.dronePathLabel.move(105, 65)

        self.droneFlownGroup = QButtonGroup()
        self.droneFlownOn = QRadioButton('On', self)
        self.droneFlownOn.move(20,80)
        self.droneFlownOff = QRadioButton('Off', self)
        self.droneFlownOff.move(60,80)
        self.droneFlownOff.setChecked(True)
        self.droneFlownGroup.addButton(self.droneFlownOn, 0)
        self.droneFlownGroup.addButton(self.droneFlownOff, 0)
        self.droneFlownLabel = QtGui.QLabel(self)
        self.droneFlownLabel.setText('Drone Paths Flown')
        self.droneFlownLabel.resize(200,20)
        self.droneFlownLabel.move(105, 85)

        self.sensorGroup = QButtonGroup()
        self.sensorOn = QRadioButton('On', self)
        self.sensorOn.move(20,100)
        self.sensorOff = QRadioButton('Off', self)
        self.sensorOff.move(60,100)
        self.sensorOff.setChecked(True)
        self.sensorGroup.addButton(self.sensorOn, 0)
        self.sensorGroup.addButton(self.sensorOff, 0)
        self.sensorLabel = QtGui.QLabel(self)
        self.sensorLabel.setText('Sensors')
        self.sensorLabel.resize(200,20)
        self.sensorLabel.move(105, 105)

        self.objectsGroup = QButtonGroup()
        self.objectsOn = QRadioButton('On', self)
        self.objectsOn.move(20,120)
        self.objectsOff = QRadioButton('Off', self)
        self.objectsOff.move(60,120)
        self.objectsOff.setChecked(True)
        self.objectsGroup.addButton(self.objectsOn, 0)
        self.objectsGroup.addButton(self.objectsOff, 0)
        self.objectsLabel = QtGui.QLabel(self)
        self.objectsLabel.setText('Objects')
        self.objectsLabel.resize(200,20)
        self.objectsLabel.move(105, 125)
        self.save = QPushButton('save', self)
        self.save.move(130, 150)
        self.save.clicked.connect(self.saveVisConfig)
        self.openVisConfig()

    # toggles radio buttons from vis_config
    def openVisConfig(self):
        config = open('vis_config.txt', 'r')
        line = config.readline().strip()
        if line == 'on':
            self.visOn.setChecked(True)
        else:
            self.visOff.setChecked(True)
        line = config.readline().strip()
        if line == 'on':
            self.droneLocOn.setChecked(True)
        else:
            self.droneLocOff.setChecked(True)
        line = config.readline().strip()
        if line == 'on':
            self.dronePathOn.setChecked(True)
        else:
            self.dronePathOff.setChecked(True)
        line = config.readline().strip()
        if line == 'on':
            self.droneFlownOn.setChecked(True)
        else:
            self.droneFlownOff.setChecked(True)
        line = config.readline().strip()
        if line == 'on':
            self.sensorOn.setChecked(True)
        else:
            self.sensorOff.setChecked(True)
        line = config.readline().strip()
        if line == 'on':
            self.objectsOn.setChecked(True)
        else:
            self.objectsOff.setChecked(True)
        config.close()
        return

    # Saves input into vis config
    def saveVisConfig(self):
        config = open('vis_config.txt', 'w')
        if self.visOn.isChecked():
            config.write('on\n')
        else:
            config.write('off\n')
        if self.droneLocOn.isChecked():
            config.write('on\n')
        else:
            config.write('off\n')
        if self.dronePathOn.isChecked():
            config.write('on\n')
        else:
            config.write('off\n')
        if self.droneFlownOn.isChecked():
            config.write('on\n')
        else:
            config.write('off\n')
        if self.sensorOn.isChecked():
            config.write('on\n')
        else:
            config.write('off\n')
        if self.objectsOn.isChecked():
            config.write('on\n')
        else:
            config.write('off\n')
        config.close()
        return

# Window to toggle what the user wishes to be logged
class ToggleLogWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ToggleLogWindow, self).__init__(parent)
        self.resize(250, 230)
        self.mainLabel = QtGui.QLabel(self)
        self.mainLabel.setText('Toggle Elements Logged')
        self.mainLabel.resize(300, 20)
        self.setWindowTitle('Toggle Log File')

        self.logGroup = QButtonGroup()
        self.logOn = QRadioButton('On', self)
        self.logOn.move(20,20)
        self.logOff = QRadioButton('Off', self)
        self.logOff.move(60,20)
        self.logOff.setChecked(True)
        self.logGroup.addButton(self.logOn, 0)
        self.logGroup.addButton(self.logOff, 0)
        self.logLabel = QtGui.QLabel(self)
        self.logLabel.setText('Logging')
        self.logLabel.resize(200,20)
        self.logLabel.move(105, 25)

        self.droneGroup = QButtonGroup()
        self.droneOn = QRadioButton('On', self)
        self.droneOn.move(20,40)
        self.droneOff = QRadioButton('Off', self)
        self.droneOff.move(60,40)
        self.droneOff.setChecked(True)
        self.droneGroup.addButton(self.droneOn, 0)
        self.droneGroup.addButton(self.droneOff, 0)
        self.droneLabel = QtGui.QLabel(self)
        self.droneLabel.setText('Drones Flown')
        self.droneLabel.resize(200,20)
        self.droneLabel.move(105, 45)

        self.droneLocGroup = QButtonGroup()
        self.droneLocOn = QRadioButton('On', self)
        self.droneLocOn.move(20,60)
        self.droneLocOff = QRadioButton('Off', self)
        self.droneLocOff.move(60,60)
        self.droneLocOff.setChecked(True)
        self.droneLocGroup.addButton(self.droneLocOn, 0)
        self.droneLocGroup.addButton(self.droneLocOff, 0)
        self.droneLocLabel = QtGui.QLabel(self)
        self.droneLocLabel.setText('Drone Locations')
        self.droneLocLabel.resize(200,20)
        self.droneLocLabel.move(105, 65)

        self.droneFreqTextbox = QLineEdit(self)
        self.droneFreqTextbox.move(20, 85)
        self.droneFreqTextbox.resize(50, 30)
        self.droneFreqLabel = QLabel(self)
        self.droneFreqLabel.setText("Frequency (in seconds)")
        self.droneFreqLabel.resize(200,20)
        self.droneFreqLabel.move(80, 90)

        self.objectsGroup = QButtonGroup()
        self.objectsOn = QRadioButton('On', self)
        self.objectsOn.move(20,110)
        self.objectsOff = QRadioButton('Off', self)
        self.objectsOff.move(60,110)
        self.objectsOff.setChecked(True)
        self.objectsGroup.addButton(self.objectsOn, 0)
        self.objectsGroup.addButton(self.objectsOff, 0)
        self.objectsLabel = QtGui.QLabel(self)
        self.objectsLabel.setText('Objects')
        self.objectsLabel.resize(200,20)
        self.objectsLabel.move(105, 115)

        self.fpGroup = QButtonGroup()
        self.fpOn = QRadioButton('On', self)
        self.fpOn.move(20,130)
        self.fpOff = QRadioButton('Off', self)
        self.fpOff.move(60,130)
        self.fpOff.setChecked(True)
        self.fpGroup.addButton(self.fpOn, 0)
        self.fpGroup.addButton(self.fpOff, 0)
        self.fpLabel = QtGui.QLabel(self)
        self.fpLabel.setText('Flight Paths')
        self.fpLabel.resize(200,20)
        self.fpLabel.move(105, 135)

        self.coordGroup = QButtonGroup()
        self.coordOn = QRadioButton('On', self)
        self.coordOn.move(20,150)
        self.coordOff = QRadioButton('Off', self)
        self.coordOff.move(60,150)
        self.coordOff.setChecked(True)
        self.coordGroup.addButton(self.coordOn, 0)
        self.coordGroup.addButton(self.coordOff, 0)
        self.coordLabel = QtGui.QLabel(self)
        self.coordLabel.setText('Coordinates')
        self.coordLabel.resize(200,20)
        self.coordLabel.move(105, 155)

        self.eventsGroup = QButtonGroup()
        self.eventsOn = QRadioButton('On', self)
        self.eventsOn.move(20,170)
        self.eventsOff = QRadioButton('Off', self)
        self.eventsOff.move(60,170)
        self.eventsOff.setChecked(True)
        self.eventsGroup.addButton(self.eventsOn, 0)
        self.eventsGroup.addButton(self.eventsOff, 0)
        self.eventsLabel = QtGui.QLabel(self)
        self.eventsLabel.setText('Major Events')
        self.eventsLabel.resize(200,20)
        self.eventsLabel.move(105, 175)

        self.save = QPushButton('save', self)
        self.save.move(130, 200)
        self.save.clicked.connect(self.saveLogConfig)
        self.openLogConfig()

    # Configures radio buttons from log_config
    def openLogConfig(self):
        config = open('log_config.txt', 'r')
        line = config.readline().strip()
        if line == 'on':
            self.logOn.setChecked(True)
        else:
            self.logOff.setChecked(True)
        line = config.readline().strip()
        if line == 'on':
            self.droneOn.setChecked(True)
        else:
            self.droneOff.setChecked(True)
        line = config.readline().strip()
        if line == 'on':
            self.droneLocOn.setChecked(True)
        else:
            self.droneLocOff.setChecked(True)
        line = config.readline().strip()
        self.droneFreqTextbox.setText(line)
        line = config.readline().strip()
        if line == 'on':
            self.objectsOn.setChecked(True)
        else:
            self.objectsOff.setChecked(True)
        line = config.readline().strip()
        if line == 'on':
            self.fpOn.setChecked(True)
        else:
            self.fpOff.setChecked(True)
        line = config.readline().strip()
        if line == 'on':
            self.coordOn.setChecked(True)
        else:
            self.coordOff.setChecked(True)
        line = config.readline().strip()
        if line == 'on':
            self.eventsOn.setChecked(True)
        else:
            self.eventsOff.setChecked(True)
        config.close()
        return

    # Saves selected input into log file config
    def saveLogConfig(self):
        config = open('log_config.txt', 'w')
        if self.logOn.isChecked():
            config.write('on\n')
        else:
            config.write('off\n')
        if self.droneOn.isChecked():
            config.write('on\n')
        else:
            config.write('off\n')
        if self.droneLocOn.isChecked():
            config.write('on\n')
        else:
            config.write('off\n')
        freq = self.droneFreqTextbox.text()
        try:
            freq = float(freq)
        except:
            freq = 0.0;
        config.write(str(freq) + '\n')
        if self.objectsOn.isChecked():
            config.write('on\n')
        else:
            config.write('off\n')
        if self.fpOn.isChecked():
            config.write('on\n')
        else:
            config.write('off\n')
        if self.coordOn.isChecked():
            config.write('on\n')
        else:
            config.write('off\n')
        if self.eventsOn.isChecked():
            config.write('on\n')
        else:
            config.write('off\n')
        config.close()
        return

# Text are to view major events and stop button to initate the flight ending
class Monitor(QMainWindow):
    def __init__(self, parent = None):
        # Set up window for console
        super(Monitor, self).__init__(parent)
        self.resize(420, 250)

        # Set text window params
        self.notifs = QPlainTextEdit(self)
        self.notifs.move(10, 10)
        self.notifs.resize(400, 200)

        self.notifs.setReadOnly(True)
        self.notifs.appendPlainText("text1")
        self.notifs.appendPlainText("text3\n")

        self.end_buttn = QPushButton("End Flight", self)
        self.end_buttn.move(310, 215)
        self.end_buttn.clicked.connect(self.end_flight)

    def end_flight(self):
        print("Starting to end the flight crapidoodle II: Electric Boogaloo")
        # publish

def main():
    app = QtGui.QApplication(sys.argv)
    start = MainWindow()
    start.show()
    app.exec_()

    monitor = Monitor()
    monitor.show()
    app.exec_()

if __name__ == "__main__":
    main()
