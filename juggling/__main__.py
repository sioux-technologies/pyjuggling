import cv2
import logging

from juggling.circle import Circle
from juggling.circle_detector import CircleDetector
from juggling.matcher import Matcher


class CircleStorage:
    def __init__(self):
        self.__circles = None

    def __getitem__(self, item):
        return self.__circles[item]

    def update(self, next_positions):
        if self.__circles is None:
            self.__circles = [Circle(position) for position in next_positions]

        else:
            for circle in self.__circles:
                next_position = Matcher(circle.position()).match(next_positions)
                circle.update(next_position)


class Application(object):
    def __init__(self):
        self.__storage = CircleStorage()

    def __display_circle(self, frame, circle):
        cv2.circle(frame, (circle.x(), circle.y()), circle.radius(), (0, 255, 0), 2)
        cv2.circle(frame, (circle.x(), circle.y()), 2, (0, 0, 255), 3)

        trajectory = circle.trajectory()
        for position in trajectory:
            cv2.circle(frame, (position[0], position[1]), 5, (255, 0, 0), 5)


    def run(self, amount_circles=2):
        camera = cv2.VideoCapture(0)

        while True:
            ret, frame = camera.read()
            circle_positions = CircleDetector(frame).get(amount_circles)

            if circle_positions is not None:
                self.__storage.update(circle_positions)

                for circle in self.__storage:
                    self.__display_circle(frame, circle)
            else:
                logging.warning("Circles are not detected.")

            cv2.imshow('Juggling', frame)

            key_signal = cv2.waitKey(17)
            if key_signal == 27:  # Esc key to stop
                break

        cv2.destroyAllWindows()


test = Application()
test.run()
