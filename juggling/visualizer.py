import cv2
import enum

from juggling.metric import euclidean


class Style(enum.IntEnum):
    Circle = 0,
    Square = 1


class Visualizer:
    _colors = [[51, 204, 255], [102, 255, 51], [255, 153, 255], [255, 255, 0]]

    @staticmethod
    def visualize(frame, circles, tracker, style=Style.Circle):
        Visualizer.show_circles(frame, circles, style)
        Visualizer.show_motion_tracking(frame, tracker)

    @staticmethod
    def _show_circle_as_circle(frame, circle, name, color):
        cv2.circle(frame, (circle.get_x(), circle.get_y()), circle.get_radius(), (0, 255, 0), 2)

        trajectory = circle.get_trajectory()
        for position in trajectory:
            cv2.circle(frame, (position[0], position[1]), 5, color, -1)

        x = circle.get_x()
        y = circle.get_y()
        v = "v: %.1f" % euclidean(circle.get_x_telemetry().get_speed(), circle.get_y_telemetry().get_speed())

        cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), lineType=2)
        cv2.putText(frame, v, (x + 20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), lineType=2)

    @staticmethod
    def _show_circle_as_square(frame, circle, name, color):
        x, y, r, m = circle.get_x(), circle.get_y(), circle.get_radius(), 1
        cv2.rectangle(frame, (x - r * m, y - r * m), (x + r * m, y + r * m), (0, 255, 0), 2)

        trajectory = circle.get_trajectory()
        for position in trajectory:
            cv2.circle(frame, (position[0], position[1]), 3, (0, 255, 0), -1)

        # prev_x, prev_y = None, None
        # for position in trajectory:
        #     if (prev_x is not None) or (prev_y is not None):
        #         cv2.line(frame, (prev_x, prev_y), (position[0], position[1]), (0, 255, 0), 1)
        #
        #     cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)
        #     prev_x, prev_y = position[0], position[1]

        descr = "#%s" % name
        cv2.putText(frame, descr, (x - r * m, y - r * m - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), lineType=2)

    @staticmethod
    def _show_circle(frame, circle, name, color, style=Style.Circle):
        if style == Style.Circle:
            Visualizer._show_circle_as_circle(frame, circle, name, color)
        elif style == Style.Square:
            Visualizer._show_circle_as_square(frame, circle, name, color)
        else:
            raise NotImplemented("'%s' style is not supported." % style)

    @staticmethod
    def _get_color(index):
        color_index = index % len(Visualizer._colors)
        return Visualizer._colors[color_index]

    @staticmethod
    def show_circles(frame, circles, style=Style.Circle):
        for i in range(len(circles)):
            if circles[i].is_visible():
                color = Visualizer._get_color(i)
                Visualizer._show_circle(frame, circles[i], str(i), color, style)

    @staticmethod
    def show_motion_tracking(frame, tracker):
        if tracker is None:
            return

        total_amount = 0
        for i in range(len(tracker)):
            total_amount += tracker.get_complete_motions(i)
            info = "Laps for #%d: %d" % (i, tracker.get_complete_motions(i))
            cv2.putText(frame, info, (0, (i + 3) * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0),
                        thickness=2, lineType=2)

        info = "Total tossing amount: %d" % total_amount
        cv2.putText(frame, info, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0),
                    thickness=2, lineType=2)

    @staticmethod
    def show_pattern(frame, locations):
        for pattern in zip(*locations[::-1]):
            cv2.rectangle(frame, pattern, (pattern[0] + 50, pattern[1] + 50), (0, 255, 0), 1)
