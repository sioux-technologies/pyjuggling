import logging

from juggling.circle import Circle
from juggling.color_extractor import ColorExtractor
from juggling.metric import euclidean
from juggling.motion_tracker import LapMotionTracker


class Tracker:
    def __init__(self, image):
        self.__circles = None
        self.__region = None
        self.__ignore_change = None

        self.__image = image
        self.__height = image.shape[1]
        self.__width = image.shape[0]

        self.__max_x = self.__width
        self.__max_y = self.__height
        self.__max_color = [255, 255, 255]
        self.__max_radius = min(self.__height, self.__width) / 2


    def get_circles(self):
        return self.__circles


    def get_circle_laps(self, index):
        return self.__region[index].get_count()


    def update(self, next_positions):
        if self.__circles is None:
            self.__circles = [Circle(next_positions[i], ColorExtractor(self.__image, next_positions[i]).extract())
                              for i in range(len(next_positions))]

            self.__region = [LapMotionTracker(self.__height, self.__width) for _ in next_positions]
            self.__ignore_change = [0] * len(next_positions)

        else:
            if len(next_positions) != len(self.__circles):
                logging.warning("Amount of location is not equal to amount of circles.")
            else:
                self.__match_circles(next_positions)


    def __normilize_features(self, positions, colors):
        result = []
        for i in range(len(positions)):
            result.append(self.__normilize_feature(positions[i], colors[i]))

        return result


    def __normilize_feature(self, position, color):
        return [position[0] / self.__width,                          # x
                position[1] / self.__height,                         # y
                position[2] / min(self.__height, self.__width),      # radius
                color[0] / 255,  # R
                color[1] / 255,  # G
                color[2] / 255]  # B


    def __update_state(self, index_circle, position, color):
        current_circle = self.__circles[index_circle]

        distance = euclidean(current_circle.get_position()[0:2], position[0:2])
        self.__circles[index_circle].update(position, distance, color)
        self.__region[index_circle].track(position)


    def __match_circles(self, next_positions):
        next_colors = [ColorExtractor(self.__image, position).extract() for position in next_positions]
        extracted_patterns = self.__normilize_features(next_positions, next_colors)

        circle_dissimilarity = []

        for i in range(len(self.__circles)):
            current_circle = self.__circles[i]
            current_pattern = self.__normilize_feature(current_circle.get_position(), current_circle.get_color())

            for index_pattern in range(len(extracted_patterns)):
                distance = euclidean(current_pattern, extracted_patterns[index_pattern])
                circle_dissimilarity.append((i, index_pattern, distance))

        circle_dissimilarity.sort(key=lambda descriptor: descriptor[2])

        assigned_patterns = set()
        for item in circle_dissimilarity:
            index_circle = item[0]
            index_pattern = item[1]

            if index_pattern in assigned_patterns:
                continue

            assigned_patterns.add(index_pattern)
            self.__update_state(index_circle, next_positions[index_pattern], next_colors[index_pattern])

        assert len(assigned_patterns) == len(self.__circles)
