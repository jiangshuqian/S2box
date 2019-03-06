#!/usr/bin/python2
import time
import serial
import threading
from math import atan

class sendOrders():

    def __init__(self, port, baudrate):
        self.__ser = serial.Serial(port, baudrate)
        self.__sent = False
        self.__wtime = time.time()
        self.__position = 0
        self.__model = '0'
        self.__parameter = ''
        if not self.__ser.isOpen():
            print 'serial not found...'

    def send(self, scmd):
        while(self.__sent):pass
        self.__sent = True
        scmd = scmd + '\r\n'
        self.__ser.write(scmd)
        self.__sent = False

    def readm(self):
        return self.__model

    def readp(self):
        time.sleep(0.1)
        return self.__parameter

    def bmodel(self):
        p = threading.Thread(target=self.__readmodel)
        p.setDaemon(True)
        p.start()
        return

    def __readmodel(self):
        time.sleep(0.5)
        while True:
            md = self.__ser.read(1)
            if md=='Y':
                self.__model = ''
                while True:
                    cmd = self.__ser.read(1)
                    if cmd == 'Z':
                        break
                    self.__model =self.__model + str(cmd)
            elif md=='X':
                self.__parameter = ''
                while True:
                    cmd = self.__ser.read(1)
                    if cmd == 'Z':
                        break
                    self.__parameter =self.__parameter + str(cmd)

    def __mvstart(self, scmd, wait_time, nozzle_number, c_ratio=2000):
        if nozzle_number==1:
            scmd = str(scmd) + 'e'
            val = 'h'
        elif nozzle_number==2:
            scmd = str(scmd) + 'd'
            val = 'g'
        elif nozzle_number==3:
            scmd = str(scmd) + 'c'
            val = 'f'
        if wait_time > 0.25:
            delay_time = wait_time - 0.25
            time.sleep(delay_time)
            self.send(scmd)
            time.sleep(0.25)
        else:
            self.send(scmd)
            time.sleep(wait_time)
        if c_ratio>=1000:
            self.send('100' + val)
        else:
            self.send('30' + val)

    def mvgrass(self, position, wait_time, nozzle_number, grass_size):
        if abs(self.__position - position) >=4 and time.time() - self.__wtime >=0.3:
            self.__wtime = time.time()
            self.__position = position
            dx = position - 160  # dx = position - 'center position of frame'
            agl = atan(float(abs(dx))/220)*180/3.1415926 #calculate the angle, the high is 400mm now(l=357mm)
            agl=int(round(agl))
            if dx<0:
                noz = 124+agl  # noz = 'center position of nazzle'+agl
            else:
                noz = 124-agl

            threading.Thread(target=self.__mvstart,args=(noz,wait_time,nozzle_number,grass_size)).start()
        else:
            print 'input number too close!'

    def close(self):
        try:
            self.__ser.close()
            print
            print 'serial close'
        except:
            print 'serial close fail'

if __name__=='__main__':
    print 'This is a serial test code of Python'
    ser1=sendOrders('/dev/ttyUSB0',115200)
    ser1.bmodel()

    for i in range(10):
        ser1.send('l')
        print 'heigh:',ser1.readp()
        if i==2:
            ser1.mvgrass(150,0.2,2,100)
        elif i==6:
            ser1.send('50c')
        elif i==8:
            ser1.send('10b')
        elif i==9:
            ser1.send('100c')
        for j in range(10):
            print 'model:',ser1.readm()
            time.sleep(0.1)

    ser1.close()
