import cv2
from imageai.Detection import ObjectDetection
import os
import numpy
import time

execution_path = os.getcwd()

detector = ObjectDetection()
#detector.
detector.setModelPath(os.path.join(execution_path, "mask_rcnn_coco.h5"))
detector.loadModel()

custom_objects = detector.CustomObjects(sports_ball=True, baseball_bat=True, apple=True, orange=True)

#camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap = cv2.VideoCapture('ball_1.mp4')

while(True):
    _, frame = cap.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    height, width, depth = frame.shape
    imgScale = 500 / width
    newX, newY = frame.shape[1] * imgScale, frame.shape[0] * imgScale
    frame = cv2.resize(frame, (int(newX), int(newY)))
    cv2.imwrite("input.jpg", frame)

    start_time = time.time()
    detections = detector.detectCustomObjectsFromImage(custom_objects=custom_objects, input_image="input.jpg", output_image_path=os.path.join(execution_path , "result.jpg"), minimum_percentage_probability=1)
    duration = time.time() - start_time
    print(duration)

    result = cv2.imread("result.jpg")
    cv2.imshow("Result", result)
    cv2.waitKey(1)
