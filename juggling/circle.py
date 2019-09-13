import collections

from juggling.telemetry import Telemerty


class Circle:
    __trajectory_length = 10

    def __init__(self, position, color):
        self.__position = position
        self.__color = color
        self.__telemetry = Telemerty()

        self.__trajectory = collections.deque()
        self.__trajectory.append((self.get_x(), self.get_y()))

    def get_x(self):
        return self.__position[0]

    def get_y(self):
        return self.__position[1]

    def get_radius(self):
        return self.__position[2]

    def get_position(self):
        return self.__position

    def get_color(self):
        return self.__color

    def get_trajectory(self):
        return self.__trajectory

    def get_telemetry(self):
        return self.__telemetry

    def update(self, position, distance_change, color):
        self.__position = position
        self.__trajectory.append((self.get_x(), self.get_y()))

        if len(self.__trajectory) > self.__trajectory_length:
            self.__trajectory.popleft()

        self.__color = color
        self.__telemetry.update(distance_change)
