import cv2


class CircleDetector:
    def __init__(self, image):
        self._source_image = image
        self._dp = 2.0
        self._max_radius = int(self._source_image.shape[0] / 4)
        self._min_distance = int(self._source_image.shape[0] / 16)


    def __remove_empty_circles(self, circles):
        if circles is not None:
            return [circle for circle in circles[0, :] if circle[2] > 0]
        return None


    def _get_circles(self, gray_image, center_threshold):
        circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, self._dp, self._min_distance,
                                   param2=center_threshold, maxRadius=self._max_radius)
        return self.__remove_empty_circles(circles)


    def _binary_search(self, gray_image, amount):
        left, center_threshold, right = 1, 250, 500
        circles = self._get_circles(gray_image, center_threshold)

        while ((circles is None) or (len(circles) != amount)) and abs(left - right) > 1:
            if (circles is None) or (len(circles) < amount):
                right = center_threshold
            elif len(circles) > amount:
                left = center_threshold

            center_threshold = (left + right) / 2
            circles = self._get_circles(gray_image, center_threshold)

        return circles


    def get(self, amount=1):
        gray_image = cv2.cvtColor(self._source_image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.blur(gray_image, (11, 11))

        circles = self._binary_search(gray_image, amount)

        if (circles is not None) and (len(circles) != amount):
            return None

        return circles


class ColorCircleDetector(CircleDetector):
    def __init__(self, image, circle_color):
        super().__init__(image)
        self._circle_color = circle_color

    def get(self, amount=1):
        pass
