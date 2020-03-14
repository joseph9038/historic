import json

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from app import Landmark


app = Flask(__name__)
# for locally running scripts and ipython shell
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sambrannan:superstrongpassword@localhost:5432/historic'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)
db.init_app(app)


def run():
    with open('./fixtures/sf_landmarks_points.geojson', 'r') as f:
        data = json.load(f)
    for feature in data['features']:
        name = feature['properties']['name']
        longitude = feature['geometry']['coordinates'][0]
        latitude = feature['geometry']['coordinates'][1]
        landmark = Landmark(name=name, coordinates='POINT({} {})'.format(longitude, latitude))
        db.session.add(landmark)
        
    db.session.commit()



if __name__ == '__main__':
    run()