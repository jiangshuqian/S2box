#!/usr/bin/python2
import scipy.weave as weave
import cv2
import numpy as np

def detect(img):
    rows, cols, _ = np.shape(img)
    outimg = np.zeros((rows, cols), np.uint8)
    code = '''
    for(int i = 0; i < rows; i++)
    {
        for(int j = 0; j < cols; j++)
        {
            if(img(i,j,1) >= 0.84*img(i,j,0) + 50 & img(i,j,2) <= img(i,j,1) - 20)
            {
                outimg(i,j) = 255;
            }
        }
    }
    '''
    weave.inline(
        code,['img','outimg','rows','cols'],
        type_converters=weave.converters.blitz,
        compiler = 'gcc')
    return outimg

def select(img):
    outimg = detect(img)
    kernel = np.ones((3,3),np.uint8)
    _,othresh = cv2.threshold(outimg,127,255,0)
    thresh = cv2.morphologyEx(othresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    return thresh

if __name__ == '__main__':
    cap = cv2.VideoCapture('output.avi')
    #cap = cv2.VideoCapture(0)
    while True:
        ret,frame=cap.read()
        if not ret:
            print 'camera not found'
            break
        img=select(frame)
        cv2.imshow('thresh',img)
        _,contours, _ = cv2.findContours(img,0,1)
        for cnt in contours:
            area=cv2.contourArea(cnt)
            if area > 300:
                x,y,w,h = cv2.boundingRect(cnt)
                hull = cv2.convexHull(cnt)
                hull_area = cv2.contourArea(hull)
                perimeter = cv2.arcLength(cnt,True)
                solidity = float(area)/hull_area
                #ne = float(perimeter)/hull_area
                text = '%1.2f' %solidity
                #text = '%1.2f' %ne
                cv2.putText(frame,text,(x,y), cv2.FONT_HERSHEY_SIMPLEX,1,(127,0,255),2)
                #outimg = othresh[y:y+h,x:x+w]
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
