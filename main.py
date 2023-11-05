from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, jsonify, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from forms import AddCoffe
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

# Init app and database
app = Flask(__name__)
# 'FLASK_KEY' => your own key as environment variable
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')

ckeditor = CKEditor(app)
Bootstrap5(app)

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
    cafe_wifi = db.Column(db.String(250), nullable=False)
    cafe_toilet = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)


# Create db. Uncomment for first app run
with app.app_context():
    db.create_all()


def get_cafe(all_cafes: []):
    cafes_json = {'cafes': []}
    for cafe in all_cafes:
        new_cafe = {'name': cafe.cafe_name,
                    'summary': cafe.cafe_summary,
                    'rating': cafe.cafe_rating,
                    'location': cafe.cafe_location,
                    'wifi': cafe.cafe_wifi,
                    'toilet': cafe.cafe_toilet,
                    'seats': cafe.cafe_seats,
                    'coffee_price': cafe.coffee_price,
                    'img_url': cafe.cafe_img_url,
                    'map_url': cafe.cafe_map_url}
        cafes_json['cafes'].append(new_cafe)
    return cafes_json


@app.route('/', methods=['GET', "POST"])
def main():
    if request.method == 'POST':
        result = db.session.query(CafeData).where(CafeData.cafe_name == request.form.get('search'))
        cafes = [result.scalar()]
        return render_template('index.html', cafes=cafes)
    # get data from BD
    result = db.session.execute(db.select(CafeData))
    cafes = result.scalars().all()
    """display main page"""
    return render_template('index.html', cafes=cafes)


@app.route('/add', methods=['POST', 'GET'])
def add():
    """add new cafe"""
    # pass a form
    form = AddCoffe()
    # add new cafe from submit form
    if form.validate_on_submit():
        try:
            new_cafe = CafeData(
                cafe_name=form.cafe_name.data,
                cafe_summary=form.cafe_summary.data,
                cafe_map_url=form.cafe_map_url.data,
                cafe_img_url=form.cafe_img_url.data,
                cafe_rating=form.cafe_rating.data,
                cafe_location=form.cafe_location.data,
                cafe_seats=form.cafe_seats.data,
                cafe_wifi=form.cafe_wifi.data,
                cafe_toilet=form.cafe_toilet.data,
                coffee_price=form.coffee_price.data,
                date=str(date.today())
            )
            db.session.add(new_cafe)
            db.session.commit()
        except IntegrityError:
            flash('Name already in use.')
            return render_template('add_coffee.html', add_form=form, title='Add new cafe')
        else:
            return redirect(url_for('main'))
    return render_template('add_coffee.html', add_form=form, title='Add new cafe')


@app.route('/delete/<int:cafe_id>', methods=['DELETE'])
def delete(cafe_id):
    """delete cafe"""
    cafe_to_delete = db.session.query(CafeData).where(CafeData.id == cafe_id)
    if not cafe_to_delete.all():
        error = {"error": {
            "Not found": "Sorry, wrong cafe id"
        }
        }
        return jsonify(error)
    else:
        if request.form.get('key') == os.environ.get('DELETE_KEY'):
            db.session.delete(cafe_to_delete.scalar())
            db.session.commit()
            success = {"response": {
                "success": 'Successfully updated the price.'
            }}
            return jsonify(success)
        wrong_key = {"error": {
            "Not found": "Sorry, wrong key. Make sure you hava a valid key required to delete cafes."
        }
        }
        return jsonify(wrong_key)


