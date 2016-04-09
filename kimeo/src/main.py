#!/usr/bin/python

from MainUI import MainWidget
from PyQt4.QtGui import QApplication
import os
import sys

repo = "/home/pi/Desktop/Kimeo/kimeo/kimeo/"

def launch():
    app = QApplication(sys.argv)

    MainWindow = MainWidget()
    MainWindow.showFullScreen()

    app.exec_()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    
    MainWindow = MainWidget()
    MainWindow.showFullScreen()
    
    app.exec_()
