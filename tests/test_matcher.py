import cv2
import numpy
import unittest

from juggling.circle import Circle
from juggling.tracker import Matcher


class TestMatch(unittest.TestCase):
    def template_one_step(self, circles, next_positions, answers):
        matcher = Matcher(100, 100, circles)
        result = matcher.match(next_positions)

        result = sorted(result, key=lambda item: item.index_circle)

        self.assertEqual(result[0].next_position, next_positions[answers[0]])
        self.assertEqual(result[1].next_position, next_positions[answers[1]])

    def test_two_circles_01(self):
        circle1 = Circle([50, 50, 10], None)
        circle2 = Circle([70, 50, 10], None)
        next_positions = [[55, 51, 10], [72, 54, 11]]

        self.template_one_step([circle1, circle2], next_positions, [0, 1])

    def test_two_circles_02(self):
        circle1 = Circle([50, 50, 10], None)
        circle2 = Circle([70, 50, 10], None)
        next_positions = [[55, 51, 10], [72, 20, 11]]

        self.template_one_step([circle1, circle2], next_positions, [0, 1])

    def test_two_circles_03(self):
        circle1 = Circle([50, 50, 10], None)
        circle2 = Circle([70, 50, 10], None)
        next_positions = [[55, 61, 10], [72, 10, 11]]

        self.template_one_step([circle1, circle2], next_positions, [0, 1])

    def test_two_circle_exchange_01(self):
        circle1 = Circle([50, 50, 10], None)
        circle2 = Circle([70, 50, 10], None)
        next_positions = [[65, 61, 10], [72, 20, 11]]

        self.template_one_step([circle1, circle2], next_positions, [1, 0])
