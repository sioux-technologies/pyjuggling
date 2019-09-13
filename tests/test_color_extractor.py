import cv2
import unittest

from juggling.circle_detector import CircleDetector
from juggling.color_extractor import ColorExtractor


class TestColorExtractor(unittest.TestCase):
    def template_color(self, image_path, amount, expected_color, tolerance):
        image = cv2.imread(image_path)
        circles = CircleDetector(image).get(amount)

        for i in range(len(circles)):
            color = ColorExtractor(image, circles[i]).extract()

            self.assertAlmostEqual(color[0], expected_color[0], delta=tolerance[0])
            self.assertAlmostEqual(color[1], expected_color[1], delta=tolerance[1])
            self.assertAlmostEqual(color[2], expected_color[2], delta=tolerance[2])

    def test_simple_colored_amount_3(self):
        self.template_color("samples/circles_simple_red_amount_3.png", 3, (36, 28, 237), (10, 10, 5))

    def test_simple_colored_amount_3_noise(self):
        self.template_color("samples/circles_simple_red_amount_3_noise.png", 3, (36, 28, 237), (20, 20, 5))
