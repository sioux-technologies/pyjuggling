import cv2
import numpy


class ColorExtractor:
    def __init__(self, image, circle_region):
        self.__image = image
        self.__region = circle_region

    def extract(self):
        circle_mask = numpy.zeros(shape=self.__image.shape[:2], dtype=numpy.uint8)
        cv2.circle(circle_mask, (self.__region[0], self.__region[1]), self.__region[2],
                   255, thickness=-1)

        average_color = cv2.mean(self.__image, circle_mask)
        return average_color
