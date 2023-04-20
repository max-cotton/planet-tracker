import datetime
import json
import logging
import sys
import time
import pytz
from cameras import PiCamera
from servos import PanTiltServos
from apis import PlanetAPI

class PlanetTracker():
    def __init__(self):
        self.configData = self.load_Config()
        self.planetAPI = PlanetAPI(latitude=self.configData['latitude'], longitude=self.configData['longitude'], elevation=self.configData['elevation'])
        self.panTiltServos = PanTiltServos()
        self.piCamera = None
        self.trackedPlanet = None

    def setup_config(self, configData):
        # Setup base configuration
        configurations = ['latitude','longitude','elevation','timeZone','predictTracking','takePictures','imagesPath']
        for configuration in configurations:
            if configuration not in configData.keys():
                configData[configuration] = ''
                
        # Check configurations
        try:
            if int(configData['latitude']) < -90 or int(configData['latitude']) > 90:
                raise ValueError("Latitude not within -90 to 90 degrees")
        except ValueError as ve:
            logging.error("Invalid latitude configuration")
            logging.error(str(ve))
            sys.exit()
        try:
            if int(configData['longitude']) < -180 or int(configData['longitude']) > 180:
                raise ValueError("Longitude not within -180 to 180 degrees")
        except ValueError as ve:
            logging.error("Invalid longitude configuration")
            logging.error(str(ve))
            sys.exit()
        try:
            if int(configData['elevation']) < 0:
                raise ValueError("Elevation not greater than 0 meters")
        except ValueError as ve:
            logging.error("Invalid elevation configuration")
            logging.error(str(ve))
            sys.exit()
        try:
            if configData['timeZone'] not in pytz.all_timezones:
                raise ValueError("Time zone not in possible arguements")
        except ValueError as ve:
            logging.error("Invalid time zone configuration")
            logging.error(str(ve))
            sys.exit()
        if configData['takePictures'] == 'True':
            if not configData['imagesPath']:
                logging.error("Take Pictures mode is selected, but no path to store the images is configured")
                sys.exit()
            try:
                if int(configData['pictureDelayTime']) < 0:
                    raise ValueError("Time delay between taking pictures not greater than 0 seconds")
            except ValueError as ve:
                logging.error("Invalid pictureDelayTime configuration")
                logging.error(str(ve))
                sys.exit()
        return configData

    def load_Config(self):
        try:
            configFile = open('config.json')
            configData = json.load(configFile)
            configFile.close()
        except Exception as e:
            logging.error("Failed to load config.json")
            logging.error(str(e))
            sys.exit()
        return self.setup_config(configData)

    def track_planet(self):
        currentTime = datetime.datetime.now(pytz.timezone(self.configData['timeZone']))
        planets = self.planetAPI.fetch_data(currentTime=currentTime)
        apiFetchtime = time.time()

        # Setup predicted path
        predictPath = True if self.configData['predictTracking'] == "True" else False 
        trackingTimeIncrease = datetime.timedelta(minutes=10)

        # Setup take pictures
        takePictures = True if self.configData['takePictures'] == "True" else False
        if takePictures:
            self.piCamera = PiCamera(imagesPath=self.configData['imagesPath'])
            pictureTakenTime = time.time()
            pictureDelayTime = int(self.configData['pictureDelayTime'])

        trackingMode = f"Predicting path with time increase of {trackingTimeIncrease}" if predictPath else "Normal tracking"
        print(f"Tracking : {self.trackedPlanet}\nMode : {trackingMode}\n")
        tracking = True
        while tracking:
            self.panTiltServos.tilt(planets[self.trackedPlanet]['altitude'])
            self.panTiltServos.pan(-(180 - planets[self.trackedPlanet]['azimuth']))
            # Update planet data every 5 seconds
            if time.time() >= (apiFetchtime + 5):
                if predictPath:
                    currentTime += trackingTimeIncrease
                else:
                    currentTime = datetime.datetime.now(pytz.timezone(self.configData['timeZone']))
                planets = self.planetAPI.fetch_data(currentTime=currentTime)
                apiFetchtime = time.time()
                if self.trackedPlanet not in planets.keys():
                    print("Planet is now below horizon")
                    tracking = False
                else:
                    print(f"Time: {currentTime}\n{planets[self.trackedPlanet]}\n")
                    if takePictures and time.time() >= (pictureTakenTime + pictureDelayTime):
                        self.piCamera.take_picture(pictureTime=currentTime, picturedPlanet=self.trackedPlanet)
                        pictureTakenTime = time.time()

    def get_tracked_planet(self):
        currentTime = datetime.datetime.now(pytz.timezone(self.configData['timeZone']))  # ISO format = YYYY-MM-DD HH:MM:SS.mmmmmm
        planets = self.planetAPI.fetch_data(currentTime=currentTime)
        print(f"\nTime: {currentTime}\n")
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