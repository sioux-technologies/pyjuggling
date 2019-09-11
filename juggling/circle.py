from juggling.trajectory import Trajectory


class Circle:
    def __init__(self, position):
        self.__position = position
        self.__trajectory = Trajectory(20)

    def x(self):
        return self.__position[0]

    def y(self):
        return self.__position[1]

    def radius(self):
        return self.__position[2]

    def position(self):
        return self.__position

    def trajectory(self):
        return self.__trajectory.get()

    def update(self, position):
        self.__position = position
        self.__trajectory.update(self.x(), self.y())
