import enum
import logging

from juggling.circle import Circle
from juggling.color_extractor import ColorExtractor
from juggling.metric import euclidean
from juggling.motion_tracker import UpDownMotionTracker


class FeatureType(enum.IntEnum):
    Common = 0,
    SameColor = 1


class Tracker:
    def __init__(self, image, ftype=FeatureType.Common):
        self.__circles = None
        self.__region = None
        self.__ignore_change = None

        self._ftype = ftype

        self.__image = image
        self.__height = image.shape[1]
        self.__width = image.shape[0]

        self.__max_x = self.__width
        self.__max_y = self.__height
        self.__max_color = [255, 255, 255]
        self.__max_radius = min(self.__height, self.__width) / 2

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
            self.__circles = [Circle(next_positions[i], ColorExtractor(self.__image, next_positions[i]).extract())
                              for i in range(len(next_positions))]

            self.__region = [UpDownMotionTracker() for position in next_positions]
            self.__ignore_change = [0] * len(next_positions)

        else:
            if len(next_positions) != len(self.__circles):
                logging.warning("Amount of location is not equal to amount of circles.")
            else:
                self.__match_circles(next_positions)

    def __normalize_features(self, positions, colors):
        result = []
        for i in range(len(positions)):
            result.append(self.__normalize_feature(positions[i], colors[i]))

        return result

    def __normalize_feature(self, position, color):
        if self._ftype == FeatureType.Common:
            return self.__normalize_common_feature(position, color)
        elif self._ftype == FeatureType.SameColor:
            return self.__normilize_same_color_feature(position)
        else:
            raise NotImplemented("'%s' feature type is not supported." % self._ftype)

    def __normalize_common_feature(self, position, color):
        return [position[0] / self.__width,                          # x
                position[1] / self.__height,                         # y
                position[2] / min(self.__height, self.__width),      # radius
                color[0] / 255,  # R
                color[1] / 255,  # G
                color[2] / 255]  # B

    def __normilize_same_color_feature(self, position):
        return [position[0] / self.__width,                          # x
                position[1] / self.__height]                         # y

    def __update_state(self, index_circle, position, color):
        current_circle = self.__circles[index_circle]

        x_distance = abs(current_circle.get_position()[0] - position[0])
        y_distance = abs(current_circle.get_position()[1] - position[1])

        self.__circles[index_circle].update(position, x_distance, y_distance, color)
        self.__region[index_circle].track(position)

    def __check_point_in_area(self, pos_prev, pos, dx, dy, m, r):
        if dx is None or dy is None:
            return True

        if dx * m < r:
            dx = r
        if dy * m < r:
            dy = r

        x_prev, y_prev, x, y = pos_prev[0], pos_prev[1], pos[0], pos[1]
        if (abs(x_prev - x) < dx * m) and (abs(y_prev - y) < dy * m):
            return True
        return False

    def __mark_circles_invisible(self):
        for circle in self.__circles:
            circle.invisible()

    def __match_circles(self, next_positions):
        next_colors = [ColorExtractor(self.__image, position).extract() for position in next_positions]
        extracted_patterns = self.__normalize_features(next_positions, next_colors)

        circle_dissimilarity = []

        self.__mark_circles_invisible()
        for i in range(len(self.__circles)):
            current_circle = self.__circles[i]
            current_pattern = self.__normalize_feature(current_circle.get_position(), current_circle.get_color())

            for index_pattern in range(len(extracted_patterns)):
                distance = euclidean(current_pattern, extracted_patterns[index_pattern])
                circle_dissimilarity.append((i, index_pattern, distance))

        circle_dissimilarity.sort(key=lambda descriptor: descriptor[2])

        assigned_patterns = set()
        updated_circles = set()
        for item in circle_dissimilarity:
            index_circle = item[0]
            index_pattern = item[1]

            if (index_pattern in assigned_patterns) or (index_circle in updated_circles):
                continue

            # make sure that it is possible in line telemetry
            if not self.__check_point_in_area(self.__circles[index_circle].get_position(),
                                              next_positions[index_pattern],
                                              self.__circles[index_circle].get_x_telemetry().predict_distance_change(),
                                              self.__circles[index_circle].get_y_telemetry().predict_distance_change(),
                                              1,
                                              self.__circles[index_circle].get_radius()):
                continue

            assigned_patterns.add(index_pattern)
            updated_circles.add(index_circle)

            self.__update_state(index_circle, next_positions[index_pattern], next_colors[index_pattern])

        #print(updated_circles)
