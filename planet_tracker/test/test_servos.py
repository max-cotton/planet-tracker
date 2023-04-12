import unittest
from servos import Servos

class TestServos(unittest.TestCase):
    def test_servo_limits(self):
        servos = Servos()
        self.assertEqual(servos.X_LIM, 90, "Servos X Limit should be 90")
        self.assertEqual(servos.Y_LIM, 90, "Servos Y Limit should be 90")

if __name__ == "__main__":
    unittest.main()