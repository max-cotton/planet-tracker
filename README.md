# Pimoroni PanTiltHAT planet tracker
## About
Track planets above the horizon with a PanTiltHat

## Run
Run with 'python3 planet_tracker'

## Configuration
Add the following configurations to a config.json file, in the root directory of the project:

| Configuration    | Value                                                                    |
| ---------------- | ------------------------------------------------------------------------ |
| latitude         | Latitude of PanTiltHAT                                                   |
| longitude        | Longitude of PanTiltHAT                                                  |
| elevation        | Elevation of PanTiltHAT above sea level in meters                        |
| timeZone         | Timezone from python library pytz                                        |
| predictTracking  | True or False to track the planet at 10 minutes for every 5 seconds      |
| takePictures     | True or False to take a picture with the attached camera every 5 seconds | 
| imagesPath       | Full path to the location to store pictures taken                        |
| pictureDelayTime | Time delay between taking pictures in seconds                            |

## Dev Setup
- Create a virtualenv with 'python3 -m venv {venv name}'
- Use 'source ./virtualenv/bin/activate' to enter venv
- Use pip as normal in the venv
- Use 'python3 setup.py develop' to setup preferences of setup.py (install package to venv in developing mode)
### Tests
- Use 'python3 -m unittest discover planet_tracker/test/' to run tests
### Documentation
- PanTiltHAT: http://docs.pimoroni.com/pantilthat/
- Planet API: https://github.com/csymlstd/visible-planets-api

## TODO
- Add custom time between photos
- Telescope
- 3D printer