from setuptools import setup, find_packages

setup(
    name='planet-tracker',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/Improbbl/planet-tracker',
    author='Max Cotton',
    author_email='maxcotton22@gmail.com',
    description='Track planets above the horizon with a PanTiltHAT',
    install_requires=[
            'pantilthat',
            'picamera',
            'pytz',
            'requests',
    ],
)