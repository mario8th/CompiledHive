from gui import *

def main():
    app = QtGui.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    app.exec_()

    data_tuple = gui.get_data()
    print data_tuple
if __name__ == '__main__':
    main()
