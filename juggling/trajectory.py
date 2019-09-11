import collections


class Trajectory:
    def __init__(self, max_size):
        self.__trajectory = collections.deque()
        self.__size = max_size

    def update(self, x, y):
        self.__trajectory.append((x, y))
        if len(self.__trajectory) > self.__size:
            self.__trajectory.popleft()

    def get(self):
        return self.__trajectory
