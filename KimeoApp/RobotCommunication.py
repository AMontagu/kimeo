#This is a singleton class for send action to the robot.

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
            RobotCommunication.instance = RobotCommunication.__CommandHandler()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def receiveMessage(self):
        pass

    def move(self):
        pass

    def changeRobotFace(self):
        pass

    def makeSound(self):
        pass
