# Reference: https://www.etutorialspoint.com/index.php/324-eye-detection-program-in-python-opencv#:~:text=The%20eye%2Ddetection%20algorithms%20focus,as%20well%20as%20detect%20objects.

# Ref: https://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv

# Ref: https://docs.opencv.org/3.4/d2/d99/tutorial_js_face_detection.html

import cv2
import numpy
from typing import List, Any

def detect_eyes(image) -> List[Any]:
    """
    Returns an array of objects representing detected faces.
    Each object contains a 'face' attribute and an 'eyes' attribute. The 'face' attribute is a 1D array representing the coordinates of the face in the image. The 'eyes' attribute is a 2D array representing all detected eyes for the face.

    Detected faces and eyes are in the shape of a 1D array [x,y,w,h], where:
        (x,y) marks the upper left corner of the detected feature's bounding box in the image
        w is the width of the bounding box
        h is the height of the bounding box
    """
    eye_cascade = cv2.CascadeClassifier(classifier_file('haarcascade_mcs_righteye.xml'))
    frontal_face_cascade = cv2.CascadeClassifier(classifier_file('haarcascade_frontalface_default.xml'))
    nose_cascade = cv2.CascadeClassifier(classifier_file('haarcascade_mcs_nose.xml'))
    
    faces = frontal_face_cascade.detectMultiScale(image, scaleFactor = 1.1, minNeighbors = 3)

    result = []

    for (x,y,w,h) in faces:
        # cv2.rectangle(image,(x,y),(x+w,y+h),(102, 0, 255),5)
        face = [int(x),int(y),int(w),int(h)]

        cand_eyes = eye_cascade.detectMultiScale(image[y:y+h, x:x+w], scaleFactor = 1.25, minNeighbors = 5)
        cand_noses = nose_cascade.detectMultiScale(image[y:y+h, x:x+w], scaleFactor = 1.2, minNeighbors = 3)

        nose = find_nose(cand_noses, (w,h))

        face_x = x
        face_y = y
        
        for (x,y,w,h) in cand_noses:
            x = x + face_x  # offset within face area
            y = y + face_y  # offset within face area
            # cv2.rectangle(image,(x,y),(x+w,y+h),(240, 154, 104),5)

        eyes = []

        for (x,y,w,h) in cand_eyes:
            if nose is not None and y > nose[1]:
                continue

            eyes.append([int(x),int(y),int(w),int(h)])

            # cv2.rectangle(image,(x,y),(x+w,y+h),(255, 102, 0),5)
            # cv2.circle(image, (x,y), radius=5, color=(34, 255, 0), thickness=3)
            # cv2.circle(image, (x+w,y+h), radius=5, color=(184, 0, 18), thickness=3)
            # print(f'x: {x}, y: {y}, w: {w}, h: {h}')
        
        if len(eyes) > 0:
            face = {
                'face': face,
                'eyes': eyes
            }
            result.append(face)
    
    return result

def find_nose(candidates: numpy.ndarray, face_size: tuple) -> numpy.ndarray:
    if len(candidates) == 0:
        return None
    elif len(candidates) == 1:
        return candidates[0]
    w, h = face_size
    # Expect the nose to be roughly in the center of the face
    face_center = (int(w/2), int(h/2))

    def distance_from_center(box_coords: numpy.ndarray):
        x1, y1, w, h = box_coords # box coords are relative to the face
        x2 = x1+w
        y2 = y1+h
        box_center = (
            int(x1+(x2-x1)/2), 
            int(y1+(y2-y1)/2)
        )
        # Euclidean distance between box center and center of the face
        return numpy.linalg.norm(numpy.subtract(box_center, face_center))

    best_cand = min(candidates, key=distance_from_center)

    return best_cand

def apply_lasers(image, faces, laser_scale: float):
    """
    Overlay a laser at each detected eye on each face
    
    laser_scale determines the size of the laser relative to the eye
    """

    laser_img = cv2.imread("laser_eyes/assets/lasers/laser.png", -1)
    laser_img_w = laser_img.shape[1]
    laser_img_h = laser_img.shape[0]

    image_width = image.shape[1]
    image_height = image.shape[0]

    for f in faces:
        [x,y,w,h] = f['face']
        face_x = x
        face_y = y
        
        for [x,y,w,h] in f['eyes']:
            x = x + face_x  # offset within face area
            y = y + face_y  # offset within face area

            width = round(float(w) * float(laser_scale))   # desired width of laser image
            height = int(width * (laser_img_h / laser_img_w))
            scaled_laser_img = cv2.resize(laser_img, (width, height))
            scaled_laser_width = scaled_laser_img.shape[1]
            scaled_laser_height = scaled_laser_img.shape[0]
            x_start = int(x + (w/2) - int(scaled_laser_width) / 2) # horizontally center the laser image within the bounding box
            y_start = int(y + (h/2)) - int(scaled_laser_height / 2) # vertically center the laser image within the bounding box

            y1, y2 = y_start, y_start + scaled_laser_height
            x1, x2 = x_start, x_start + scaled_laser_width

            # If the laser goes out of bounds on the image, determine the cutoff points
            x1_trim = min(x1, 0)
            x2_trim = max(x2-image_width, 0)
            y1_trim = min(y1, 0)
            y2_trim = max(y2-image_height, 0)

            x1_img, x2_img = x1-x1_trim, x2-x2_trim
            y1_img, y2_img = y1-y1_trim, y2-y2_trim

            x1_laser, x2_laser = -1 * x1_trim, scaled_laser_width - x2_trim
            y1_laser, y2_laser = -1 * y1_trim, scaled_laser_height - y2_trim

            # print(f'IMG SIZE: {image_width} x {image_height} \nLASER SIZE: {scaled_laser_width} x {scaled_laser_height}\nx_start: {x1} x_finish: {x2} y_start: {y1} y_finish: {y2}\nx1_trim: {x1_trim} x2_trim: {x2_trim} y1_trim: {y1_trim} y2_trim: {y2_trim}\nx1_img: {x1_img} x2_img: {x2_img} y1_img: {y1_img} y2_img: {y2_img}\nx1_laser: {x1_laser} x2_laser: {x2_laser} y1_laser: {y1_laser} y2_laser: {y2_laser}')

            alpha_s = scaled_laser_img[y1_laser:y2_laser, x1_laser:x2_laser, 3] / 255.0
            alpha_l = 1.0 - alpha_s

            for c in range(0, 3):
                image[y1_img:y2_img, x1_img:x2_img, c] = (
                        alpha_s * scaled_laser_img[y1_laser:y2_laser, x1_laser:x2_laser, c] +
                        alpha_l * image[y1_img:y2_img, x1_img:x2_img, c]
                    )

    return image

def classifier_file(filename: str) -> str:
    classifier_dir = 'laser_eyes/assets/classifiers'
    return f'{classifier_dir}/{filename}'