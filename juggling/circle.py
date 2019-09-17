import collections

from juggling.telemetry import Telemetry


class Circle:
    __trajectory_length = 10
    __radius_values_length = 10

    def __init__(self, position, color):
        self.__position = position
        self.__color = color
        self.__telemetry = Telemetry()
        self.__visible = False

        self.__trajectory = collections.deque()
        self.__radius_values = collections.deque()
        self.__radius = position[2]

        self.__trajectory.append((self.get_x(), self.get_y()))
        self.__radius_values.append(self.get_radius())

    def get_x(self):
        return self.__position[0]

    def get_y(self):
        return self.__position[1]

    def get_radius(self):
        return self.__radius

    def get_position(self):
        return [self.get_x(), self.get_y(), self.get_radius()]

    def get_color(self):
        return self.__color

    def get_trajectory(self):
        return self.__trajectory

    def get_telemetry(self):
        return self.__telemetry

    def is_visible(self):
        return self.__visible

    def invisible(self):
        self.__visible = False

    def update(self, position, distance_change, color):
        self.__position = position
        self.__trajectory.append((position[0], position[1]))
        self.__radius_values.append(position[2])

        if len(self.__trajectory) > self.__trajectory_length:
            self.__trajectory.popleft()

        if len(self.__radius_values) > self.__radius_values_length:
            self.__radius_values.popleft()

        self.__radius = int(sum(self.__radius_values) / len(self.__radius_values))
        self.__color = color
        self.__telemetry.update(distance_change)
        self.__visible = True
