import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
a = QApplication(sys.argv)
w = QWidget()
vbox = QVBoxLayout()
w.resize(320,220)
w.setWindowTitle("Add/Remove Drones")

label_drones = QLabel()
label_drones.setText("test buttons")
label_drones.setAlignment(Qt.AlignLeft)
vbox.addWidget(label_drones)

i = 0
while(i < 5):
    title = "button" + str(i)
    button_add = QPushButton(title, w)
    vbox.addWidget(button_add)
    i += 1
    
w.setLayout(vbox)

w.show()

sys.exit(a.exec_())
