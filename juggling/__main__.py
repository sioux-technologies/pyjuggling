import cv2
import logging
import time

from juggling.circle_tracker import CircleTracker
from juggling.circle_detector import CircleDetector
from juggling.simulator import Simulator


class Application(object):
    def __init__(self):
        self.__tracker = None
        #self.__simulator = Simulator([[100, 100, 40], [100, 100, 50]], [[250, 300, 120], [250, 250, 120]], [0.0, 3.14])  # for 2 balls
        self.__simulator = Simulator([[100, 100, 30], [100, 100, 30], [100, 100, 30]], [[250, 300, 120], [250, 250, 120], [300, 260, 140]],
                                     [0.0, 2.54, 5.0])  # for 3 balls

    def __display_circle(self, frame, circle, name):
        cv2.circle(frame, (circle.x(), circle.y()), circle.radius(), (0, 255, 0), 2)

        trajectory = circle.trajectory()
        for position in trajectory:
            cv2.circle(frame, (position[0], position[1]), 5, (255, 0, 0), -1)

        avg_change = "avg. dh: %.1f" % circle.average_change()
        speed = "v: %.1f" % circle.speed()
        acceleration = "a: %.1f" % circle.acceleration()

        cv2.putText(frame, name, (circle.x(), circle.y()), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), lineType=2)
        cv2.putText(frame, avg_change, (circle.x() + 20, circle.y()), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), lineType=2)
        cv2.putText(frame, speed, (circle.x() + 20, circle.y() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), lineType=2)
        cv2.putText(frame, acceleration, (circle.x() + 20, circle.y() + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), lineType=2)


    def run(self, amount_circles=2):
        camera = cv2.VideoCapture(0)

        time.sleep(1)

        ret, frame = camera.read()
        self.__tracker = CircleTracker(frame.shape[1], frame.shape[0])

        while True:
            ret, frame = camera.read()
            #self.__simulator.step(frame)
            circle_positions = CircleDetector(frame).get(amount_circles)

            if circle_positions is not None:
                self.__tracker.update(circle_positions)

                circles = self.__tracker.get_circles()
                for i in range(len(circles)):
                    self.__display_circle(frame, circles[i], str(i))

                    info = "Laps for #%d: %d" % (i, self.__tracker.get_circle_laps(i))
                    cv2.putText(frame, info, (0, (i + 1) * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), lineType=2)
            else:
                logging.warning("Circles are not detected.")

            cv2.imshow('Juggling', frame)

            key_signal = cv2.waitKey(17)
            if key_signal == 27:  # Esc key to stop
                break

        cv2.destroyAllWindows()


test = Application()
test.run(2)
