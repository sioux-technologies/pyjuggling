import numpy
import unittest

from juggling.telemetry import Telemerty


class TestTelemetry(unittest.TestCase):
    def test_calculation(self):
        telemetry = Telemerty()

        t = [1, 2, 3, 4]
        s = [1, 4, 9, 16, 25]
        ds = numpy.diff(s)

        for i in range(3):
            telemetry.update(ds[i], t[i])

        self.assertEqual(7, telemetry.get_speed())
        self.assertEqual(2, telemetry.get_acceleration())

        telemetry.update(ds[-1], t[-1])
        self.assertEqual(9, telemetry.get_speed())
        self.assertEqual(2, telemetry.get_acceleration())
