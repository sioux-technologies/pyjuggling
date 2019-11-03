import collections

from juggling.telemetry import Telemetry


class Circle:
    """
    Stores information that describes circle in 2-dimensional space.
    """
    __trajectory_length = 15
    __radius_values_length = 10

    def __init__(self, position, color):
        self.__position = position
        self.__color = color
        self.__x_telemetry = Telemetry()
        self.__y_telemetry = Telemetry()
        self.__visible = False

        self.__trajectory = collections.deque()
        self.__radius_values = collections.deque()
        self.__radius = position[2]

        self.__trajectory.append((self.get_x(), self.get_y()))
        self.__radius_values.append(self.get_radius())

    def __str__(self):
        return str(self.__position)

    def __repr__(self):
        return str(self)

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

    def get_x_telemetry(self):
        return self.__x_telemetry

    def get_y_telemetry(self):
        return self.__y_telemetry

    def get_velocity(self):
        return pow(pow(self.__x_telemetry.get_velocity(), 2.0) + pow(self.__y_telemetry.get_velocity(), 2.0), 0.5)

    def is_visible(self):
        """
        :return: True if a circle is visible (observable).
        """
        return self.__visible

    def invisible(self):
        """
        Mark circle as invisible that means that circle is not observable.
        """
        self.__visible = False

    def update(self, position):
        """
        Updates circle in line with position on an image. When update method is called then circle visibility property
        becomes True.

        :param position: New circle's coordinates (x, y, radius).
        """

        x_position = int(position[0] * 0.8 + self.__x_telemetry.predict_position() * 0.2)
        y_position = int(position[1] * 0.8 + self.__y_telemetry.predict_position() * 0.2)

        self.__position = [x_position, y_position]

        self.__trajectory.append((x_position, y_position))
        self.__radius_values.append(position[2])

        if len(self.__trajectory) > self.__trajectory_length:
            self.__trajectory.popleft()

        if len(self.__radius_values) > self.__radius_values_length:
            self.__radius_values.popleft()

        self.__radius = int(sum(self.__radius_values) / len(self.__radius_values))
        self.__x_telemetry.update(x_position)
        self.__y_telemetry.update(y_position)
        self.__visible = True
