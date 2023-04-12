import datetime
import json
import os
import pantilthat
import picamera
import pytz
import requests 
import time

class Camera(picamera.PiCamera):
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

class Servos():  # NOTE: Currently the servos take left and down as positive, so is currently adjusted to that in these methods
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

class PlanetAPI():
    def __init__(self, latitude, longitude):
        self.LATITUDE = latitude
        self.LONGITUDE = longitude
        self.URL = "https://api.visibleplanets.dev/v3?latitude=32&=-98"

    def fetch_data(self, inputTime):
        params = {'latitude':self.LATITUDE, 
                  'longitude':self.LONGITUDE, 
                  'time':inputTime,}
        data = requests.get(self.URL, params).json()
        planets = {}
        for planet in data['data']:
            planets[planet['name']] = {'altitude':planet['altitude'],        # Altitude = Veritcal angle above horizon
                                       'azimuth':planet['azimuth'],          # Azimuth = Horizontal angle around the horizon, from true north
                                       'nakedEye':planet['nakedEyeObject'],}
        return planets
    
    def read_data(self, planets):
        print("These are the planets above the horizon at your latitude and longitude!\n")
        for key in planets.keys():
            print(f"{key} : {planets[key]}")
        print("\n")

class PlanetTracker():
    def __init__(self):
        self.configData = self.load_Config()
        self.planetAPI = PlanetAPI(latitude=self.configData['latitude'], longitude=self.configData['longitude'])
        self.servos = Servos()
        self.camera = None
        self.trackedPlanet = None

    def load_Config(self):
        configFile = open('config.json')
        configData = json.load(configFile)
        configFile.close()
        return configData

    def track_planet(self):
        inputTime = datetime.datetime.now(pytz.timezone(self.configData['timeZone']))
        planets = self.planetAPI.fetch_data(inputTime=inputTime)
        updateTime = time.time()

        # Setup predicted path
        predictPath = True if self.configData['predictTracking'] == "True" else False 
        timeIncrease = datetime.timedelta(minutes=10)

        # Setup take pictures
        takePictures = True if self.configData['takePictures'] == "True" else False
        if takePictures:
            self.camera = Camera(imagesPath=self.configData['imagesPath'])

        trackingMode = f"Predicting path with time increase of {timeIncrease}" if predictPath else "Normal tracking"
        print(f"Tracking : {self.trackedPlanet}\nMode : {trackingMode}\n")
        tracking = True
        while tracking:
            self.servos.tilt(planets[self.trackedPlanet]['altitude'])
            self.servos.pan(-(180 - planets[self.trackedPlanet]['azimuth']))
            if time.time() >= (updateTime + 5):  # Update planet data every 5 seconds
                if predictPath:
                    inputTime += timeIncrease
                else:
                    inputTime = datetime.datetime.now(pytz.timezone(self.configData['timeZone']))
                planets = self.planetAPI.fetch_data(inputTime=inputTime)
                updateTime = time.time()
                try:
                    print(f"Time: {inputTime}\n{planets[self.trackedPlanet]}\n")
                    if takePictures:
                        self.camera.take_picture(pictureTime=inputTime, picturedPlanet=self.trackedPlanet)
                except Exception as e:
                    print(e)
                    tracking = False

    def get_tracked_planet(self):
        inputTime = datetime.datetime.now(pytz.timezone(self.configData['timeZone']))  # ISO format = YYYY-MM-DD HH:MM:SS.mmmmmm
        planets = self.planetAPI.fetch_data(inputTime=inputTime)
        print(f"\nTime: {inputTime}\n")
        self.planetAPI.read_data(planets)
        while self.trackedPlanet not in planets.keys():
            self.trackedPlanet = input("Enter the name of one of the planets above to track: ")
        print("\n")

    def main(self):
        self.servos.reset()
        print("\nPanTiltHAT script for tracking planets above horizon\nMake sure that the PanTiltHat is aimed South")
        self.get_tracked_planet()
        self.track_planet()

if __name__ == "__main__":
    planetTracker = PlanetTracker()
    planetTracker.main()