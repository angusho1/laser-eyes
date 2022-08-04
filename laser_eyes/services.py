# Reference: https://www.etutorialspoint.com/index.php/324-eye-detection-program-in-python-opencv#:~:text=The%20eye%2Ddetection%20algorithms%20focus,as%20well%20as%20detect%20objects.

import cv2

def detect_eyes(image):
    eye_cascade = cv2.CascadeClassifier('laser_eyes/classifiers/haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(image, scaleFactor = 1.2,
                                    minNeighbors = 4)
 
 
    for (x,y,w,h) in eyes:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0, 255, 0),5)
    
    return image
    