import unittest
from planet_tracker.servos import PanTiltServos

class TestServos(unittest.TestCase):
    def test_servo_limits(self):
        panTiltServos = PanTiltServos()
        self.assertEqual(panTiltServos.X_LIM, 90, "Servos X Limit should be 90")
        self.assertEqual(panTiltServos.Y_LIM, 90, "Servos Y Limit should be 90")

if __name__ == "__main__":
    unittest.main()