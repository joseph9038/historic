from flask import Flask, request, render_template, redirect

from flask_sqlalchemy import SQLAlchemy

from geoalchemy2.types import Geography


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pypostgresql://sambrannan:superstrongpassword@postgresdb:5432/historic'

# for inside of docker container
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sambrannan:superstrongpassword@postgresdb:5432/historic'

# for locally running scripts and ipython shell
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sambrannan:superstrongpassword@localhost:5432/historic'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

db = SQLAlchemy(app)
db.init_app(app)


class Landmark(db.Model):
    __tablename__ = 'landmarks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    coordinates = db.Column(Geography('POINT', srid=4326))


@app.route('/')
def index():
    landmarks = Landmark.query.all()
    return render_template('index.html', **{'landmarks': landmarks})


db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)