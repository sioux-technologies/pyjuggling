import re

from juggling.singletone import Singleton


class Configuration(metaclass=Singleton):
    def __init__(self):
        self.__amount = 1

        # aggressive - [[(0, 180, 110), (10, 255, 255)], [(170, 180, 110), (180, 255, 255)]]
        # middle - [[(0, 180, 100), (10, 255, 255)], [(170, 180, 100), (180, 255, 255)]]
        # relax - [[(0, 170, 100), (10, 255, 255)], [(170, 170, 100), (180, 255, 255)]]
        self.__color_ranges = [[(0, 180, 105), (10, 255, 255)], [(170, 180, 105), (180, 255, 255)]]
        self.__simulate = False
        self.__play_file = None
        self.__output_file = None
        self.__delay = 1

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
        self.__play_file = file

    def get_play_file(self):
        return self.__play_file

    def set_output_file(self, file):
        self.__output_file = file

    def get_output_file(self):
        return self.__output_file

    def set_delay(self, delay):
        self.__delay = delay

    def get_delay(self):
        return self.__delay

    def set_resolution(self, resolution):
        pattern = re.compile("(\d+)x(\d+)")
        result = pattern.match(resolution)
        if result is None:
            raise ValueError("Impossible to obtain camera resolution, resolution pattern is [width]x[height], "
                             "for example, 1280x720.")
        else:
            self.__width = int(result.group(1))
            self.__height = int(result.group(2))

    def get_resolution(self):
        return self.__width, self.__height
