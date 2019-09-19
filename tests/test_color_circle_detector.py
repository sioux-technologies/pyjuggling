import cv2
import unittest

from juggling.circle_detector import ColorCircleDetector


class TestColorCircleDetector(unittest.TestCase):
    def template_amount(self, image_path, amount):
        image = cv2.imread(image_path)
        circles = ColorCircleDetector(image).get(amount)

        self.assertIsNotNone(circles)
        self.assertEqual(amount, len(circles))

    def test_simple_amount_3_reddish_1(self):
        self.template_amount("samples/circles_simple_red_amount_3_01.png", 3)

    def test_simple_amount_3_reddish_2(self):
        self.template_amount("samples/circles_simple_red_amount_3_02.png", 3)

    def test_photo_amount_1_reddish_1(self):
        self.template_amount("samples/photo_reddish_ball_01.jpg", 1)

    def test_photo_amount_1_reddish_2(self):
        self.template_amount("samples/photo_reddish_ball_02.jpg", 1)

    def test_photo_amount_1_reddish_3(self):
        self.template_amount("samples/photo_reddish_ball_03.jpg", 1)

    def test_photo_amount_2_reddish_1(self):
        self.template_amount("samples/photo_reddish_ball_04.jpg", 2)

    def test_photo_amount_2_reddish_2(self):
        self.template_amount("samples/photo_reddish_ball_05.jpg", 2)

    def test_photo_amount_2_reddish_3(self):
        self.template_amount("samples/photo_reddish_ball_06.jpg", 2)

    def test_photo_amount_2_reddish_4(self):
        self.template_amount("samples/photo_reddish_ball_07.jpg", 2)

    def test_photo_amount_3_reddish_1(self):
        self.template_amount("samples/photo_reddish_ball_08.jpg", 3)

    def test_photo_amount_3_reddish_2(self):
        self.template_amount("samples/photo_reddish_ball_09.jpg", 3)

    def test_photo_amount_3_reddish_3(self):
        self.template_amount("samples/photo_reddish_ball_10.jpg", 3)

    def test_photo_amount_2_reddish_5(self):
        self.template_amount("samples/photo_reddish_ball_11.jpg", 2)

    def test_photo_amount_2_reddish_6(self):
        self.template_amount("samples/photo_reddish_ball_12.jpg", 2)
