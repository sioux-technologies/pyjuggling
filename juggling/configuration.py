from juggling.singletone import Singleton


class Configuration(metaclass=Singleton):
    def __init__(self):
        self.__amount = 1
        self.__color_ranges = [[(0, 150, 120), (10, 255, 255)], [(170, 150, 120), (180, 255, 255)]]

    def set_amount(self, amount):
        self.__amount = amount

    def get_amount(self):
        return self.__amount

    def set_color_ranges(self, color_ranges):
        self.__color_ranges = color_ranges

    def get_color_ranges(self):
        return self.__color_ranges
