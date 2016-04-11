#This is a singleton class for send action to the robot.
from threading import Thread

from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
import pypot.dynamixel
import time
from IPC.ActionOnJson import *
from SerialCommunication.SerialCom import *
from motorControl.motor import *

class RobotCommunication:
    class __RobotCommunication:
        def __init__(self):
            self.threads = []

            threadSerialCom = SerialCom(threadID=1, name="serialThread")
            threadSerialCom.daemon = True
            threadSerialCom.start()
            self.threads.append(threadSerialCom)
            self.motorAction = Motor(7,11)

        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self):
        if not RobotCommunication.instance:
            RobotCommunication.instance = RobotCommunication.__RobotCommunication()
        else:
            pass # update class variable with parameter

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def receiveMessage(self, dataSerialized):
        print(dataSerialized.data['content']) # data['robotId'], data['userName'], data['content'], data['created']
        #TODO condition and process for handle message

    def move(self, dataSerialized):
        typeMovement = dataSerialized.data['direction'] #dataSerialized.data['direction'], dataSerialized.data['rightSpeed'], dataSerialized.data['leftSpeed'], dataSerialized.data['duration']
        print(typeMovement)
        if typeMovement == "Forward":
            print("in forward")
            th = Thread(target=self.motorAction.moveForward(dataSerialized.data['rightSpeed'], dataSerialized.data['leftSpeed'], dataSerialized.data['duration']))

        if typeMovement == "Backward":
            th = Thread(target=self.motorAction.moveBackward(dataSerialized.data['rightSpeed'], dataSerialized.data['duration'], dataSerialized.data['leftSpeed']))

        if typeMovement == "TurnLeft":
            th = Thread(target=self.motorAction.turnLeft(dataSerialized.data['rightSpeed'], dataSerialized.data['leftSpeed'], dataSerialized.data['duration']))

        if typeMovement == "TurnRight":
            th = Thread(target=self.motorAction.turnRight(dataSerialized.data['rightSpeed'], dataSerialized.data['leftSpeed'], dataSerialized.data['duration']))

        th.daemon = True
        th.start()

    def changeRobotFace(self, dataSerialized):
        face = dataSerialized.data['imageName'] #data['imageName'], data['stay'], data['timeToStay']
        print(face)
        actionOnJson = ActionOnJson(fileForScreen)
        actionJson.writeJson(dataSerialized)

    def makeSound(self, dataSerialized):
        sound = dataSerialized.data['soundName']  # data['soundName'], data['repeat']
        print(sound)

    def makeLight(self, dataSerialized):
        turnOn = dataSerialized.data['turnOn']  # data['turnOn'], data['blink'], data['repeat'], data['intervalBlinking']
        print(turnOn)
