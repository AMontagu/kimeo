#!/usr/bin/python

from MainUI import MainWidget
from PyQt4.QtGui import QApplication
import os
import sys
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from IPC.ActionOnJson import *

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*"]

    def on_modified(self, event):
        print(event.src_path, event.event_type)
        if(event.src_path == fileForScreen):
            actionOnJson = ActionOnJson(fileForScreen)
            jsonText = actionJson.getJson()
            # imageName = jsonText["imageName"]
            # timeToStay = jsonText["timeToStay"]
            # stay = jsonText["stay"]
            print ("Ludo do something here !")

repo = "/home/pi/Desktop/Kimeo/kimeo/IHM/"

if __name__ == "__main__":

    app = QApplication(sys.argv)
    
    MainWindow = MainWidget()
    MainWindow.showFullScreen()

    observer = Observer()
    observer.schedule(MyHandler(), '/home/pi/Desktop/Kimeo/kimeo/IPC')
    observer.start()

    try:
        app.exec_()
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

