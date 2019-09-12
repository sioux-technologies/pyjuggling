import cv2
import math


class Simulator:
    def __init__(self, circles, trajectory, initial_angle):
        self.__circles = circles
        self.__trajectory = trajectory

        self.__radians = initial_angle


    def step(self, frame):
        for i in range(len(self.__circles)):
            x = int(self.__trajectory[i][2] * math.sin(self.__radians[i]) * 1.5) + self.__trajectory[i][0]
            y = int(self.__trajectory[i][2] * math.cos(self.__radians[i])) + self.__trajectory[i][1]

            cv2.circle(frame, (x, y), self.__circles[i][2], (255, 255, 255), -1)
            cv2.circle(frame, (x, y), self.__circles[i][2], (0, 0, 255), 4)

            self.__radians[i] -= 0.1
