import cv2
import unittest

from juggling.circle_detector import CircleDetector


class TestCircleDetector(unittest.TestCase):
    def template_amount(self, image_path, amount):
        image = cv2.imread(image_path)
        circles = CircleDetector(image).get(amount)

        self.assertIsNotNone(circles)
        self.assertEqual(amount, len(circles))

    def test_simple_colored_amount_3(self):
        self.template_amount("samples/circles_simple_colored_amount_3.png", 3)

    def test_simple_colored_amount_3_noise(self):
        self.template_amount("samples/circles_simple_colored_amount_3_noise.png", 3)

    def test_simple_red_amount_3(self):
        self.template_amount("samples/circles_simple_red_amount_3.png", 3)

    def test_simple_red_amount_3_noise(self):
        self.template_amount("samples/circles_simple_red_amount_3_noise.png", 3)

    def test_simple_color_amount_5(self):
        self.template_amount("samples/circles_simple_colored_amount_5.png", 5)

    def test_photo_amount_3_white_background_1(self):
        self.template_amount("samples/circles_photo_amount_3_white_background_1.jpg", 3)

    def test_photo_amount_3_white_background_2(self):
        self.template_amount("samples/circles_photo_amount_3_white_background_2.jpg", 3)

