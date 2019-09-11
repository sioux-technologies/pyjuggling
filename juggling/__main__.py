import cv2
import logging

from juggling.circle import Circle
from juggling.circle_detector import CircleDetector
from juggling.matcher import Matcher


class CircleStorage:
    def __init__(self):
        self.__circles = None
        self.__ignore_change = None

    def get(self):
        return self.__circles

    def update(self, next_positions):
        if self.__circles is None:
            self.__circles = [Circle(position) for position in next_positions]
            self.__ignore_change = [0] * len(next_positions)

        else:
            if len(next_positions) != len(self.__circles):
                logging.warning("Amount of location is not equal to amount of circles.")
                return

            for i in range(len(self.__circles)):
                distance, next_position = Matcher(self.__circles[i].position()).match(next_positions)
                next_positions.remove(next_position)

                change_threshold = self.__circles[i].average_change() * 5.0
                if self.__ignore_change[i] > 2 or (distance < change_threshold and distance != 0):
                    self.__circles[i].update(next_position, distance)
                    self.__ignore_change[i] = 0
                else:
                    self.__ignore_change[i] += 1


class Application(object):
    def __init__(self):
        self.__storage = CircleStorage()

    def __display_circle(self, frame, circle, name):
        cv2.circle(frame, (circle.x(), circle.y()), circle.radius(), (0, 255, 0), 2)

        trajectory = circle.trajectory()
        for position in trajectory:
            cv2.circle(frame, (position[0], position[1]), 5, (255, 0, 0), -1)

        cv2.putText(frame, name, (circle.x(), circle.y()), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), lineType=2)
        cv2.putText(frame, str(circle.average_change()), (circle.x() + 20, circle.y()), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), lineType=2)


    def run(self, amount_circles=2):
        camera = cv2.VideoCapture(0)

        while True:
            ret, frame = camera.read()
            circle_positions = CircleDetector(frame).get(amount_circles)

            if circle_positions is not None:
                self.__storage.update(circle_positions)

                circles = self.__storage.get()
                for i in range(len(circles)):
                    self.__display_circle(frame, circles[i], str(i))
            else:
                logging.warning("Circles are not detected.")

            cv2.imshow('Juggling', frame)

            key_signal = cv2.waitKey(17)
            if key_signal == 27:  # Esc key to stop
                break

        cv2.destroyAllWindows()


test = Application()
test.run()
