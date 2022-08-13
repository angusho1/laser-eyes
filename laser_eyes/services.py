# Reference: https://www.etutorialspoint.com/index.php/324-eye-detection-program-in-python-opencv#:~:text=The%20eye%2Ddetection%20algorithms%20focus,as%20well%20as%20detect%20objects.

# Ref: https://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv

# Ref: https://docs.opencv.org/3.4/d2/d99/tutorial_js_face_detection.html

import cv2

def detect_eyes(image):
    eye_cascade = cv2.CascadeClassifier('laser_eyes/assets/classifiers/haarcascade_eye.xml')
    frontal_face_cascade = cv2.CascadeClassifier('laser_eyes/assets/classifiers/haarcascade_frontalface_default.xml')
    
    faces = frontal_face_cascade.detectMultiScale(image, scaleFactor = 1.1, minNeighbors = 3)

    laser_img = cv2.imread("laser_eyes/assets/lasers/laser.png", -1)
    laser_img_w = laser_img.shape[1]
    laser_img_h = laser_img.shape[0]

    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(102, 0, 255),5)

        eyes = eye_cascade.detectMultiScale(image[y:y+h, x:x+w], scaleFactor = 1.2, minNeighbors = 3)

        face_x = x
        face_y = y

        for (x,y,w,h) in eyes:
            x = x + face_x
            y = y + face_y

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

            cv2.rectangle(image,(x,y),(x+w,y+h),(255, 102, 0),5)
            # cv2.circle(image, (x,y), radius=5, color=(34, 255, 0), thickness=3)
            # cv2.circle(image, (x+w,y+h), radius=5, color=(184, 0, 18), thickness=3)
            # print(f'x: {x}, y: {y}, w: {w}, h: {h}')
    
    return image
    