import sys

import time

print(sys.version_info)
print(sys.executable)
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

    print(sys.version_info)

    observer = Observer()
    observer.schedule(MyHandler(), '/home/pi/Desktop/Kimeo/kimeo/IPC')
    observer.start()

    try:
        while True:
            time.sleep(3)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
