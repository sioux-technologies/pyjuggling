import collections


class Circle:
    def __init__(self, position, trajectory_length=20):
        self.__position = position
        self.__trajectory_length = 20

        self.__trajectory = collections.deque()
        self.__distance_change = collections.deque()
        self.update(position, 0)

    def x(self):
        return int(self.__position[0])

    def y(self):
        return int(self.__position[1])

    def radius(self):
        return int(self.__position[2])

    def position(self):
        return self.__position

    def trajectory(self):
        return self.__trajectory

    def average_change(self):
        return sum(self.__distance_change) / len(self.__distance_change)

    def update(self, position, distance_change):
        assert distance_change >= 0
        self.__position = position

        self.__trajectory.append((self.x(), self.y()))
        self.__distance_change.append(distance_change)
        if len(self.__trajectory) > self.__trajectory_length:
            self.__trajectory.popleft()
            self.__distance_change.popleft()