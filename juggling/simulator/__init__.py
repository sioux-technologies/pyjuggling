import cv2
import math


class Simulator:
    def __init__(self, circles, trajectory, initial_angle, appearance_step=1):
        self.__circles = circles
        self.__trajectory = trajectory

        self.__appearance_step = appearance_step
        self.__step = 0

        self.__radians = initial_angle


    def step(self, frame):
        for i in range(len(self.__circles)):
            if self.__step % self.__appearance_step == 0:
                x = int(self.__trajectory[i][2] * math.sin(self.__radians[i])) + self.__trajectory[i][0]
                y = int(self.__trajectory[i][2] * math.cos(self.__radians[i])) + self.__trajectory[i][1]

                cv2.circle(frame, (x, y), self.__circles[i][2], (66, 66, 255), -1)
                cv2.circle(frame, (x, y), self.__circles[i][2], (66, 66, 255), 4)

            self.__radians[i] -= 0.1

        self.__step += 1
