import requests
import unittest
from planet_tracker.apis import PlanetAPI

class TestApis(unittest.TestCase):
    def test_planet_api_url(self):
        planetApi = PlanetAPI(None,None,None)
        request = requests.get(planetApi.URL)
        self.assertEqual(request.status_code, 200)

if __name__ == '__main__':
    unittest.main()