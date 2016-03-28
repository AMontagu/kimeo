#This is a singleton class for send action to the robot.
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
import pypot.dynamixel
import time

class RobotCommunication:
    class __RobotCommunication:
        def __init__(self):
            #here put all the variable of the electronical component then create function for each action
            self.serialCom = "tty/com"  # need to be replace with good one
            self.dxl_io = pypot.dynamixel.DxlIO('/dev/ttyACM0')

        def __str__(self):
            return repr(self) + self.serialCom

    instance = None

    def __init__(self):
        if not RobotCommunication.instance:
            RobotCommunication.instance = RobotCommunication.__RobotCommunication()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def receiveMessage(self, dataSerialized):
        print(dataSerialized.data['content']) # data['robotId'], data['userName'], data['content'], data['created']
        #TODO condition and process for handle message

    def move(self, dataSerialized):
        typeMovement = dataSerialized.data['direction'] #data['direction'], data['speedright'], data['speedLeft'], data['duration']
        if typeMovement == "forward":
            self.dxl_io.set_moving_speed({11: float(dataSerialized.data['speedright'])})
            time.sleep(float(dataSerialized.data['duration']))
            self.dxl_io.set_moving_speed({11: 0.0})
            #TODO call serial communication for move forward the robot with speed and duration apropriate
        if typeMovement == "backward":
            pass
        if typeMovement == "turnLeft":
            pass
        if typeMovement == "turnRight":
            pass

    def changeRobotFace(self, dataSerialized):
        face = dataSerialized.data['imageName'] #data['imageName'], data['stay'], data['timeToStay']
        print(face)

    def makeSound(self, dataSerialized):
        sound = dataSerialized.data['soundName']  # data['soundName'], data['repeat']
        print(sound)

    def makeLight(self, dataSerialized):
        turnOn = dataSerialized.data['turnOn']  # data['turnOn'], data['blink'], data['repeat'], data['intervalBlinking']
        print(turnOn)
