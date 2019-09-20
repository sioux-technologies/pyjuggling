import cv2

from juggling.configuration import Configuration
from juggling.circle_detector import ColorCircleDetector
from juggling.tracker import Tracker
from juggling.visualizer import Visualizer, Style


class Application(object):
    _exit_key = 27      # Escape

    def __init__(self):
        self.__camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        _, frame = self.__camera.read()

        self.__tracker = Tracker(frame.shape[1], frame.shape[0])

    def start(self):
        while True:
            _, frame = self.__camera.read()

            positions = ColorCircleDetector(frame, Configuration().get_color_ranges()).get(Configuration().get_amount())

            if positions is not None:
                self.__tracker.update(positions)
                circles = self.__tracker.get_circles()
                Visualizer.visualize(frame, circles, self.__tracker, Style.Square)
            else:
                Visualizer.show_motion_tracking(frame, self.__tracker)

            cv2.imshow('Juggling', frame)
            key_signal = cv2.waitKey(1)

            if key_signal == Application._exit_key:  # Esc key to stop
                break

        self.__camera.release()
        cv2.destroyAllWindows()
