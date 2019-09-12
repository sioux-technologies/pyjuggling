import cv2
import logging

from juggling.circle_tracker import CircleTracker
from juggling.circle_detector import CircleDetector


class Application(object):
    def __init__(self):
        self.__tracker = None

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

        ret, frame = camera.read()
        self.__tracker = CircleTracker(frame.shape[1], frame.shape[0])

        while True:
            ret, frame = camera.read()
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
test.run(1)
