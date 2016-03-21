#This is a singleton class for send action to the robot.
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser

class RobotCommunication:
    class __RobotCommunication:
        def __init__(self):
            #here put all the variable of the electronical component then create function for each action
            self.serialCom = "tty/com"  # need to be replace with good one

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
            #TODO call serial communication for move forward the robot with speed and duration apropriate
            pass
        if typeMovement == "backward":
            pass
        if typeMovement == "turnLeft":
            pass
        if typeMovement == "turnRight":
            pass

    def changeRobotFace(self):
        pass

    def makeSound(self):
        pass
