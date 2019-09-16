from imageai.Detection import ObjectDetection

import cv2
import os

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()

custom_objects = detector.CustomObjects(sports_ball=True, baseball_bat=True, apple=True, orange=True)
detections = detector.detectCustomObjectsFromImage(custom_objects=custom_objects, input_image=os.path.join(execution_path, "../tests/samples/photo_juggling_01.jpg"), output_image_path=os.path.join(execution_path , "result.jpg"), minimum_percentage_probability=30)

for eachObject in detections:
    print(eachObject["name"], " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"])
    print("--------------------------------")

result = cv2.imread("result.jpg")
cv2.imshow("Result", result)
cv2.waitKey(0)