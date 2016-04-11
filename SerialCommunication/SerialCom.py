import threading
import time
import serial


class SerialCom(threading.Thread):
    def __init__(self, threadID, name, port = '/dev/ttyUSB1', baudrate = 9600, parity = serial.PARITY_ODD, stopbits = serial.STOPBITS_TWO, bytesize = serial.SEVENBITS):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.running = True
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize
        )

    def run(self):
        while self.running:
            self.initSerial()

            try:
                while True:
                    input = self.ser.readline()
                    print(input())
                    if(input == "test"):
                        print("receive test")
                    time.sleep(2)
            except IOError:
                pass
            self.closeSerial()

    def write(self, data):
        #maybe need ths line:
        #self.ser.write(data + '\r\n')
        print("send this : " + data)
        self.ser.write(data)

    def initSerial(self):
        self.ser.isOpen()

    def closeSerial(self):
        self.ser.close()

if __name__ == '__main__':
    serialCom = SerialCom(1, "serialThread")
    serialCom.daemon = True
    serialCom.start()

    while True:
        time.sleep(3)
        serialCom.write("testtestest")
        serialCom.write("testtestest" + "\r\n")