import cv2
import os

from juggling.configuration import Configuration
from juggling.circle_detector import ColorCircleDetector
from juggling.movement_detector import MovementDetector
from juggling.tracker import Tracker
from juggling.visualizer import Visualizer, Style
from juggling.simulator import Simulator


class Application(object):
    _exit_key = 27      # Escape

    def __init__(self):
        self.__video_stream = self.__create_video_stream()

        self.__simulator = Simulator([[100, 100, 10], [100, 100, 10], [100, 100, 10]],
                                     [[250, 300, 120], [250, 250, 120], [300, 260, 140]],
                                     [0.0, 2.54, 5.0], 3)

        frame = self.__get_frame()
        if frame is None:
            print("No input video stream - nothing to process.")
            exit(-1)

        self.__movement_detector = MovementDetector()
        self.__movement_detector.crop(frame)

        self.__tracker = Tracker(frame.shape[1], frame.shape[0])

    def __create_video_stream(self):
        play_file = Configuration().get_play_file()
        if play_file is None:
            stream = cv2.VideoCapture(0, cv2.CAP_ANY)

            width, height = Configuration().get_resolution()
            stream.set(cv2.CAP_PROP_FRAME_WIDTH, int(width))
            stream.set(cv2.CAP_PROP_FRAME_HEIGHT, int(height))
            return stream
        else:
            if not os.path.exists(play_file):
                raise FileNotFoundError("File to play '%s' is not found." % play_file)
            return cv2.VideoCapture(play_file)

    def __get_frame(self):
        _, frame = self.__video_stream.read()

        if Configuration().get_simulation_state():
            self.__simulator.step(frame)
        return frame

    def start(self):
        skip_counter = 0

        while True:
            frame = self.__get_frame()
            if frame is None:
                print("No input video stream - nothing to process.")
                exit(-1)

            if self.__tracker.get_circles() is None:
                maximum_amount = Configuration().get_amount()
            else:
                # maximum_amount = 100  # try to pay attention to data like in clustering.
                maximum_amount = Configuration().get_amount()   # be direct

            movement_frame, centers = self.__movement_detector.crop(frame)
            positions = ColorCircleDetector(movement_frame, Configuration().get_color_ranges()).\
                get(Configuration().get_amount(), maximum_amount)

            if positions is not None:
                # for position in positions:
                #    cv2.circle(frame, (position[0], position[1]), position[2], [0, 0, 255], 3)

                self.__tracker.update(positions)
                circles = self.__tracker.get_circles()
                Visualizer.visualize(frame, circles, self.__tracker, Style.Square)
                skip_counter = 0
            else:
                if skip_counter < 10:
                    self.__tracker.predict(centers)

                circles = self.__tracker.get_circles()
                if (circles is not None) and (skip_counter < 20):
                    # for circle in circles:
                    #     pos = circle.get_position()
                    #     cv2.circle(frame, (pos[0], pos[1]), circle.get_radius(), [255, 0, 0], 3)
                    Visualizer.visualize(frame, circles, self.__tracker, Style.Square)

                skip_counter += 1

            cv2.imshow('Juggling', frame)
            key_signal = cv2.waitKey(100)

            if key_signal == Application._exit_key:  # Esc key to stop
                break

        self.__video_stream.release()
        cv2.destroyAllWindows()
