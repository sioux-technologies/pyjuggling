import cv2


class CircleDetector:
    _cache_center_threshold = 250

    def __init__(self, image):
        self._source_image = image
        self._dp = 2.0
        self._max_radius = int(self._source_image.shape[0] / 8)
        self._min_distance = int(self._source_image.shape[0] / 16)

    def __remove_empty_circles(self, circles):
        """Removes from the collection empty circles. Despite minimum radius OpenCV returns circles with 0 radius.

        :param circles: Collection of circles that should be checked for empty circles.
        :return: Collection without empty circles.
        """
        if circles is not None:
            return [circle.astype(int).tolist() for circle in circles[0, :] if circle[2] > 0]
        return None

    def __remove_duplicate_circles(self, circles):
        """Removes from the collection non-unique circles. Despite minimum distance OpenCV returns circles with the
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

    def _get_circles(self, gray_image, center_threshold):
        """Search circles using HoughCircles procedure and return only correct circles.

        :param gray_image: Gray scaled image that is used for circle searching.
        :param center_threshold: Center threshold parameter.
        :return: Collection without empty and non-unique circles.
        """
        circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, self._dp, self._min_distance,
                                   param2=center_threshold, maxRadius=self._max_radius)

        if circles is not None:
            circles.astype(int)

        circles = self.__remove_empty_circles(circles)
        return self.__remove_duplicate_circles(circles)

    def _binary_search(self, gray_image, amount):
        """Performs binary search of proper center threshold to extract required amount of circles.

        :param gray_image: Gray scaled image.
        :param amount: Required amount of circles that should found.
        :return: Center threshold parameter and allocated circles.
        """
        left, center_threshold, right = 1, CircleDetector._cache_center_threshold, 500
        circles = self._get_circles(gray_image, center_threshold)

        while ((circles is None) or (len(circles) != amount)) and abs(left - right) > 1:
            if (circles is None) or (len(circles) < amount):
                right = center_threshold
            elif len(circles) > amount:
                left = center_threshold

            center_threshold = (left + right) / 2
            circles = self._get_circles(gray_image, center_threshold)

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
    def __init__(self, image, circle_color):
        super().__init__(image)
        self._circle_color = circle_color

    def get(self, amount=1):
        pass
