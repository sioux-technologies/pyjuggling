import logging

from juggling.circle import Circle
from juggling.color_extractor import ColorExtractor
from juggling.matcher import Matcher
from juggling.metric import euclidean
from juggling.region_tracker import LapRegionTracker


class CircleTracker:
    def __init__(self, image):
        self.__circles = None
        self.__region = None
        self.__ignore_change = None

        self.__image = image
        self.__height = image.shape[1]
        self.__width = image.shape[0]


    def get_circles(self):
        return self.__circles


    def get_circle_laps(self, index):
        return self.__region[index].get_count()


    def update(self, next_positions):
        if self.__circles is None:
            self.__circles = [Circle(next_positions[i], ColorExtractor(self.__image, next_positions[i]).extract())
                              for i in range(len(next_positions))]

            self.__region = [LapRegionTracker(self.__height, self.__width) for _ in next_positions]
            self.__ignore_change = [0] * len(next_positions)

        else:
            if len(next_positions) != len(self.__circles):
                logging.warning("Amount of location is not equal to amount of circles.")
            else:
                self.__match_circles(next_positions)


    def __match_circles(self, next_positions):
        for i in range(len(self.__circles)):
            distance, next_position = Matcher(self.__circles[i].get_position()).match(next_positions, [1, 1, 0])
            next_positions.remove(next_position)

            # check whether position is predictable
            predict_next_change = self.__circles[i].get_telemetry().predict_distance_change()
            if predict_next_change is not None:
                predict_next_change = predict_next_change * 0.3 + predict_next_change
                if predict_next_change < 100:
                    predict_next_change = 100

            position_verdict = (predict_next_change is None) or (distance < predict_next_change)

            # check whether color is the same with tolerance
            color = ColorExtractor(self.__image, next_position).extract()
            color_difference = euclidean(color, self.__circles[i].get_color())
            #print("Color difference:", color_difference)

            # check whether radius is the same with tolerance
            radius = self.__circles[i].get_position()[2]
            radius_verdict = (radius * 0.2 + radius) > next_position[2]

            # general verdict
            general_verdict = position_verdict or radius_verdict

            if (self.__ignore_change[i] > 6) or general_verdict:
                # print("Recognized (position: %s, radius: %s)" % (position_verdict, radius_verdict))
                color = ColorExtractor(self.__image, next_position).extract()
                self.__circles[i].update(next_position, distance, color)
                self.__region[i].track(next_position)
                self.__ignore_change[i] = 0
            else:
                # print("Ignore (position: %s, radius: %s)" % (position_verdict, radius_verdict))
                self.__ignore_change[i] += 1
