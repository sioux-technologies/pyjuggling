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

        blur_image = cv2.blur(self.__image, (11, 11))
        average_color = cv2.mean(blur_image, circle_mask)
        return average_color
