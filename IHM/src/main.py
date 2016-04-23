import sys
sys.path.append('/home/pi/Desktop/Kimeo/kimeo/IPC')
sys.path.append('/home/pi/Desktop/Kimeo/kimeo/soundControl')

from MainUI import MainWidget
from PyQt4.QtGui import QApplication
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from ActionOnJson import *
from sound import *
from threading import *

MainWindow = MainWidget()

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*"]
        
    def on_modified(self, event):
        print(event.src_path, event.event_type)
        if event.src_path == fileForScreen:
            actionOnJson = ActionOnJson(fileForScreen)
            jsonText = actionOnJson.getJson()
            imageName = jsonText["imageName"]
            # timeToStay = jsonText["timeToStay"]
            # stay = jsonText["stay"]
            if imageName == "angry":
                MainWindow.setEmotion("angry")
            if imageName == "happy":
                MainWindow.setEmotion("happy")
            if imageName == "neutral":
                MainWindow.setEmotion("neutral")
            if imageName == "sad":
                MainWindow.setEmotion("sad")
            if imageName == "message":
                MainWindow.setEmotion("message")
            if imageName == "batterie":
                MainWindow.setEmotion("batterie")
            if imageName == "sleepy":
                MainWindow.setEmotion("sleepy")
            if imageName == "love":
                MainWindow.setEmotion("love")

repo = "/home/pi/Desktop/Kimeo/kimeo/IHM/"

if __name__ == "__main__":

    print(sys.version_info)

    app = QApplication(sys.argv)
    
    MainWindow.showFullScreen()
    #MainWindow.show()
    observer = Observer()
    
    observer.schedule(MyHandler(), '/home/pi/Desktop/Kimeo/kimeo/IPC')
    
    observer.start()
    
    try:
        app.exec_()
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

