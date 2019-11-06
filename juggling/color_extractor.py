import cv2
import numpy


class ColorExtractor:
    def __init__(self, image, rectangle):
        self.__image = image
        self.__region = rectangle

    def contains(self, color_range):
        mask = numpy.full((self.__image.shape[0], self.__image.shape[1]), 0, dtype=numpy.uint8)

        (x, y, w, h) = self.__region
        cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)

        image_region = cv2.bitwise_or(self.__image, self.__image, mask=mask)

        image_hsv = cv2.cvtColor(image_region, cv2.COLOR_BGR2HSV)

        mask_color_hsv = cv2.inRange(image_hsv, color_range[0][0], color_range[0][1])
        for index_range in range(1, len(color_range)):
            color_range = color_range[index_range]
            mask_additional_hsv = cv2.inRange(image_hsv, color_range[0], color_range[1])

            mask_color_hsv = cv2.bitwise_or(mask_color_hsv, mask_additional_hsv)

        average_color = cv2.mean(self.__image, mask_color_hsv)
        return average_color != (0.0, 0.0, 0.0, 0.0)
