import pypot.dynamixel
import time


class Motor:
    def __init__(self, motorRight = 7, motorLeft = 4, motorHead = 11):
        self.ports = pypot.dynamixel.get_available_ports()
        if not self.ports or self.ports[0] == "/dev/ttyAMAO":
            self.available = False
            print('No port available for motor.')
        else:
            self.available = True
            self.dxl_io = pypot.dynamixel.DxlIO(self.ports[0])
            self.motorRight = motorRight
            self.motorRightAvailable = False
            self.motorLeft = motorLeft
            self.motorLeftAvailable = False
            self.motorHead = motorHead
            self.motorHeadAvailable = False
            self.initMotor(motorRight,motorLeft,motorHead)
            self.oldPositionhead = 45

    def initMotor(self, motorRight, motorLeft, motorHead):
        self.motorRight = motorRight
        self.motorRightAvailable = False
        self.motorLeft = motorLeft
        self.motorLeftAvailable = False
        self.motorHead = motorHead
        self.motorHeadAvailable = False
        if self.motorRight != 0:
            self.setMotorWheelMode(self.motorRight)
            self.motorRightAvailable = True
        if self.motorLeft != 0:
            self.setMotorWheelMode(self.motorLeft)
            self.motorLeftAvailable = True
        if self.motorHead != 0:
            self.setMotorWheelMode(motorHead)
            self.motorHeadAvailable = True
            # self.dxl_io.set_wheel_mode((motorLeft,motorRight, motorHead))

    def printInfo(self):
        print(pypot.dynamixel.get_available_ports())
        print(self.dxl_io.scan())
        if self.available:
            if self.motorRightAvailable:
                print(self.dxl_io.get_control_mode((self.motorRight,)))
            if self.motorLeftAvailable:
                print(self.dxl_io.get_control_mode((self.motorLeft,)))
            if self.motorHeadAvailable:
                print(self.dxl_io.get_control_mode((self.motorHead,)))

    def moveForward(self, rightSpeed, leftSpeed, duration):
        if self.available:
            rightSpeed = float(rightSpeed)
            leftSpeed = float(leftSpeed)
            self.move(rightSpeed,leftSpeed,duration)
        else:
            print("can't move no open port are available")

    def moveBackward(self, rightSpeed, leftSpeed, duration):
        if self.available:
            rightSpeed = float(rightSpeed)
            leftSpeed = float(leftSpeed)
            self.move(-rightSpeed, -leftSpeed, duration)
        else:
            print("can't move no open port are available")

    def turnLeft(self, rightSpeed, leftSpeed, duration):
        if self.available:
            rightSpeed = float(rightSpeed)
            leftSpeed = float(leftSpeed)
            self.move(-rightSpeed, leftSpeed, duration)
        else:
            print("can't move no open port are available")

    def turnRight(self, rightSpeed, leftSpeed, duration):
        if self.available:
            rightSpeed = float(rightSpeed)
            leftSpeed = float(leftSpeed)
            self.move(rightSpeed, -leftSpeed, duration)
        else:
            print("can't move no open port are available")

    def moveHead(self, positionHead, headSpeed = 100.0):
        positionHead = int(positionHead)
        self.dxl_io.set_moving_speed({self.motorHead, headSpeed})
        self.oldPositionhead = positionHead
        #TODO calculate time with inclinaison
        self.dxl_io.set_moving_speed({self.motorHead, 0})

    def move(self, rightSpeed, leftSpeed, duration):
        if self.motorRightAvailable:
            self.dxl_io.set_moving_speed({self.motorRight: rightSpeed})
        if self.motorLeftAvailable:
            self.dxl_io.set_moving_speed({self.motorLeft: leftSpeed})
        time.sleep(duration)
        if self.motorRightAvailable:
            self.dxl_io.set_moving_speed({self.motorRight: 0.0})
        if self.motorLeftAvailable:
            self.dxl_io.set_moving_speed({self.motorLeft: 0.0})

    def setMotorWheelMode(self, motor):
        self.dxl_io.set_wheel_mode((motor,))


if __name__ == '__main__':
    motor = Motor(7,0,0)
    motor.printInfo()
    motor.moveForward(200,200,5)