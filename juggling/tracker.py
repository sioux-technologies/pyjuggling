import enum
import logging

from juggling.circle import Circle
from juggling.matcher import Matcher
from juggling.motion_tracker import UpDownMotionTracker


class Tracker:
    __ignore_threshold = 1

    def __init__(self, image):
        self.__circles = None
        self.__region = None
        self.__ignore = None

        self.__image = image
        self.__height = image.shape[1]
        self.__width = image.shape[0]

    def __len__(self):
        if self.__region is None:
            return 0
        return len(self.__region)

    def get_circles(self):
        return self.__circles

    def get_complete_motions(self, index):
        return self.__region[index].get_count()

    def update(self, next_positions):
        if self.__circles is None:
            self.__circles = [Circle(next_positions[i], None) for i in range(len(next_positions))]
            self.__region = [UpDownMotionTracker() for _ in next_positions]
            self.__ignore = [0] * len(next_positions)

        else:
            if len(next_positions) != len(self.__circles):
                logging.warning("Amount of location is not equal to amount of circles.")
            else:
                self.__match_circles(next_positions)

    def __update_state(self, index_circle, position, color):
        current_circle = self.__circles[index_circle]

        x_distance = abs(current_circle.get_position()[0] - position[0])
        y_distance = abs(current_circle.get_position()[1] - position[1])

        self.__circles[index_circle].update(position, x_distance, y_distance, color)
        self.__region[index_circle].track(position)
        self.__ignore[index_circle] = 0

    def __mark_circles_invisible(self):
        for circle in self.__circles:
            circle.invisible()

    def __match_circles(self, next_positions):
        self.__mark_circles_invisible()
        results = Matcher(self.__height, self.__width, self.__circles).match(next_positions, None)
        # print("--------------------")
        # print("Circles:          %s" % str(self.__circles))
        # print("Matching results: %s" % results)
        for result in results:
            index_circle = result.index_circle
            if result.relible is True or self.__ignore[index_circle] > self.__ignore_threshold:
                self.__update_state(index_circle, result.next_position, None)
            else:
                self.__ignore[index_circle] += 1
