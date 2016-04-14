import sys
sys.path.append('/home/pi/Desktop/Kimeo/kimeo/IPC')
sys.path.append('/home/pi/Desktop/Kimeo/kimeo/soundControl')

from MainUI import MainWidget
from PyQt4.QtGui import QApplication
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from ActionOnJson import *
from sound import *

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
                th = Thread(target=playSound("angry/angry.ogg"))
                th.daemon = True
                th.start()
            if imageName == "happy":
                th = Thread(target=playSound("happy/happy.ogg"))
                th.daemon = True
                th.start()
            print("Ludo do something in the conditional expression above !")

repo = "/home/pi/Desktop/Kimeo/kimeo/IHM/"

if __name__ == "__main__":

    print(sys.version_info)

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

