import collections
import numpy
import time


class Circle:
    def __init__(self, position, trajectory_length=20):
        self.__position = position
        self.__trajectory_length = 20

        self.__trajectory = collections.deque()
        self.__dh = collections.deque()
        self.__time = collections.deque()

        self.__speed = -1
        self.__acceleration = -1

        self.update(position, 0)

    def x(self):
        return int(self.__position[0])

    def y(self):
        return int(self.__position[1])

    def radius(self):
        return int(self.__position[2])

    def position(self):
        return self.__position

    def speed(self):
        return self.__speed

    def acceleration(self):
        return self.__acceleration

    def trajectory(self):
        return self.__trajectory

    def average_change(self):
        return sum(self.__dh) / len(self.__dh)

    def predict_distance(self):
        if (self.__speed == -1) or (self.__acceleration == -1):
            return None

        avg_t = numpy.sum(numpy.diff(self.__time)) / len(self.__time)
        distance = self.__speed * avg_t + 0.5 * self.__acceleration * pow(avg_t, 2)
        return distance

    def update(self, position, distance_change):
        self.__position = position

        self.__trajectory.append((self.x(), self.y()))
        self.__dh.append(distance_change)
        self.__time.append(int(time.time() * 1000))
        if len(self.__trajectory) > self.__trajectory_length:
            self.__trajectory.popleft()
            self.__dh.popleft()
            self.__time.popleft()

        self.__calculate_telemetry()

    def __calculate_telemetry(self):
        if len(self.__dh) < 3:
            return

        dt = numpy.diff(self.__time)

        v = numpy.array(self.__dh)[1:] / dt
        dv = numpy.abs(numpy.diff(v))

        a = dv / dt[1:]

        self.__speed = v[-1]
        self.__acceleration = a[-1]
