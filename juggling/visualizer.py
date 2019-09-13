import cv2


class Visualizer:
    @staticmethod
    def visualize(frame, circles, tracker):
        Visualizer.show_circles(frame, circles)
        Visualizer.show_motion_tracking(frame, tracker)

    @staticmethod
    def show_circle(frame, circle, name):
        cv2.circle(frame, (circle.get_x(), circle.get_y()), circle.get_radius(), (0, 255, 0), 2)

        trajectory = circle.get_trajectory()
        for position in trajectory:
            cv2.circle(frame, (position[0], position[1]), 5, (255, 0, 0), -1)

        x = circle.get_x()
        y = circle.get_y()
        v = "v: %.1f" % circle.get_telemetry().get_speed()
        a = "a: %.1f" % circle.get_telemetry().get_acceleration()

        cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), lineType=2)
        cv2.putText(frame, v, (x + 20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), lineType=2)
        cv2.putText(frame, a, (x + 20, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), lineType=2)

    @staticmethod
    def show_circles(frame, circles):
        for i in range(len(circles)):
            Visualizer.show_circle(frame, circles[i], str(i))

    @staticmethod
    def show_motion_tracking(frame, tracker):
        for i in range(len(tracker)):
            info = "Laps for #%d: %d" % (i, tracker.get_complete_motions(i))
            cv2.putText(frame, info, (0, (i + 1) * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), lineType=2)
