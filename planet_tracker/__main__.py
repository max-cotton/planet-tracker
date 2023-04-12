import datetime
import json
import pytz
import time
from cameras import PiCamera
from servos import PanTiltServos
from apis import PlanetAPI

class PlanetTracker():
    def __init__(self):
        self.configData = self.load_Config()
        self.planetAPI = PlanetAPI(latitude=self.configData['latitude'], longitude=self.configData['longitude'])
        self.panTiltServos = PanTiltServos()
        self.piCamera = None
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
            self.piCamera = PiCamera(imagesPath=self.configData['imagesPath'])

        trackingMode = f"Predicting path with time increase of {timeIncrease}" if predictPath else "Normal tracking"
        print(f"Tracking : {self.trackedPlanet}\nMode : {trackingMode}\n")
        tracking = True
        while tracking:
            self.panTiltServos.tilt(planets[self.trackedPlanet]['altitude'])
            self.panTiltServos.pan(-(180 - planets[self.trackedPlanet]['azimuth']))
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
                        self.piCamera.take_picture(pictureTime=inputTime, picturedPlanet=self.trackedPlanet)
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
        self.panTiltServos.reset()
        print("\nPanTiltHAT script for tracking planets above horizon\nMake sure that the PanTiltHat is aimed South")
        self.get_tracked_planet()
        self.track_planet()

if __name__ == "__main__":
    planetTracker = PlanetTracker()
    planetTracker.main()