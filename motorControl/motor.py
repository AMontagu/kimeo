import pypot.dynamixel
import time


class Motor:
    def __init__(self, motorRight = 7, motorLeft = 4, motorHead = 11):
        self.ports = pypot.dynamixel.get_available_ports()
        if not self.ports:
            raise IOError('No port available.')
        self.dxl_io = pypot.dynamixel.DxlIO(self.ports[0])
        self.motorRight = motorRight
        self.motorLeft = motorLeft
        self.motorHead = motorHead
        self.dxl_io.set_wheel_mode((motorLeft,motorRight, motorHead))
        print(self.dxl_io.get_control_mode((motorLeft,motorRight,motorHead)))

    def printInfo(self):
        print(pypot.dynamixel.get_available_ports())
        print(self.xl_io.scan())

    def moveForward(self, rightSpeed, leftSpeed, duration):
        rightSpeed = float(rightSpeed)
        leftSpeed = float(leftSpeed)
        self.dxl_io.set_moving_speed({self.motorRight: rightSpeed})
        self.dxl_io.set_moving_speed({self.motorLeft: leftSpeed})
        self.dxl_io.set_moving_speed({self.motorHead: 100.0})
        time.sleep(duration)
        self.dxl_io.set_moving_speed({self.motorRight: 0.0})
        self.dxl_io.set_moving_speed({self.motorLeft: 0.0})
        self.dxl_io.set_moving_speed({self.motorHead: 0.0})

    def moveBackward(self, rightSpeed, leftSpeed, duration):
        rightSpeed = float(rightSpeed)
        leftSpeed = float(leftSpeed)
        self.dxl_io.set_moving_speed({self.motorRight: -rightSpeed})
        self.dxl_io.set_moving_speed({self.motorLeft: -leftSpeed})
        time.sleep(duration)
        self.dxl_io.set_moving_speed({self.motorRight: 0.0})
        self.dxl_io.set_moving_speed({self.motorLeft: 0.0})

    def turnLeft(self, rightSpeed, leftSpeed, duration):
        rightSpeed = float(rightSpeed)
        leftSpeed = float(leftSpeed)
        self.dxl_io.set_moving_speed({self.motorRight: -rightSpeed})
        self.dxl_io.set_moving_speed({self.motorLeft: leftSpeed})
        time.sleep(duration)
        self.dxl_io.set_moving_speed({self.motorRight: 0.0})
        self.dxl_io.set_moving_speed({self.motorLeft: 0.0})

    def turnRight(self, rightSpeed, leftSpeed, duration):
        rightSpeed = float(rightSpeed)
        leftSpeed = float(leftSpeed)
        self.dxl_io.set_moving_speed({self.motorRight: rightSpeed})
        self.dxl_io.set_moving_speed({self.motorLeft: -leftSpeed})
        time.sleep(duration)
        self.dxl_io.set_moving_speed({self.motorRight: 0.0})
        self.dxl_io.set_moving_speed({self.motorLeft: 0.0})


if __name__ == '__main__':
    motor = Motor(10,4,7)
    motor.moveForward(100,100,5)