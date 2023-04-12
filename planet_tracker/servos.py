import time
import pantilthat

class PanTiltServos():  # NOTE: Currently the servos take left and down as positive, so is currently adjusted to that in these methods
    def __init__(self):
        self.X_LIM = 90
        self.Y_LIM = 90

    def pan(self, x):
        if x > self.X_LIM:
            x = self.X_LIM
        elif x < -self.X_LIM:
            x = -self.X_LIM
        pantilthat.pan(-x)
        time.sleep(0.005)

    def tilt(self, y):
        if y > self.Y_LIM:
            y = self.Y_LIM
        elif y < -self.Y_LIM:
            y = -self.Y_LIM
        pantilthat.tilt(-y)
        time.sleep(0.005)

    def reset(self):
        print("Resetting Servos")
        startTime = time.time()
        resetting = True
        while resetting:
            if time.time() >= startTime + 2:
                resetting = False
            self.pan(0)
            self.tilt(0)
            time.sleep(0.005)
        print("Servos Reset")