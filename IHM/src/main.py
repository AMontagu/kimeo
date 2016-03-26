#!/usr/bin/python

from MainUI import MainWidget
from PyQt4.QtGui import QApplication
import os
import sys

if __name__ == "__main__":
        
    app = QApplication(sys.argv)
    
    MainWindow = MainWidget()
    MainWindow.show()
    
    app.exec_()
    