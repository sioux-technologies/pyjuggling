import abc
import collections


class RegionTracker(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def track(self, position):
        ...

    @abc.abstractmethod
    def get_count(self):
        ...


class UpDownRegionTracker(RegionTracker):
    def __init__(self):
        raise NotImplemented("To be implemented.")

    def track(self, position):
        raise NotImplemented("To be implemented.")

    def get_count(self):
        raise NotImplemented("To be implemented.")


class LapRegionTracker(RegionTracker):
    def __init__(self, image_height, image_width):
        self.__visited_regions = collections.deque()
        self.__image_height = image_height
        self.__image_width = image_width

        self.__map_id = [[1, 2], [0, 3]]
        self.__laps = 0

    def track(self, position):
        id = self.__get_block_id(position[0], position[1])
        if (len(self.__visited_regions) > 0) and (id == self.__visited_regions[-1]):
            return

        self.__visited_regions.append(id)
        if len(self.__visited_regions) > 4:
            self.__visited_regions.popleft()

        self.__check_lap()

    def get_count(self):
        return self.__laps

    def __check_lap(self):
        if len(self.__visited_regions) != 4:
            return

        if list(self.__visited_regions) == [0, 1, 2, 3]:
            self.__laps += 1
        elif list(self.__visited_regions) == [3, 2, 1, 0]:
            self.__laps += 1

    def __get_block_id(self, x, y):
        row = 0
        if y > self.__image_width / 2:
            row = 1

        col = 0
        if x > self.__image_height / 2:
            col = 1

        return self.__map_id[row][col]
