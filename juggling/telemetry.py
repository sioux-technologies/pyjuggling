import collections
import numpy
import time


class Telemetry:
    _ds_len = 2     # at lest 2 ds is require to calculate v and a
    _t_len = 3      # three time points is required to calculate v and a

    def __init__(self):
        self._ds = collections.deque()     # distance rate of change
        self._t = collections.deque()      # measured time points
        self._v = None                     # measured speed points
        self._a = -1                       # acceleration

    def __str__(self):
        if self._v is None:
            return "v: 'None', a: 'None'"
        return "v: '%.1f', a: '%.3f'" % (self._v[-1], self._a)

    def update(self, ds, t=None):
        self._update_ds(ds)
        self._update_t(t)

        if len(self._t) == self._t_len:
            dt = numpy.diff(self._t)
            dv = self._update_v(dt)
            self._update_a(dv, dt)

    def get_speed(self):
        if self._v is None:
            return 0
        return self._v[-1]

    def get_acceleration(self):
        return self._a

    def predict_distance_change(self):
        if self._v is None:
            return None

        t = numpy.sum(numpy.diff(self._t)) / len(self._t)
        distance = self._v[-1] * t + 0.5 * self._a * t * t
        return distance

    def _update_ds(self, ds):
        self._ds.append(ds)
        if len(self._ds) > self._ds_len:
            self._ds.popleft()

    def _update_t(self, t=None):
        cur_time = t or int(time.time() * 1000)
        self._t.append(cur_time)
        if len(self._t) > self._t_len:
            self._t.popleft()

    def _update_v(self, dt):
        self._v = numpy.array(self._ds) / dt
        return numpy.abs(numpy.diff(self._v))  # direction does not matter

    def _update_a(self, dv, dt):
        self._a = dv[-1] / dt[-1]
