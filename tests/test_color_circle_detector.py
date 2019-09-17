import cv2
import unittest

from juggling.circle_detector import ColorCircleDetector


class TestColorCircleDetector(unittest.TestCase):
    def template_amount(self, image_path, amount):
        image = cv2.imread(image_path)
        circles = ColorCircleDetector(image).get(amount)

        self.assertIsNotNone(circles)
        self.assertEqual(amount, len(circles))

    def test_photo_amount_1_reddish_1(self):
        self.template_amount("samples/photo_reddish_ball_01.jpg", 1)

    def test_photo_amount_1_reddish_2(self):
        self.template_amount("samples/photo_reddish_ball_02.jpg", 1)

    def test_photo_amount_1_reddish_3(self):
        self.template_amount("samples/photo_reddish_ball_03.jpg", 1)

    def test_photo_amount_2_reddish_1(self):
        self.template_amount("samples/photo_reddish_ball_04.jpg", 2)
