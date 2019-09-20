"""
Module consists of classes for motion tracking: up-to-down and circle motions.
"""

import abc
import collections
import enum


class MotionTracker(metaclass=abc.ABCMeta):
    """
    Interface for motion trackers.
    """

    @abc.abstractmethod
    def track(self, position):
        """
        Notifies tracker about position changes.

        :param position: New position of an object.
        """
        ...

    @abc.abstractmethod
    def get_count(self):
        """
        :return: Amount of movement that are defined by specific motion tracker.
        """
        ...


class UpDownMotionTracker(MotionTracker):
    """
    Counts up down motions - so-called tossing, up-to-down juggling. This class calculates how many times
    an object is tossed during juggling.
    """

    class Direction(enum.IntEnum):
        """
        Enumerates possible directions of an object.
        """
        Unknown = 0
        Up = 1
        Down = 2

    __trajectory_size = 5
    __motion_size = 2
    __peek_threshold = 40
    __accept_change_direction = 1
    __pattern = [Direction.Up, Direction.Down]

    def __init__(self):
        """
        Initialize motion tracker.
        """
        self.__direction = UpDownMotionTracker.Direction.Unknown
        self.__differences = collections.deque()
        self.__previous = None
        self.__current = None
        self.__motions = collections.deque()
        self.__peeks = collections.deque()
        self.__laps = 0

    def track(self, position):
        """
        Notifies tracker about position changes of an object. Tracker updates statistics related to counting motions.

        :param position: New position of an object.
        """
        self.__previous = self.__current
        self.__current = position[1]

        if (self.__current is None) or (self.__previous is None):
            return

        self.__differences.appendleft(self.__current - self.__previous)
        if len(self.__differences) > self.__trajectory_size:
            self.__differences.pop()

        new_direction = self.__get_direction()
        if new_direction != self.__direction:
            self.__direction_changed(new_direction)

    def get_count(self):
        """
        :return: Total amount of tossing of an object.
        """
        return self.__laps

    def __direction_changed(self, new_direction):
        """
        :param new_direction: New direction defined by enumerator Direction.
        """
        self.__motions.append(new_direction)
        self.__peeks.append(self.__current)
        if len(self.__motions) > self.__motion_size:
            self.__motions.popleft()
            self.__peeks.popleft()

        self.__direction = new_direction

        if self.__is_trusted_motion():
            self.__laps += 1

    def __is_trusted_motion(self):
        """
        Checks whether an object follows the pattern of tossing.

        :return: If an object moves like in case of tossing, then it returns True, otherwise False.
        """
        if list(self.__motions) != self.__pattern:
            return False

        distance = abs(self.__peeks[-1] - self.__peeks[-2])
        return distance > self.__peek_threshold

    def __get_direction(self):
        """
        Calculates current object movement: up or down.

        :return: Current direction of an object.
        :type: Direction
        """
        if len(self.__differences) <= self.__accept_change_direction:
            return UpDownMotionTracker.Direction.Unknown

        count = 0
        direction = UpDownMotionTracker.Direction.Unknown
        for difference in self.__differences:
            if direction == UpDownMotionTracker.Direction.Unknown:
                if difference > 0:
                    direction = UpDownMotionTracker.Direction.Down
                else:
                    direction = UpDownMotionTracker.Direction.Up

            elif direction == UpDownMotionTracker.Direction.Down:
                if difference > 0:
                    count += 1
                else:
                    return self.__direction

            elif direction == UpDownMotionTracker.Direction.Up:
                if difference < 0:
                    count += 1
                else:
                    return self.__direction

            if count > self.__accept_change_direction:
                return direction

        return self.__direction


class LapMotionTracker(MotionTracker):
    """
    Counts circle motions of an object.
    """

    def __init__(self, image_height, image_width):
        """
        Initializes circle motion tracker.

        :param image_height: Height of an image.
        :param image_width: Width of an image.
        """
        self.__visited_regions = collections.deque()
        self.__image_height = image_height
        self.__image_width = image_width

        self.__map_id = [[1, 2], [0, 3]]
        self.__laps = 0

    def track(self, position):
        """
        Notifies tracker about position changes of an object. Tracker updates statistics related to counting motions.

        :param position: New position of an object.
        """
        location = self.__get_block_id(position[0], position[1])
        if (len(self.__visited_regions) > 0) and (location == self.__visited_regions[-1]):
            return

        self.__visited_regions.append(location)
        if len(self.__visited_regions) > 4:
            self.__visited_regions.popleft()

        self.__check_lap()

    def get_count(self):
        """
        :return: Amount of complete circle-motions in both directions for tracked object.
        """
        return self.__laps

    def __check_lap(self):
        """
        Checks for circle motion and if it is then updates statistic.
        """
        if len(self.__visited_regions) != 4:
            return

        if list(self.__visited_regions) == [0, 1, 2, 3]:
            self.__laps += 1
        elif list(self.__visited_regions) == [3, 2, 1, 0]:
            self.__laps += 1

    def __get_block_id(self, x, y):
        """
        :param x: Object's coordinate on X-axis.
        :param y: Object's coordinate on Y-axis.
        :return: ID of a block that corresponds to specified coordinates.
        """
        row = 0
        if y > self.__image_width / 2:
            row = 1

        col = 0
        if x > self.__image_height / 2:
            col = 1

        return self.__map_id[row][col]
