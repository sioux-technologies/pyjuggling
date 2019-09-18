"""
Module contains classes that provide circle detection functionality:
- CircleDetector - common circle detection.
- ColorCircleDetector - circle detection with specific color.
"""

import cv2
import numpy


class CircleDetector:
    """
    Provides service to extract required amount of circles from an input image. It uses Hough algorithm to extract
    circles and binary search algorithm to find proper parameters for the algorithm.
    """
    _cache_center_threshold = 250

    def __init__(self, image):
        """Initializes circle detector instance.

        :param image: Colored image where circle detectors should be found.
        """
        self._source_image = image
        self._dp = 2.0
        self._max_radius = int(self._source_image.shape[0] / 8)
        self._min_radius = 5
        self._min_distance = int(self._source_image.shape[0] / 16)

    def _remove_empty_circles(self, circles):
        """
        Removes from the collection empty circles. Despite minimum radius OpenCV returns circles with 0 radius.

        :param circles: Collection of circles that should be checked for empty circles.
        :return: Collection without empty circles.
        """
        if circles is not None:
            return [circle.astype(int).tolist() for circle in circles[0, :] if circle[2] > 0]
        return None

    def _remove_duplicate_circles(self, circles):
        """
        Removes from the collection non-unique circles. Despite minimum distance OpenCV returns circles with the
        same radius.

        :param circles: Collection of circles that should be checked for empty circles.
        :return: Collection without non-unique circles.
        """
        if circles is not None:
            unique_circles = []
            unique_map = [True] * len(circles)
            for i in range(0, len(circles)):
                if unique_map[i] is True:
                    for j in range(i + 1, len(circles)):
                        if circles[i] == circles[j]:
                            unique_map[j] = False

                    unique_circles.append(circles[i])

            return unique_circles
        return None

    def _get_circles(self, gray_image, center_threshold, **kwargs):
        """
        Search circles using HoughCircles procedure and return only correct circles.

        :param gray_image: Gray scaled image that is used for circle searching.
        :param center_threshold: Center threshold parameter.
        :param **kwargs: Additional parameters for search.
        :return: Collection without empty and non-unique circles.
        """
        min_radius = kwargs.get('min_radius', None) or self._min_radius
        circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, self._dp, self._min_distance,
                                   param2=center_threshold, maxRadius=self._max_radius, minRadius=min_radius)

        if circles is not None:
            circles.astype(int)

        circles = self._remove_empty_circles(circles)
        return self._remove_duplicate_circles(circles)

    def _binary_search(self, gray_image, amount, **kwargs):
        """
        Performs binary search of proper center threshold to extract required amount of circles.

        :param gray_image: Gray scaled image.
        :param amount: Required amount of circles that should found.
        :param kwargs: Other arguments.
        :return: Center threshold parameter and allocated circles.
        """
        left, center_threshold, right = 1, CircleDetector._cache_center_threshold, 500
        circles = self._get_circles(gray_image, center_threshold, **kwargs)

        while ((circles is None) or (len(circles) != amount)) and abs(left - right) > 1:
            if (circles is None) or (len(circles) < amount):
                right = center_threshold
            elif len(circles) > amount:
                left = center_threshold

            center_threshold = (left + right) / 2
            circles = self._get_circles(gray_image, center_threshold, **kwargs)

        return center_threshold, circles

    def get(self, amount=1):
        """Extracts specified amount of circles from the image.

        :param amount: Required amount of circles that should found (default is 1).
        :return: Extracted circles that have been found on the image, otherwise None.
        """
        image = cv2.medianBlur(self._source_image, 11)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        threshold, circles = self._binary_search(gray_image, amount)

        if (circles is not None) and (len(circles) != amount):
            return None

        CircleDetector._cache_center_threshold = threshold
        return circles


class ColorCircleDetector(CircleDetector):
    """
    Provides service to extract specified amount of colored circles (by default red). It uses color mask and Hough
    algorithm with binary search of proper parameters.
    """
    def __init__(self, image, color_from=(0, 0, 130), color_to=(40, 40, 255)):
        """
        Initializes circle detector instance.

        :param image: Colored image where circle detectors should be found.
        :param color_from: The lowest color value that is used for detection colored circle (by default min red color).
        :param: color_to: The highest color value that is used for detection colored circle (by default max red color).
        """
        super().__init__(image)
        self._color_from = color_from
        self._color_to = color_to

    def get(self, amount=1):
        """
        Extracts specified amount of colored circles from the image.

        :param amount: Required amount of circles that should found (default is 1).
        :return: Extracted circles that have been found on the image, otherwise None.
        """
        return self.__get_by_color_contours(amount)

    def __get_by_color_detection(self, amount):
        image = cv2.blur(self._source_image, (11, 11))
        color_mask = cv2.inRange(image, self._color_from, self._color_to)

        image = cv2.bitwise_and(image, self._source_image, mask=color_mask)

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold, circles = self._binary_search(gray_image, amount)

        if (circles is not None) and (len(circles) != amount):
            return None

        CircleDetector._cache_center_threshold = threshold
        return circles

    def __get_by_color_contours(self, amount):
        image = cv2.blur(self._source_image, (13, 13))
        color_mask = cv2.inRange(image, self._color_from, self._color_to)

        _, contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) < amount:
            return None

        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        extracted_circles = []
        for contour in contours:
            moments = cv2.moments(contour)
            if moments["m00"] == 0.0:
                continue

            x, y = int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"])

            _, _, w, h = cv2.boundingRect(contour)
            side = max(w, h)
            radius = int(side / 2)

            y0, y1, x0, x1 = y - side, y + side, x - side, x + side
            if x0 < 0:
                x0 = 0
            if y0 < 0:
                y0 = 0
            if radius < self._min_radius:
                radius = self._min_radius

            segment_image = image[y0:y1, x0:x1]

            segment_gray = cv2.cvtColor(segment_image, cv2.COLOR_BGR2GRAY)
            segment_threshold, segment_circles = self._binary_search(segment_gray, 1, min_radius=radius)

            if segment_circles is not None:
                for segment_circle in segment_circles:
                    # For debugging purpose
                    # cv2.circle(segment_image, (segment_circle[0], segment_circle[1]), segment_circle[2], (255, 0, 0), 3)
                    # cv2.imshow("Segment image", segment_image)
                    # cv2.waitKey(0)

                    x, y, r = segment_circle[0] + x0, segment_circle[1] + y0, segment_circle[2]
                    extracted_circles.append((segment_threshold, (x, y, r)))

        sorted(extracted_circles, key=lambda obj: obj[1], reverse=True)

        circles = []
        for circle_description in extracted_circles:
            circles.append(circle_description[1])

        circles = self._remove_duplicate_circles(circles)

        if circles is not None:
            circles = circles[0:amount]

        return circles
