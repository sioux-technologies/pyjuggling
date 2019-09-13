import cv2
import logging

from juggling.tracker import Tracker
from juggling.circle_detector import CircleDetector
from juggling.visualizer import Visualizer

from juggling.simulator import Simulator


class Application(object):
    def __init__(self):
        self.__tracker = None
        self.__simulator = Simulator([[100, 100, 30], [100, 100, 30], [100, 100, 30]], [[250, 300, 120], [250, 250, 120], [300, 260, 140]],
                                     [0.0, 2.54, 5.0])  # for 3 balls


    def run(self, amount_circles=2):
        camera = cv2.VideoCapture(0)

        ret, frame = camera.read()
        self.__tracker = Tracker(frame)

        while True:
            ret, frame = camera.read()

            circle_positions = CircleDetector(frame).get(amount_circles)

            if circle_positions is not None:
                self.__tracker.update(circle_positions)

                circles = self.__tracker.get_circles()
                Visualizer.visualize(frame, circles, self.__tracker)
            else:
                logging.warning("Circles are not detected.")

            cv2.imshow('Juggling', frame)

            key_signal = cv2.waitKey(17)
            if key_signal == 27:  # Esc key to stop
                break

        cv2.destroyAllWindows()


test = Application()
test.run(2)
