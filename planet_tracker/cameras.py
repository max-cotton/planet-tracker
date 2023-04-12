import os
import picamera

class PiCamera(picamera.PiCamera):
    def __init__(self, imagesPath):
        super().__init__()
        self.IMAGES_PATH = imagesPath

    def take_picture(self, pictureTime, picturedPlanet):
        # Create directory for image
        if not os.path.exists(self.IMAGES_PATH + f"{picturedPlanet}/"):
            os.makedirs(self.IMAGES_PATH + f"{picturedPlanet}/")
        # Create image name from time of capture
        replacedChars = " .:"
        for char in replacedChars:
            pictureTime = str(pictureTime).replace(char, "-")
        # Take Image
        self.capture(f'{self.IMAGES_PATH + f"{picturedPlanet}/"}{pictureTime}.jpg')
        print(f'\nPhoto taken and stored in {self.IMAGES_PATH + f"{picturedPlanet}/"}\n')