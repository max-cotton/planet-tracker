# Pimoroni PanTiltHAT planet tracker
## Track planets above the horizon

## Run
Run with 'python3 planet_tracker'

## Configuration
Add the following configurations to a config.json file, in the root directory of the project:

| Configuration   | Value                                                                    |
| --------------- | ------------------------------------------------------------------------ |
| latitude        | Latitude of PanTiltHAT                                                   |
| longitude       | Longitude of PanTiltHAT                                                  |
| timeZone        | Timezone from python library pytz                                        |
| predictTracking | True or False to track the planet at 10 minutes for every 5 seconds      |
| takePictures    | True or False to take a picture with the attached camera every 5 seconds | 
| imagesPath      | Full path to the location to store pictures taken                        |

## Dev Setup
- Create a virtualenv with 'python3 -m venv {venv name}'
- Use 'source ./virtualenv/bin/activate' to enter venv
- Use pip as normal in the venv
- Use 'python3 setup.py develop' to setup preferences of setup.py (install package to venv in developing mode)
### Tests
- Use 'python3 -m unittest discover planet_tracker/test/' to run tests

## TODO
- Telescope
- 3D printer