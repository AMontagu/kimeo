#This is a singleton class for send action to the robot.
from threading import Thread
from IPC.ActionOnJson import *
from SerialCommunication.SerialCom import *
from motorControl.motor import *
from soundControl.sound import *


class RobotCommunication:
    class __RobotCommunication:
        def __init__(self, motorRight, motorLeft, motorHead, serialAvailable=True, motorAvailable=False):
            self.threads = []

            self.serialAvailable = serialAvailable
            if serialAvailable:
                self.threadSerialCom = SerialCom(threadID=1, name="serialThread")
                self.threadSerialCom.daemon = True
                self.threadSerialCom.start()
                self.threads.append(self.threadSerialCom)

            self.motorAvailable = motorAvailable
            if self.motorAvailable:
                #self.motorAction = Motor(motorRight, motorLeft, motorHead)
                self.motorAction = Motor()
                self.oldMotorRight = motorRight
                self.oldMotorLeft = motorLeft
                self.oldMotorHead = motorHead
            playSound("sonKimeo/ON_OFF/on.ogg")

        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self, motorRight = 4, motorLeft = 10, motorHead = 11):
        if not RobotCommunication.instance:
            RobotCommunication.instance = RobotCommunication.__RobotCommunication(motorRight, motorLeft, motorHead)
        else:
            if self.motorAvailable:
                if(motorRight != RobotCommunication.instance.oldMotorRight or motorLeft != RobotCommunication.instance.oldMotorLeft or motorHead != RobotCommunication.instance.oldMotorHead):
                    RobotCommunication.instance.motorAction.initMotor(motorRight, motorLeft, motorHead)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def receiveMessage(self, dataSerialized):
        print(dataSerialized.data['content']) # data['robotId'], data['userName'], data['content'], data['created']
        #TODO condition and process for handle message

    def move(self, dataSerialized):
        typeMovement = dataSerialized.data['direction'] #dataSerialized.data['direction'], dataSerialized.data['rightSpeed'], dataSerialized.data['headPosition'], dataSerialized.data['leftSpeed'], dataSerialized.data['duration']
        positionHead = dataSerialized.data['headPosition']
        continu = dataSerialized.data["continu"]
        print(typeMovement)
        if self.motorAvailable:
            soundThread = Thread(target=playSound("sonKimeo/robotRoule/mouv1.ogg"))
            soundThread.daemon = True
            soundThread.start()
            rightSpeed = float(dataSerialized.data['rightSpeed'])
            leftSpeed = float(dataSerialized.data['leftSpeed'])

            if typeMovement == "Forward":
                print("in forward")
                th = Thread(target=self.motorAction.move(rightSpeed, leftSpeed, dataSerialized.data['duration'], continu))
                if not continu:
                    thHead = Thread(target=self.motorAction.moveHead(positionHead))

            if typeMovement == "Backward":
                th = Thread(target=self.motorAction.move(-rightSpeed, -leftSpeed, dataSerialized.data['duration'], continu))
                if not continu:
                    thHead = Thread(target=self.motorAction.moveHead(positionHead))

            if typeMovement == "TurnLeft":
                th = Thread(target=self.motorAction.move(-rightSpeed, leftSpeed, dataSerialized.data['duration'], continu))
                if not continu:
                    thHead = Thread(target=self.motorAction.moveHead(positionHead))

            if typeMovement == "TurnRight":
                th = Thread(target=self.motorAction.move(rightSpeed, -leftSpeed, dataSerialized.data['duration'], continu))
                if not continu:
                    thHead = Thread(target=self.motorAction.moveHead(positionHead))

            if typeMovement == "Stop":
                th = Thread(target=self.motorAction.stop())

            th.daemon = True
            th.start()
            thHead.daemon = True
            thHead.start()

    def changeRobotFace(self, dataSerialized):
        face = dataSerialized.data['imageName'] #data['imageName'], data['stay'], data['timeToStay']
        stay = dataSerialized.data['stay']
        timeToStay = dataSerialized.data['timeToStay']
        print(face)
        actionOnJson = ActionOnJson(fileForScreen)
        screenJsonSerializer = ScreenJsonSerializer(face,stay,timeToStay)
        actionOnJson.writeJson(screenJsonSerializer.__dict__)

    def makeSound(self, dataSerialized):
        sound = dataSerialized.data['soundName']  # data['soundName'], data['repeat']
        repeat = dataSerialized.data['repeat']
        th = Thread(target=playSound(sound, repeat))
        th.daemon = True
        th.start()

        print(sound)

    def makeLight(self, dataSerialized):
        turnOn = dataSerialized.data['turnOn']  # data['turnOn'], data['blink'], data['repeat'], data['intervalBlinking']
        blink = dataSerialized.data['blink']
        repeat = dataSerialized.data['repeat']
        intervalBlinking = dataSerialized.data['intervalBlinking']
        if self.serialAvailable:
            """for t in self.threads:
                print(t.getName())
                if t.getName() == "serialThread":
                    t.write(turnOn + "," + blink + "," + repeat + "," + intervalBlinking)"""
            if turnOn:
                self.threadSerialCom.write("lightOn")
            else:
                self.threadSerialCom.write("lightOff")
            print(turnOn)
