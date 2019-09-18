import cv2
import numpy
import unittest

from juggling.circle import Circle
from juggling.tracker import Tracker


class TestTracker(unittest.TestCase):
    def test_two_circles_prediction(self):
        image_stub = cv2.imread("samples/circles_simple_red_amount_3.png")
        circle1 = Circle([50, 50, 10], None)
        circle2 = Circle([70, 50, 10], None)

        tracker = Tracker()