@app.route('/change/<int:cafe_id>', methods=['POST', 'PATCH', 'GET'])
def patch(cafe_id):
    columns = CafeData.__table__.columns.keys()
    """change cafe data"""
    # get cafe
    cafe = db.get_or_404(CafeData, cafe_id)
    edit_form = AddCoffe(
        cafe_name=cafe.cafe_name,
        cafe_rating=cafe.cafe_rating,
        cafe_location=cafe.cafe_location,
        cafe_summary=cafe.cafe_summary,
        cafe_seats=cafe.cafe_seats,
        cafe_wifi=cafe.cafe_wifi,
        cafe_toilet=cafe.cafe_toilet,
        coffee_price=cafe.coffee_price,
        cafe_map_url=cafe.cafe_map_url,
        cafe_img_url=cafe.cafe_img_url
    )
    if edit_form.validate_on_submit():
        cafe.cafe_name = edit_form.cafe_name.data
        cafe.cafe_rating = edit_form.cafe_rating.data
        cafe.cafe_location = edit_form.cafe_location.data
        cafe.cafe_summary = edit_form.cafe_summary.data
        cafe.cafe_seats = edit_form.cafe_seats.data
        cafe.cafe_wifi = edit_form.cafe_wifi.data
        cafe.cafe_toilet = edit_form.cafe_toilet.data
        cafe.coffee_price = edit_form.coffee_price.data
        cafe.cafe_map_url = edit_form.cafe_map_url.data
        cafe.cafe_img_url = edit_form.cafe_img_url.data
        cafe.date = str(date.today())
        db.session.commit()
        return redirect(url_for('main'))
    if request.method == 'PATCH':
        if not request.form.get('cafe_name'):
            pass
        else:
            cafe.cafe_name = request.form.get('cafe_name')
        if not request.form.get('cafe_rating'):
            pass
        else:
            cafe.cafe_rating = request.form.get('cafe_rating')
        if not request.form.get('cafe_location'):
            pass
        else:
            cafe.cafe_location = request.form.get('cafe_location')
        if not request.form.get('cafe_summary'):
            pass
        else:
            cafe.cafe_summary = request.form.get('cafe_summary')
        if not request.form.get('cafe_seats'):
            pass
        else:
            cafe.cafe_seats = request.form.get('cafe_seats')
        if not request.form.get('cafe_wifi'):
            pass
        else:
            cafe.cafe_wifi = request.form.get('cafe_wifi')
        if not request.form.get('cafe_toilet'):
            pass
        else:
            cafe.cafe_toilet = request.form.get('cafe_toilet')
        if not request.form.get('coffee_price'):
            pass
        else:
            cafe.coffee_price = request.form.get('coffee_price')
        if not request.form.get('cafe_map_url'):
            pass
        else:
            cafe.cafe_map_url = request.form.get('cafe_map_url')
        if not request.form.get('cafe_img_url'):
            pass
        else:
            cafe.cafe_img_url = request.form.get('cafe_img_url')

        cafe.date = str(date.today())
        db.session.commit()
        success = {"response": {
            "success": 'Successfully updated the price.'
        }}
        return jsonify(success)
    return render_template('add_coffee.html', add_form=edit_form, title='Edit cafe')


@app.route('/search', methods=['GET'])
def search():
    """get a data on particular cafe"""
    loc = request.args['loc']
    response = db.session.query(CafeData).where(CafeData.cafe_location == loc)
    cafes = response.all()
    if not cafes:
        error = {"error": {
            "Not found": "Sorry, we don't have a cafe at that location."
        }
        }
        return jsonify(error)
    fetched_cafes = get_cafe(cafes)
    return jsonify(fetched_cafes)


@app.route('/all')
def get_all():
    """get all cafes"""
    response = db.session.query(CafeData)
    cafes = response.all()
    if not cafes:
        error = {"error": {
            "Not found": "Sorry, we don't have any cafes collected."
        }
        }
        return jsonify(error)
    fetched_cafes = get_cafe(cafes)
    return jsonify(fetched_cafes)


@app.route('/add_cafe', methods=['POST', 'GET'])
def add_cafe():
    """add a cafe"""
    if request.method == 'POST':
        try:
            new_cafe = CafeData(
                cafe_name=request.form.get('cafe_name'),
                cafe_summary=request.form.get('cafe_summary'),
                cafe_map_url=request.form.get('cafe_map_url'),
                cafe_img_url=request.form.get('cafe_img_url'),
                cafe_rating=request.form.get('cafe_rating'),
                cafe_location=request.form.get('cafe_location'),
                cafe_seats=request.form.get('cafe_seats'),
                cafe_wifi=request.form.get('cafe_wifi'),
                cafe_toilet=request.form.get('cafe_toilet'),
                coffee_price=request.form.get('coffee_price'),
                date=str(date.today())
            )
            db.session.add(new_cafe)
            db.session.commit()
        except IntegrityError:
            error = {"response": {
                "error": 'Name already in use.'
            }}
            return jsonify(error)
        else:
            success = {"response": {
                'success': 'New cafe has been added to DB'
            }}
            return jsonify(success)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
