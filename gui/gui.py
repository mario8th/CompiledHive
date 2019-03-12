import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MainWindow(QMainWindow):
   count = 0
   def get_data(self):
      drone_count = 1.0
      for drone in self.drone_coords:
         self.drone_coords[drone] = [(drone_count, 0, 0)] + self.drone_coords[drone]
         drone_count = round(drone_count + .3,2)
      return (self.drones_connected, self.fp_connected, self.drone_coords, self.object_dict)
	
   def __init__(self, parent = None):
      super(MainWindow, self).__init__(parent)
      self.resize(1000,800)
      self.setWindowTitle("CrazySwarm Flight Path Stuff")

      self.drones_connected = []
      self.drones_available = []
      self.fp_connected = {}
      self.drone_coords = {}
      self.object_dict = {}
      self.file_names = "flights.txt"
      
      self.drone_select()
      self.fp_select()
      self.connect_drone_to_fp()
      self.coordinates()
      self.objects()

      self.toggle_vis = QPushButton('Toggle Vis', self)
      self.toggle_vis.move(520, 250)
      self.toggle_vis.clicked.connect(self.open_toggle_vis)
      self.toggle_log = QPushButton('Toggle Log', self)
      self.toggle_log.move(520, 300)
      self.toggle_log.clicked.connect(self.open_toggle_log)
      self.start_flight = QPushButton('Start Flight', self)
      self.start_flight.move(520, 400)
      self.start_flight.clicked.connect(self.start_flight_action)
      
   def drone_select(self):
      self.label_ds = QtGui.QLabel(self)
      self.label_ds.setText("Enter a drone id:")
      self.label_ds.move(20, 25)
      self.label_ds.resize(110, 20)

      self.textbox_ds = QLineEdit(self)
      self.textbox_ds.resize(60, 40)
      self.textbox_ds.move(20, 50)

      self.ds_add = QPushButton('Add Drone', self)
      self.ds_add.move(90, 55)
      self.ds_add.clicked.connect(self.add_drone_click)
        
      self.ds_combo = QComboBox(self)
      self.ds_combo.move(20, 95)
      self.ds_combo.resize(60,40)
      self.ds_combo.addItem("")

      self.ds_remove = QPushButton('Remove Drone', self)
      self.ds_remove.move(90, 100)
      self.ds_remove.clicked.connect(self.remove_drone_click)

   def add_drone_click(self):
      # TODO Connect to Drone Location System
      curr_drone = str(self.textbox_ds.text())
      self.textbox_ds.setText('')
      if(curr_drone == ''):
         return
      if(curr_drone in self.drones_connected):
         return
      if(len(self.drones_connected) < 7):
         self.drones_connected.append(curr_drone)
         self.drones_available.append(curr_drone)
         self.ds_combo.addItem(curr_drone)
         self.cdtfp_avail_combo.addItem(curr_drone)
         self.combo_c_drone.addItem(curr_drone)
         self.drone_coords[curr_drone] = []

   def remove_drone_click(self):
      drone_id = str(self.ds_combo.currentText())
      if(drone_id == ''):
         return
      drone_index = self.ds_combo.currentIndex()
      print "removing drone {}".format(drone_id)
      self.ds_combo.removeItem(drone_index)
      self.drones_connected.remove(drone_id)
      if drone_id in self.drones_available:
         drone_index = self.cdtfp_avail_combo.findText(drone_id)
         self.cdtfp_avail_combo.removeItem(drone_index)
         drone_index = self.combo_c_drone.findText(drone_id)
         self.combo_c_drone.removeItem(drone_index)
         print self.drone_coords
         self.drone_coords.pop(drone_id)
      else:
         drone_index = self.cdtfp_rem_combo.findText(drone_id)
         if drone_index >= 0:
            self.cdtfp_rem_combo.remove(drone_index)
         for key in self.fp_connected:
            if drone_id in self.fp_connected[key]:
               self.fp_connected[key].remove(drone_id)


   def fp_select(self):
      self.label_fps = QLabel(self)
      self.label_fps.setText("Select a flight path:")
      self.label_fps.move(20, 150)
      self.label_fps.resize(180, 20)

      #self.textbox_fps = QLine(self)
      #self.textbox_fps.resize(280, 40)
      #self.textbox_fps.move(20, 170)
      self.combo_fps = QtGui.QComboBox(self)
      self.combo_fps.move(20, 170)

      self.fps_add = QPushButton('Upload', self)
      self.fps_add.move(20, 220)
      self.fps_add.clicked.connect(self.add_fp_click)

      self.fps_remove = QPushButton('Remove', self)
      self.fps_remove.move(200, 220)
      self.fps_remove.clicked.connect(self.rem_fp_click)

   def add_fp_click(self):
      print "hewwo"
      self.current_file = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
      #if self.check_for_file(self.current_file) == False:
      temp = self.get_file_name(self.current_file)
      try:
         #check file is python file
         temp = temp.remove(".py")
      except (Exception) as error:
         message = ("File must be python file "+ str(error) )
         print(message)
      else:
         self.combo_fps.addItem(temp)
         self.combo_fp_cdtfp.addItem(temp)
         temp = str(temp)
         self.fp_connected[temp] = []
         file = open(self.file_names, 'a')
         file.write(" "+temp)
         file.close()
         self.create_file(temp)
      return

   def check_for_file(self,my_file):
       for count in range(self.combo_fps.count()):
          if self.comboBox.itemText(count) == my_file:
              return True
          else:
              return False

   def create_file(self, a_file):
        with open(self.current_file) as file_in:
            with open(a_file + ".py", "w") as file_out:
                for line in file_in:
                   file_out.write(line)
        return

   def get_file_name(self, a_file):
        temp = a_file
        if temp.contains("/") == True:
            temp = temp.section('/', -1)
        print temp
        return temp

   def rem_fp_click(self):
      file = open(self.file_names, 'w+')
      for line in file:
        temp = line.split(" ")
        for name in temp:
           index = 0;
           if name == self.current_file:
               index += 1
              #TO DO remove file from computer
               self.combo_fps.removeItem(index)
               file.write(" ")
           else:
               index += 1
               file.write(name) 
      file.close()
      return

   def connect_drone_to_fp(self):
      self.label_fp_cdtfp = QtGui.QLabel(self)
      self.label_fp_cdtfp.setText("Select Flight Path:")
      self.label_fp_cdtfp.resize(150, 20)
      self.label_fp_cdtfp.move(20,255)
      self.combo_fp_cdtfp = QtGui.QComboBox(self)
      self.combo_fp_cdtfp.resize(110, 40)
      self.combo_fp_cdtfp.move(20, 275)
      self.combo_fp_cdtfp.currentIndexChanged.connect(self.fp_combo_changed)

      self.cdtfp_avail_label = QtGui.QLabel(self)
      self.cdtfp_avail_label.setText("Select Drone:")
      self.cdtfp_avail_label.resize(150, 20)
      self.cdtfp_avail_label.move(150 ,255)
      self.cdtfp_avail_combo = QtGui.QComboBox(self)
      self.cdtfp_avail_combo.resize(110,40)
      self.cdtfp_avail_combo.move(150, 275)
      self.cdtfp_add = QtGui.QPushButton('Add', self)
      self.cdtfp_add.move(150, 320)
      self.cdtfp_add.resize(110, 30)
      self.cdtfp_add.clicked.connect(self.add_drone_to_fp_click)

      self.cdtfp_rem_label = QtGui.QLabel(self)
      self.cdtfp_rem_label.setText("Select Drone:")
      self.cdtfp_rem_label.resize(150, 20)
      self.cdtfp_rem_label.move(280, 255)
      self.cdtfp_rem_combo = QtGui.QComboBox(self)
      self.cdtfp_rem_combo.resize(110, 40)
      self.cdtfp_rem_combo.move(280, 275)
      self.cdtfp_remove = QtGui.QPushButton("Remove", self)
      self.cdtfp_remove.move(280, 320)
      self.cdtfp_remove.resize(110, 30)
      self.cdtfp_remove.clicked.connect(self.rem_drone_from_fp_click)

   def add_drone_to_fp_click(self):
      curr_fp = str(self.combo_fp_cdtfp.currentText())
      curr_drone = str(self.cdtfp_avail_combo.currentText())
      curr_index = self.cdtfp_avail_combo.currentIndex()
      self.cdtfp_avail_combo.removeItem(curr_index)
      self.drones_available.remove(curr_drone)
      self.fp_connected[curr_fp].append(curr_drone)
      self.drone_coords.pop(curr_drone)
      curr_index = self.combo_c_drone.findText(curr_drone)
      self.combo_c_drone.removeItem(curr_index)
      self.cdtfp_rem_combo.addItem(curr_drone)
      return

   def rem_drone_from_fp_click(self):
      curr_fp = str(self.combo_fp_cdtfp.currentText())
      curr_drone = str(self.cdtfp_rem_combo.currentText())
      curr_index = self.cdtfp_rem_combo.currentIndex()
      if curr_drone != '':
         self.cdtfp_rem_combo.removeItem(curr_index)
         self.fp_connected[curr_fp].remove(curr_drone)
         self.drones_available.append(curr_drone)
         self.drone_coords[curr_drone] = []
         self.cdtfp_avail_combo.addItem(curr_drone)
         self.combo_c_drone.addItem(curr_drone)
      return

   def fp_combo_changed(self):
      self.cdtfp_rem_combo.clear()
      curr_fp = str(self.combo_fp_cdtfp.currentText())
      if curr_fp != '':
         for drone in self.fp_connected[curr_fp]:
            self.cdtfp_rem_combo.addItem(drone)
      return
   
   def coordinates(self):
      self.label_c_drone = QtGui.QLabel(self)
      self.label_c_drone.setText("Choose Drone:")
      self.label_c_drone.resize(150, 20)
      self.label_c_drone.move(20, 375)
      self.combo_c_drone = QtGui.QComboBox(self)
      self.combo_c_drone.resize(110, 40)
      self.combo_c_drone.move(20, 395)
      self.combo_c_drone.currentIndexChanged.connect(self.coord_combo_changed)
      self.label_c_coord = QtGui.QLabel(self)
      self.label_c_coord.setText("Enter Coordinate:")
      self.label_c_coord.resize(120, 20)
      self.label_c_coord.move(145, 375)
      self.label_c_x = QtGui.QLabel(self)
      self.label_c_x.move(145, 400)
      self.label_c_x.setText('X:')
      self.textbox_c_x = QtGui.QLineEdit(self)
      self.textbox_c_x.resize(60, 40)
      self.textbox_c_x.move(160, 395)
      self.label_c_y = QtGui.QLabel(self)
      self.label_c_y.setText("Y:")
      self.label_c_y.move(230, 400)
      self.textbox_c_y = QtGui.QLineEdit(self)
      self.textbox_c_y.resize(60, 40)
      self.textbox_c_y.move(245, 395)
      self.label_c_z = QtGui.QLabel(self)
      self.label_c_z.setText('Z:')
      self.label_c_z.move(315, 400)
      self.textbox_c_z = QtGui.QLineEdit(self)
      self.textbox_c_z.resize(60, 40)
      self.textbox_c_z.move(330, 395)
      self.add_c_coord = QtGui.QPushButton("Add", self)
      self.add_c_coord.move(160, 445)
      self.add_c_coord.clicked.connect(self.add_coord)

      self.label_c_coord = QtGui.QLabel(self)
      self.label_c_coord.setText('Select Coordinate:')
      self.label_c_coord.resize(130, 20)
      self.label_c_coord.move(20, 470)
      self.combo_c_coord = QtGui.QComboBox(self)
      self.combo_c_coord.resize(110, 40)
      self.combo_c_coord.move(20, 490)
      self.rem_c_coord = QtGui.QPushButton('Remove', self)
      self.rem_c_coord.move(140, 495)
      self.rem_c_coord.clicked.connect(self.rem_coord)

   def add_coord(self):
      x_coord = self.textbox_c_x.text()
      y_coord = self.textbox_c_y.text()
      z_coord = self.textbox_c_z.text()
      curr_drone = str(self.combo_c_drone.currentText())
      if x_coord != '' and y_coord != '' and z_coord != '' and curr_drone != '':
         self.textbox_c_x.setText('')
         self.textbox_c_y.setText('')
         self.textbox_c_z.setText('')
         
         try:
            x_coord = float(x_coord)
            y_coord = float(y_coord)
            z_coord = float(z_coord)
         except:
            return

         x_bool = x_coord >= 0 and x_coord <= 3.4
         y_bool = y_coord >= 0 and y_coord <= 4.25
         z_bool = z_coord >= 0 and z_coord <= 2.43
         if x_bool and y_bool and z_bool:
            coordinate = (x_coord, y_coord, z_coord)
            self.drone_coords[curr_drone].append(coordinate)
            coordinate = '(' + str(x_coord) + ',' + str(y_coord) + ','  + str(z_coord) + ')'
            self.combo_c_coord.addItem(coordinate)
      return

   def rem_coord(self):
      curr_coord = str(self.combo_c_coord.currentText())
      curr_index = self.combo_c_coord.currentIndex()
      curr_drone = str(self.combo_c_drone.currentText())
      self.combo_c_coord.removeItem(curr_index)
      curr_coord = curr_coord[1:-1].split(',')
      curr_coord = (float(curr_coord[0]), float(curr_coord[1]), float(curr_coord[2]))
      self.drone_coords[curr_drone].remove(curr_coord)
      return

   def coord_combo_changed(self):
      self.combo_c_coord.clear()
      curr_drone = str(self.combo_c_drone.currentText())
      for coord in self.drone_coords[curr_drone]:
         coordinate = '(' + str(coord[0]) + ',' + str(coord[1]) + ',' + str(coord[2]) + ')'
         self.combo_c_coord.addItem(coordinate)
      return
   
   def objects(self):
      self.label_o_coord = QtGui.QLabel(self)
      self.label_o_coord.setText("Enter Corner Coordinates:")
      self.label_o_coord.resize(200, 20)
      self.label_o_coord.move(520, 25)
      self.label_o_x1 = QtGui.QLabel(self)
      self.label_o_x1.move(520, 50)
      self.label_o_x1.setText('X:')
      self.textbox_o_x1 = QtGui.QLineEdit(self)
      self.textbox_o_x1.resize(60, 40)
      self.textbox_o_x1.move(535, 45)
      self.label_o_y1 = QtGui.QLabel(self)
      self.label_o_y1.setText("Y:")
      self.label_o_y1.move(605, 50)
      self.textbox_o_y1 = QtGui.QLineEdit(self)
      self.textbox_o_y1.resize(60, 40)
      self.textbox_o_y1.move(620, 45)
      self.label_o_z1 = QtGui.QLabel(self)
      self.label_o_z1.setText('Z:')
      self.label_o_z1.move(690, 50)
      self.textbox_o_z1 = QtGui.QLineEdit(self)
      self.textbox_o_z1.resize(60, 40)
      self.textbox_o_z1.move(705, 45)

      self.label_o_x2 = QtGui.QLabel(self)
      self.label_o_x2.move(520, 100)
      self.label_o_x2.setText('X:')
      self.textbox_o_x2 = QtGui.QLineEdit(self)
      self.textbox_o_x2.resize(60, 40)
      self.textbox_o_x2.move(535, 95)
      self.label_o_y2 = QtGui.QLabel(self)
      self.label_o_y2.setText("Y:")
      self.label_o_y2.move(605, 100)
      self.textbox_o_y2 = QtGui.QLineEdit(self)
      self.textbox_o_y2.resize(60, 40)
      self.textbox_o_y2.move(620, 95)
      self.label_o_z2 = QtGui.QLabel(self)
      self.label_o_z2.setText('Z:')
      self.label_o_z2.move(690, 100)
      self.textbox_o_z2 = QtGui.QLineEdit(self)
      self.textbox_o_z2.resize(60, 40)
      self.textbox_o_z2.move(705, 95)

      self.label_o_name = QtGui.QLabel(self)
      self.label_o_name.setText('Choose a Name:')
      self.label_o_name.resize(200, 20)
      self.label_o_name.move(535, 140)
      self.textbox_o_name = QtGui.QLineEdit(self)
      self.textbox_o_name.resize(100, 40)
      self.textbox_o_name.move(535, 165)
      self.textbox_o_name.setText('object_' + str(len(self.object_dict)))
      self.add_o_coord = QtGui.QPushButton("Add", self)
      self.add_o_coord.move(650, 170)
      self.add_o_coord.clicked.connect(self.add_obj)

      self.label_o_rem = QLabel(self)
      self.label_o_rem.setText('Select an Object:')
      self.label_o_rem.resize(200, 20)
      self.label_o_rem.move(800, 25)
      self.combo_obj = QtGui.QComboBox(self)
      self.combo_obj.move(800, 50)
      self.obj_rem = QtGui.QPushButton("Remove", self)
      self.obj_rem.move(800, 100)
      self.obj_rem.clicked.connect(self.rem_obj)

   def add_obj(self):
      x1_coord = self.textbox_o_x1.text()
      y1_coord = self.textbox_o_y1.text()
      z1_coord = self.textbox_o_z1.text()
      x2_coord = self.textbox_o_x2.text()
      y2_coord = self.textbox_o_y2.text()
      z2_coord = self.textbox_o_z2.text()
      obj_name = str(self.textbox_o_name.text())
      if obj_name in self.object_dict:
         obj_name = obj_name + '(1)'
      if x1_coord != '' and x2_coord != '' and y1_coord != '' and y2_coord != '' and z1_coord != '' and z2_coord != '':
         self.textbox_o_x1.setText('')
         self.textbox_o_x2.setText('')
         self.textbox_o_y1.setText('')
         self.textbox_o_y2.setText('')
         self.textbox_o_z1.setText('')
         self.textbox_o_z2.setText('')
         
         try:
            x1_coord = float(x1_coord)
            x2_coord = float(x2_coord)
            y1_coord = float(y1_coord)
            y2_coord = float(y2_coord)
            z1_coord = float(z1_coord)
            z2_coord = float(z2_coord)
            self.textbox_o_name.setText('object_' + str(len(self.object_dict)))
         except:
            return

         x1_bool = x1_coord >= 0 and x1_coord <= 3.4
         y1_bool = y1_coord >= 0 and y1_coord <= 4.25
         z1_bool = z1_coord >= 0 and z1_coord <= 2.43
         x2_bool = x2_coord >= 0 and x2_coord <= 3.4
         y2_bool = y2_coord >= 0 and y2_coord <= 4.25
         z2_bool = z2_coord >= 0 and z2_coord <= 2.43
         if x1_bool and x2_bool and y1_bool and y2_bool and z1_bool and z2_bool:
            coord1 = (x1_coord, y1_coord, z1_coord)
            coord2 = (x2_coord, y2_coord, z2_coord)
            self.object_dict[obj_name] = (coord1, coord2)
            self.combo_obj.addItem(obj_name)
      return

   def rem_obj(self):
      curr_obj = str(self.combo_obj.currentText())
      curr_index = self.combo_obj.currentIndex()
      self.combo_obj.removeItem(curr_index)
      self.object_dict.pop(curr_obj)
      return
      
   def open_toggle_vis(self):
      self.toggle_vis_win = toggle_vis_window()
      self.toggle_vis_win.show()
      return

   def open_toggle_log(self):
      self.toggle_log_win = toggle_log_window()
      self.toggle_log_win.show()
      return

   def start_flight_action(self):
      print self.drones_connected
      print self.drones_available
      print self.fp_connected
      print self.drone_coords
      print self.object_dict
      QCoreApplication.exit(0)
      return

class toggle_vis_window(QtGui.QMainWindow):
   def __init__(self, parent=None):
      super(toggle_vis_window, self).__init__(parent)
      self.resize(250, 185)
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
      config = open('vis_config.txt', 'r')
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
      config = open('vis_config.txt', 'w')
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
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
