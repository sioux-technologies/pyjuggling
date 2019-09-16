import cv2
import numpy


class PatternSearcher:
    def __init__(self, learn_pattern):
        self.__pattern = cv2.cvtColor(learn_pattern, cv2.COLOR_BGR2GRAY)
        cv2.blur(self.__pattern, (11, 11))

    def search(self, image, threshold):
        cv2.blur(image, (11, 11))
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(image_gray, self.__pattern, cv2.TM_CCOEFF_NORMED)

        locations = numpy.where(result >= threshold)
        return locations
