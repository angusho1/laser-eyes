# Reference: https://www.etutorialspoint.com/index.php/324-eye-detection-program-in-python-opencv#:~:text=The%20eye%2Ddetection%20algorithms%20focus,as%20well%20as%20detect%20objects.

# Ref: https://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv

import cv2

def detect_eyes(image):
    eye_cascade = cv2.CascadeClassifier('laser_eyes/assets/classifiers/haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(image, scaleFactor = 1.1, minNeighbors = 3)

    laser_img = cv2.imread("laser_eyes/assets/lasers/laser.png", -1)
    laser_img_w = laser_img.shape[1]
    laser_img_h = laser_img.shape[0]

    for (x,y,w,h) in eyes:
        width = w
        height = int(width * (laser_img_h / laser_img_w))
        scaled_laser_img = cv2.resize(laser_img, (width, height))
        scaled_laser_height = scaled_laser_img.shape[0]
        y_start = int(y + (h/2)) - int(scaled_laser_height / 2)

        y1, y2 = y_start, y_start + scaled_laser_height
        x1, x2 = x, x + scaled_laser_img.shape[1]

        alpha_s = scaled_laser_img[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            image[y1:y2, x1:x2, c] = (alpha_s * scaled_laser_img[:, :, c] +
                                    alpha_l * image[y1:y2, x1:x2, c])

        # cv2.rectangle(image,(x,y),(x+w,y+h),(0, 255, 0),5)
    
    return image
    