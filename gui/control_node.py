from gui import *
from visros import *

def main():
    app = QtGui.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    app.exec_()

    data_tuple = gui.get_data()
    print data_tuple


    monitor = Monitor()
    monitor.show()
    app.exec_()
if __name__ == '__main__':
    main()
