import re

from juggling.singletone import Singleton


class Configuration(metaclass=Singleton):
    def __init__(self):
        self.__amount = 1
        self.__color_ranges = [[(0, 180, 100), (15, 255, 255)], [(165, 180, 100), (180, 255, 255)]]
        self.__simulate = False
        self.__file = None

        self.__width = 1280
        self.__height = 720

    def set_amount(self, amount):
        self.__amount = amount

    def get_amount(self):
        return self.__amount

    def set_color_ranges(self, color_ranges):
        self.__color_ranges = color_ranges

    def get_color_ranges(self):
        return self.__color_ranges

    def set_simulation_state(self, state):
        self.__simulate = state

    def get_simulation_state(self):
        return self.__simulate

    def set_play_file(self, file):
        self.__file = file

    def get_play_file(self):
        return self.__file

    def set_resolution(self, resolution):
        pattern = re.compile("(\d+)x(\d+)")
        result = pattern.match(resolution)
        if result is None:
            raise ValueError("Impossible to obtain camera resolution, resolution pattern is [width]x[height], "
                             "for example, 1280x720.")
        else:
            self.__width = result.group(1)
            self.__height = result.group(2)

    def get_resolution(self):
        return self.__width, self.__height
