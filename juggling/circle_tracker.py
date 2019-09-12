import logging

from juggling.circle import Circle
from juggling.matcher import Matcher
from juggling.region_tracker import RegionTracker


class CircleTracker:
    def __init__(self, image_height, image_width):
        self.__circles = None
        self.__region = None
        self.__ignore_change = None

        self.__height = image_height
        self.__width = image_width


    def get_circles(self):
        return self.__circles


    def get_circle_laps(self, index):
        return self.__region[index].get_laps()


    def update(self, next_positions):
        if self.__circles is None:
            self.__circles = [Circle(position) for position in next_positions]
            self.__region = [RegionTracker(self.__height, self.__width) for _ in next_positions]
            self.__ignore_change = [0] * len(next_positions)

        else:
            if len(next_positions) != len(self.__circles):
                logging.warning("Amount of location is not equal to amount of circles.")
            else:
                self.__match_circles(next_positions)


    def __match_circles(self, next_positions):
        for i in range(len(self.__circles)):
            distance, next_position = Matcher(self.__circles[i].position()).match(next_positions, [1, 1, 0])
            next_positions.remove(next_position)

            # position is predictable
            predict_next_change = self.__circles[i].predict_distance()
            if predict_next_change is not None:
                predict_next_change = predict_next_change * 0.3 + predict_next_change
                if predict_next_change < 100:
                    predict_next_change = 100

            position_verdict = (predict_next_change is None) or (distance < predict_next_change)

            # TODO: color change?

            # radius is the same with tolerance
            radius = self.__circles[i].position()[2]
            radius_verdict = (radius * 0.2 + radius) > next_position[2]
            print(radius, next_position[2])

            # general verdict
            general_verdict = position_verdict or radius_verdict

            if (self.__ignore_change[i] > 6) or general_verdict:
                # print("Recognized (position: %s, radius: %s)" % (position_verdict, radius_verdict))
                self.__circles[i].update(next_position, distance)
                self.__region[i].track(next_position)
                self.__ignore_change[i] = 0
            else:
                # print("Ignore (position: %s, radius: %s)" % (position_verdict, radius_verdict))
                self.__ignore_change[i] += 1
