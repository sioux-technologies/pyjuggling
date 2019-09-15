import cv2
import logging
import numpy

from juggling.tracker import Tracker
from juggling.circle_detector import CircleDetector
from juggling.pattern_searcher import PatternSearcher
from juggling.visualizer import Visualizer

from juggling.simulator import Simulator


class Application(object):
    def __init__(self):
        self.__tracker = None
        self.__pattern_searcher = None
        self.__simulator = Simulator([[100, 100, 30], [100, 100, 30], [100, 100, 30]], [[250, 300, 120], [250, 250, 120], [300, 260, 140]],
                                     [0.0, 2.54, 5.0])  # for 3 balls


    def run(self, amount_circles=2):
        camera = cv2.VideoCapture(0)

        ret, frame = camera.read()
        self.__tracker = Tracker(frame)

        while True:
            ret, frame = camera.read()
            original = frame.copy()

            circle_positions = CircleDetector(frame).get(amount_circles)

            if self.__pattern_searcher is None:
                if circle_positions is not None:
                    self.__tracker.update(circle_positions)
                    circles = self.__tracker.get_circles()
                    Visualizer.visualize(frame, circles, self.__tracker)
                else:
                    logging.warning("Circles are not detected.")

            else:
                patterns = self.__pattern_searcher.search(frame, 0.7)
                Visualizer.show_pattern(frame, patterns)

            cv2.imshow('Juggling', frame)
            key_signal = cv2.waitKey(5)

            if key_signal == 27:  # Esc key to stop
                break

            elif key_signal == 48:
                if circle_positions is None:
                    logging.warning("No circles is detected to learn.")
                    continue

                r = cv2.selectROI(frame)
                image_pattern = original[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

                cv2.imshow("Pattern to learn", image_pattern)

                self.__pattern_searcher = PatternSearcher(image_pattern)

            elif key_signal == 57:
                self.__pattern_searcher = None

        cv2.destroyAllWindows()


test = Application()
test.run(1)
