import requests

class PlanetAPI():
    def __init__(self, latitude, longitude, elevation):
        self.LATITUDE = latitude
        self.LONGITUDE = longitude
        self.ELEVATION = elevation
        self.URL = "https://api.visibleplanets.dev/v3?latitude=32&=-98"

    def fetch_data(self, currentTime):
        params = {'latitude':self.LATITUDE, 
                  'longitude':self.LONGITUDE,
                  'elevation':self.ELEVATION,
                  'time':currentTime,}
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