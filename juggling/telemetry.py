"""
Module provides telemetry services.

"""

import collections
import numpy
import time


class Telemetry:
    """
    Calculates object movement parameters like velocity, acceleration. Additionally the class provides service to
    predict further position of the object using velocity and acceleration.
    """
    _ds_len = 2     # at lest 2 ds is require to calculate v and a
    _t_len = 3      # three time points is required to calculate v and a

    def __init__(self):
        """
        Initializes telemetry instance.
        """
        self._ds = collections.deque()     # distance rate of change
        self._t = collections.deque()      # measured time points
        self._v = None                     # measured speed points
        self._a = -1                       # acceleration

    def __str__(self):
        """
        :return: String representation of a telemetry of an object.
        """
        if self._v is None:
            return "v: 'None', a: 'None'"
        return "v: '%.1f', a: '%.3f'" % (self._v[-1], self._a)

    def update(self, ds, t=None):
        """
        Calculates current state the object.

        :param ds: distance change (difference).
        :param t:  current time (can be ignored, in this case time point is set inside of the instance).
        """
        self._update_ds(ds)
        self._update_t(t)

        if len(self._t) == self._t_len:
            dt = numpy.diff(self._t)
            dv = self._update_v(dt)
            self._update_a(dv, dt)

    def get_speed(self):
        """
        :return: Velocity of an object that is tracked by this telemetry instance. It may return '0' if there is
                  no enough data (distance changes) - common situation at the begging.
        """
        if self._v is None:
            return 0
        return self._v[-1]

    def get_acceleration(self):
        """
        :return: Acceleration of an object that is tracked by this telemetry instance. If may return '0' if there is
                  no enough data (distance changes) - common situation at the begging.
        """
        return self._a

    def predict_distance_change(self):
        """
        Calculates distance that will done in line with current state: velocity and acceleration.

        :return: Predicted distance change in the next step of movement.
        """
        if self._v is None:
            return None

        t = numpy.sum(numpy.diff(self._t)) / len(self._t)
        distance = self._v[-1] * t + 0.5 * self._a * t * t
        return distance

    def _update_ds(self, ds):
        """
        Updates current distance difference.

        :param ds: New distance difference that has been passed by an object.
        """
        self._ds.append(ds)
        if len(self._ds) > self._ds_len:
            self._ds.popleft()

    def _update_t(self, t=None):
        """
        Updates time point for distance difference.

        :param t: New time point (can be omitted - will be calculated automatically).
        """
        cur_time = t or int(time.time() * 1000)
        self._t.append(cur_time)
        if len(self._t) > self._t_len:
            self._t.popleft()

    def _update_v(self, dt):
        """
        Update current velocity in line with passed distance and time change.

        :param dt: Time change between last update and current.
        :return Velocity for each measurement period.
        :type array_like
        """
        self._v = numpy.array(self._ds) / dt
        return numpy.abs(numpy.diff(self._v))  # direction does not matter

    def _update_a(self, dv, dt):
        """
        Update current acceleration in line with current state of an object.

        :param dv: Velocity change between last update and current.
        :param dt: Time change between last update and current.
        :return: Current acceleration.
        :type: float
        """
        self._a = dv[-1] / dt[-1]
