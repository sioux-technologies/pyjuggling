import cv2

from juggling.configuration import Configuration
from juggling.circle_detector import ColorCircleDetector
from juggling.tracker import Tracker
from juggling.visualizer import Visualizer, Style
from juggling.simulator import Simulator


class Application(object):
    _exit_key = 27      # Escape

    def __init__(self):
        self.__camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        self.__simulator = Simulator([[100, 100, 10], [100, 100, 10], [100, 100, 10]],
                                     [[250, 300, 120], [250, 250, 120], [300, 260, 140]],
                                     [0.0, 2.54, 5.0], 3)

        frame = self.__read_camera()

        self.__tracker = Tracker(frame.shape[1], frame.shape[0])

    def __read_camera(self):
        _, frame = self.__camera.read()

        if Configuration().get_simulation_state():
            self.__simulator.step(frame)
        return frame

    def start(self):
        skip_counter = 0

        while True:
            frame = self.__read_camera()

            if self.__tracker.get_circles() is None:
                maximum_amount = Configuration().get_amount()
            else:
                maximum_amount = 100

            positions = ColorCircleDetector(frame, Configuration().get_color_ranges()).\
                get(Configuration().get_amount(), maximum_amount)

            if positions is not None:
                self.__tracker.update(positions)
                circles = self.__tracker.get_circles()
                Visualizer.visualize(frame, circles, self.__tracker, Style.Square)
                skip_counter = 0
            else:
                circles = self.__tracker.get_circles()
                if (circles is not None) and (skip_counter < 3):
                    Visualizer.visualize(frame, circles, self.__tracker, Style.Square)

                skip_counter += 1

            cv2.imshow('Juggling', frame)
            key_signal = cv2.waitKey(1)

            if key_signal == Application._exit_key:  # Esc key to stop
                break

        self.__camera.release()
        cv2.destroyAllWindows()
