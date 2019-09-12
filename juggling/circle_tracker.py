import logging

from juggling.circle import Circle
from juggling.matcher import Matcher


class CircleTracker:
    def __init__(self):
        self.__circles = None
        self.__ignore_change = None


    def get(self):
        return self.__circles


    def update(self, next_positions):
        if self.__circles is None:
            self.__circles = [Circle(position) for position in next_positions]
            self.__ignore_change = [0] * len(next_positions)

        else:
            if len(next_positions) != len(self.__circles):
                logging.warning("Amount of location is not equal to amount of circles.")
            else:
                self.__match_circles(next_positions)


    def __match_circles(self, next_positions):
        for i in range(len(self.__circles)):
            distance, next_position = Matcher(self.__circles[i].position()).match(next_positions)
            next_positions.remove(next_position)

            predict_next_change = self.__circles[i].predict_distance()
            if predict_next_change is not None:
                predict_next_change *= 2

            if (self.__ignore_change[i] > 2) or (predict_next_change is None) or (distance < predict_next_change):
                self.__circles[i].update(next_position, distance)
                self.__ignore_change[i] = 0
            else:
                self.__ignore_change[i] += 1
