from environmental_data import app

import os
from flask_googlemaps import GoogleMaps

GoogleMaps(app)
basedir = os.path.abspath(os.path.dirname(__file__))


if __name__ == '__main__':
    app.run(port=5001, host='0.0.0.0')