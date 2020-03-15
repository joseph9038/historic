from binascii import unhexlify
import json
import os

from sqlalchemy import create_engine, sql

import shapely

from flask import Flask, request, render_template, redirect

from flask_sqlalchemy import SQLAlchemy

from geoalchemy2.types import Geography

POSTGRES_USER = os.environ.get('POSTGRES_USER', 'sambrannan')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'superstrongpassword')
POSTGRES_HOSTNAME = os.environ.get('POSTGRES_HOSTNAME', 'localhost')
POSTGRES_DBNAME = os.environ.get('POSTGRES_DBNAME', 'historic')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', 5432)

DB_CONNECTION_STRING = f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DBNAME}'

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECTION_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

db = SQLAlchemy(app)
db.init_app(app)


class Landmark(db.Model):
    __tablename__ = 'landmarks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    coordinates = db.Column(Geography('POINT', srid=4326))
    _coordinate_description_string = None

    def __repr__(self):
        return f"<{self.name} @ {self.latitude},{self.longitude}>"

    @classmethod
    def init(cls, id, name, coordinates):
        landmark = cls(name=name)
        setattr(landmark, 'id', id)
        setattr(landmark, '_coordinate_description_string', coordinates)
        return landmark

    @property
    def point(self):
        if self._coordinate_description_string:
            desc = self._coordinate_description_string
        else:
            desc = self.coordinates.desc
        binary_data = unhexlify(desc)
        return shapely.wkb.loads(binary_data)

    @property
    def latitude(self):
        return self.point.y

    @property
    def longitude(self):
        return self.point.x


def landmarks_by_proximity(latitude, longitude):
    landmarks = []
    statement = """
        SELECT name, id, coordinates
        FROM landmarks
        CROSS JOIN (
            SELECT ST_Point(%(longitude)s,%(latitude)s)::geography AS ref_geog
        ) AS r
        WHERE ST_DWithin(coordinates, ref_geog, %(distance)s)
        ORDER BY ST_Distance(coordinates, ref_geog)
        LIMIT %(limit)s;
    """
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'distance': 10000,
        'limit': 10
    }
    engine = create_engine(DB_CONNECTION_STRING)
    with engine.connect() as cn:
        records = cn.execute(statement, **params).fetchall()
        for record in records:
            landmarks.append(Landmark.init(record[1], record[0], record[2]))
    return landmarks


def _generate_feature(landmark):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [landmark.longitude, landmark.latitude]
        },
        "properties": {
            "name": landmark.name
        }
    }

def get_geojson(landmarks):
    features = [f for f in map(_generate_feature, landmarks)]
    return {
        "type": "FeatureCollection",
        "features": features
    }


@app.route('/')
def index():
    landmarks = []
    latitude = request.args.get('latitude', None)
    longitude = request.args.get('longitude', None)
    if latitude and longitude:
        landmarks = landmarks_by_proximity(latitude, longitude)
    
    return render_template('index.html', **{'landmarks': landmarks})


@app.route('/map')
def mapper():
    return render_template('map.html', **{'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY})


@app.route('/landmarks')
def landmarks():
    landmarks = Landmark.query.all()
    return render_template('landmarks.html', **{'landmarks': landmarks})


@app.route('/api/landmarks')
def api_landmarks():
    landmarks = []
    latitude = request.args.get('latitude', None)
    longitude = request.args.get('longitude', None)
    if latitude and longitude:
        landmarks = landmarks_by_proximity(latitude, longitude)

    return json.dumps(get_geojson(landmarks))


@app.route('/ar')
def ar():
    return render_template('ar.html')


db.create_all()

if __name__ == '__main__':
    # latitude = 37.797583811500004
    # longitude = -122.40659186274999

    # landmarks = []
    # statement = """
    #     SELECT name, id, coordinates
    #     FROM landmarks
    #     CROSS JOIN (
    #         SELECT ST_Point(%(longitude)s,%(latitude)s)::geography AS ref_geog
    #     ) AS r
    #     WHERE ST_DWithin(coordinates, ref_geog, %(distance)s)
    #     ORDER BY ST_Distance(coordinates, ref_geog)
    #     LIMIT %(limit)s;
    # """
    # params = {
    #     'latitude': latitude,
    #     'longitude': longitude,
    #     'distance': 10000,
    #     'limit': 10
    # }
    # engine = create_engine(DB_CONNECTION_STRING)
    # with engine.connect() as cn:
    #     records = cn.execute(statement, **params).fetchall()
    #     for record in records:
    #         landmarks.append(Landmark.init(record[1], record[0], record[2]))
    # import pdb; pdb.set_trace()
    # print(landmarks)
    app.run(host='0.0.0.0', port=9090)