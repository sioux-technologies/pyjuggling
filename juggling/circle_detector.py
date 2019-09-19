"""
Module contains classes that provide circle detection functionality:
- CircleDetector - common circle detection.
- ColorCircleDetector - circle detection with specific color.
"""

import cv2

from pyclustering.cluster.agglomerative import agglomerative


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
        if circles is None:
            return None

        unique_circles = []
        unique_map = [True] * len(circles)
        for i in range(0, len(circles)):
            if unique_map[i] is True:
                for j in range(i + 1, len(circles)):
                    if circles[i] == circles[j] or circles[i][2] == circles[j][2]:
                        unique_map[j] = False

                unique_circles.append(circles[i])

        return unique_circles

    def _is_overlapped(self, a_min, a_max, b_min, b_max):
        return not ((a_min > b_max) or (b_min > a_max))

    def _remove_overlapped_circles(self, circles):
        if circles is None:
            return None

        result = []
        overlapped_map = [False] * len(circles)

        for i in range(0, len(circles)):
            if overlapped_map[i] is True:
                continue

            result.append(circles[i])

            for j in range(i + 1, len(circles)):
                r1_left, r1_right = circles[i][0] - circles[i][2], circles[i][0] + circles[i][2]
                r2_left, r2_right = circles[j][0] - circles[j][2], circles[j][0] + circles[j][2]

                r1_bottom, r1_top = circles[i][1] - circles[i][2], circles[i][1] + circles[i][2]
                r2_bottom, r2_top = circles[j][1] - circles[j][2], circles[j][1] + circles[j][2]

                if self._is_overlapped(r1_left, r1_right, r2_left, r2_right) and self._is_overlapped(r1_bottom, r1_top, r2_bottom, r2_top):
                    overlapped_map[i] = True
                    overlapped_map[j] = True

                    # print("%d overlap %d" % (i, j))

        return result

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
        circles = self._remove_duplicate_circles(circles)
        return self._remove_overlapped_circles(circles)

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
        return self.__get_by_color_detection(amount)

    def __get_farthest_circles(self, circles, clusters):
        result = []
        for cluster in clusters:
            biggest_index = cluster[0]
            biggest_square = 3.14 * circles[biggest_index][2] * circles[biggest_index][2]

            for i in range(1, len(cluster)):
                candidate_index = cluster[i]
                candidate_square = 3.14 * circles[candidate_index][2] * circles[candidate_index][2]

                if candidate_square > biggest_square:
                    biggest_index = candidate_index
                    biggest_square = candidate_square

            result.append(circles[biggest_index])

        return result

    def __get_circles_from_contours(self, contours):
        circles = []
        for contour in contours:
            moments = cv2.moments(contour)
            if moments["m00"] == 0.0:
                continue

            x, y = int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"])
            _, _, w, h = cv2.boundingRect(contour)
            r = int(max(w, h) / 2)

            circles.append((x, y, r))

        return circles

    def __build_circles_from_contour(self, color_mask, amount):
        _, contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) < amount:
            return None

        circles = self.__get_circles_from_contours(contours)
        if len(circles) < amount:
            return None

        coordinates = [[c[0], c[1]] for c in circles]

        clustering_algorithm = agglomerative(coordinates, amount)
        clustering_algorithm.process()
        clusters = clustering_algorithm.get_clusters()

        return self.__get_farthest_circles(circles, clusters)

    def __get_by_color_detection(self, amount):
        image = cv2.blur(self._source_image, (11, 11))
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask_left_hsv = cv2.inRange(image_hsv, (0, 190, 120), (10, 255, 255))
        mask_right_hsv = cv2.inRange(image_hsv, (170, 190, 120), (180, 255, 255))

        color_mask_hsv = cv2.bitwise_or(mask_left_hsv, mask_right_hsv)

        # image_cropped = cv2.bitwise_and(image, image, mask=color_mask_hsv)
        # cv2.imshow("Cropped", image_cropped)

        circles = self.__build_circles_from_contour(color_mask_hsv, amount)

        if (circles is not None) and (len(circles) != amount):
            return None

        return circles
