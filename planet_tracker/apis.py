import requests

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