#!/usr/bin/python
import numpy as np
import cv2
from grasscontours import detect
from box_interactive_plus import *

import sys

def getnozzleGrass(mod = 2):
    return 1,2,3

def detectGrass(cnt, area):
    grass_k = 0
    M = cv2.moments(cnt)
    x,y = int(M['m10']/M['m00']),int(M['m01']/M['m00'])
    if abs(y-140)<=8 and abs(x -120) < 100:
        if area < 1200:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            box_a = np.sqrt(np.square(box[0][0]-box[1][0])+np.square(box[0][1]-box[1][1]))
            box_b = np.sqrt(np.square(box[1][0]-box[2][0])+np.square(box[1][1]-box[2][1]))
            rato_box = box_a/box_b
            if rato_box <= 0.4 or rato_box >= 2.5:
                grass_k = 3
            else:
                hull = cv2.convexHull(cnt)
                hull_area = cv2.contourArea(hull)
                solidity = float(area)/hull_area
                if solidity > 0.8:
                    grass_k = 2
                else:
                    abarea = area/(box_a*box_b)
                    if abarea > 0.6:
                        grass_k = 2
                    else:
                        grass_k = 4
        else:
            hull = cv2.convexHull(cnt)
            hull_area = cv2.contourArea(hull)
            solidity = float(area)/hull_area
            if solidity > 0.8:
                grass_k = 2
            else:
                grass_k = 1
    return grass_k, x

def changeModel(mod,ser1):
    if mod == '1' or mod == '2':
        ser1.send('120a')
        time.sleep(0.1)
        ser1.send('15b')
        time.sleep(0.1)
        ser1.send('30i')
        time.sleep(0.1)
        ser1.send('30j')
        time.sleep(0.1)
        ser1.send('30k')
    elif mod == '3':
        ser1.send('120a')
        time.sleep(0.1)
        ser1.send('15b')
        time.sleep(0.1)
        ser1.send('50i')
        time.sleep(0.1)
        ser1.send('50j')
        time.sleep(0.1)
        ser1.send('50k')
    elif mod == '4':
        ser1.send('120a')
        time.sleep(0.1)
        ser1.send('15b')
        time.sleep(0.1)
        ser1.send('30i')
        time.sleep(0.1)
        ser1.send('30j')
        time.sleep(0.1)
        ser1.send('30k')
    elif mod == '5':
        time.sleep(0.1)
        ser1.send('a')
        time.sleep(0.1)
        ser1.send('b')
    elif mod == '0':
        pass

if __name__=='__main__':
# Init data ...
    ser1 = sendOrders('/dev/ttyUSB0',115200)
    time.sleep(0.1)
    ser1.bmodel()
    #ser1.send('o')
    time.sleep(0.1)
    ser1.send('120a')
    time.sleep(0.1)
    ser1.send('15b')
#Init Camera ...
    cap = cv2.VideoCapture(0)
    cap.set(3,320)
    cap.set(4,240)

    kernel = np.ones((3,3),np.uint8)
    origmod = 0
    ng1, ng2, ng3 = getnozzleGrass()
    while (True):
        ret, frame = cap.read()
        if not ret: break
        mod = ser1.readm()
        if mod != origmod:
            changeModel(mod, ser1)
            ng1, ng2, ng3 = getnozzleGrass(mod)
            origmod = mod

        if mod == '1' or mod == '2':
            simg = cv2.resize(frame, (320,240))
            cimg = simg[:,40:260,:]
            oimg = detect(cimg)
            img = cv2.dilate(oimg,kernel,iterations = 1)
            _,contours, _ = cv2.findContours(img,0,1)
            for cnt in contours:
                area=cv2.contourArea(cnt)
                if area > 280:
                    grass_k,x = detectGrass(cnt, area)
                    if grass_k == ng1:
                        ser1.mvgrass(x,0.25,1,area)
                    elif grass_k == ng2:
                        ser1.mvgrass(x,0.5,2,area)
                    elif grass_k == ng3:
                        ser1.mvgrass(x,0.8,3,area)
        elif mod == '3':
            simg = cv2.resize(frame, (320,240))
            cimg = simg[:,40:260,:]
            oimg = detect(cimg)
            img = cv2.dilate(oimg,kernel,iterations = 1)
            _,contours, _ = cv2.findContours(img,0,1)
            for cnt in contours:
                area=cv2.contourArea(cnt)
                if area > 280:
                    grass_k,x = detectGrass(cnt, area)
                    if grass_k == 4:
                        if x > 160:
                            ser1.mvgrass(x,0.25,1,1000)
                        else:
                            ser1.mvgrass(x,0.5,2,1000)
        elif mod == '4':
            simg = cv2.resize(frame, (320,240))
            cimg = simg[:,40:260,:]
            oimg = detect(cimg)
            img = cv2.dilate(oimg,kernel,iterations = 1)
            _,contours, _ = cv2.findContours(img,0,1)
            for cnt in contours:
                area=cv2.contourArea(cnt)
                if area > 280:
                    grass_k,x = detectGrass(cnt, area)
                    if grass_k == 4:
                        if x > 160:
                            ser1.mvgrass(x,0.25,1,1000)
                        else:
                            ser1.mvgrass(x,0.5,2,1000)
        elif mod == '5':
            time.sleep(1)
        elif mod == '0':
            #if cv2.waitKey(10) & 0xFF == ord('q'): break
            time.sleep(1)
            print 'stop...'
#        cv2.imshow('cimg',cimg)
#        cv2.imshow('img',img)
#        key = cv2.waitKey() & 0xFF
#        if key == ord('q'):
#            break
#    cap.release()
#    cv2.destroyAllWindows()
