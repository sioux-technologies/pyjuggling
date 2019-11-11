import cv2
import os

from juggling.color_extractor import ColorExtractor
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
        self.__output_stream = self.__create_output_stream()

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

    def __del__(self):
        self.__video_stream.release()
        if self.__output_stream is not None:
            self.__output_stream.release()

        cv2.destroyAllWindows()

    def __create_output_stream(self):
        output_file = Configuration().get_output_file()
        stream = None
        if output_file is not None:
            width, height = Configuration().get_resolution()
            stream = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, (width, height))
        return stream

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

    def __relax_color(self, ranges, s, v):
        color_range_relaxed = []
        for pair in ranges:
            relaxed_pair = []
            for color in pair:
                relaxed = list(color)
                relaxed[1] -= s
                relaxed[2] -= v
                relaxed_pair.append(tuple(relaxed))

            color_range_relaxed.append(tuple(relaxed_pair))
        return color_range_relaxed

    def __filter_regions(self, image, rectangles, ranges):
        filtered_regions = []
        for rectangle in rectangles:
            if ColorExtractor(image, rectangle).contains(ranges) is True:
                filtered_regions.append(rectangle)
        return filtered_regions

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

            movement_frame, rectangles = self.__movement_detector.crop(frame)
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
                    # ranges = self.__relax_color(Configuration().get_color_ranges(), 20, 5)
                    # filtered_rectangles = self.__filter_regions(frame, rectangles, ranges)
                    if len(rectangles) >= Configuration().get_amount():
                        self.__tracker.predict(rectangles)

                circles = self.__tracker.get_circles()
                if (circles is not None) and (skip_counter < 20):
                    Visualizer.visualize(frame, circles, self.__tracker, Style.Square)

                skip_counter += 1

            cv2.imshow('Juggling', frame)
            if self.__output_stream is not None:
                self.__output_stream.write(frame)
            key_signal = cv2.waitKey(Configuration().get_delay())

            if key_signal == Application._exit_key:  # Esc key to stop
                break
