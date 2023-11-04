from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, jsonify, request
from flask_bootstrap import Bootstrap5
from forms import AddCoffe
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

# Init app and database
app = Flask(__name__)
# 'FLASK_KEY' => your own key as environment variable
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
# DB_URL -> your own url as environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
db = SQLAlchemy()
db.init_app(app)


# create DB columns
class CafeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cafe_name = db.Column(db.String(500), unique=True, nullable=False)
    cafe_summary = db.Column(db.String(250), nullable=False)
    cafe_map_url = db.Column(db.String(500), nullable=False)
    cafe_img_url = db.Column(db.String(500), nullable=False)
    cafe_rating = db.Column(db.String(250), nullable=False)
    cafe_location = db.Column(db.String(250), nullable=False)
    cafe_seats = db.Column(db.String(250), nullable=False)
    cafe_wifi = db.Column(db.Boolean, nullable=False)
    cafe_toilet = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)


# Create db. Uncomment for first app run
with app.app_context():
    db.create_all()


@app.route('/')
def main():
    """display main page"""
    return render_template('index.html')


@app.route('/add')
def add():
    """add new cafe"""
    pass


@app.route('/delete')
def delete():
    """delete cafe"""
    pass


@app.route('/change')
def patch():
    """change cafe data"""
    pass


@app.route('/search')
def search():
    """get a data on particular cafe"""
    pass


@app.route('/all')
def get_all():
    """get all cafes"""
    pass


if __name__ == '__main__':
    app.run(debug=True)
