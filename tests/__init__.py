import cv2
import unittest

from juggling.circle_detector import CircleDetector


class TestCircleDetector(unittest.TestCase):
    def template_amount(self, image_path, amount):
        image = cv2.imread(image_path)
        circles = CircleDetector(image).get(amount)

        self.assertIsNotNone(circles)
        self.assertEqual(amount, len(circles))