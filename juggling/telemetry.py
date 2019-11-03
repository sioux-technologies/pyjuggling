"""
Module provides telemetry services.

"""


class Telemetry:
    """
    Calculates object movement parameters like velocity, acceleration. Additionally the class provides service to
    predict further position of the object using velocity and acceleration.
    """

    def __init__(self):
        """
        Initializes telemetry instance.
        """

        self._pos_prev = 0
        self._pos_cur = 0
        self._velocity = 0

    def __str__(self):
        """
        :return: String representation of a telemetry of an object.
        """
        return "v: '%.1f'" % self._velocity

    def update(self, position):
        """
        Calculates current state the object.

        :param: position: distance change (difference).

        """
        self._pos_prev = self._pos_cur
        self._pos_cur = position

        self._velocity = self._pos_cur - self._pos_prev

    def get_velocity(self):
        """
        :return: Velocity of an object that is tracked by this telemetry instance. It may return '0' if there is
                  no enough data (distance changes) - common situation at the begging.
        """
        return self._velocity

    def predict_position(self):
        """
        Calculates next position of an object.

        :return: Predicted position of an object.
        """

        return self._pos_cur + self._velocity
