from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class AddCoffe(FlaskForm):
    cafe_name = StringField("Name", validators=[DataRequired()])
    cafe_rating = SelectField("Rating", choices=[('⭐', '⭐'),
                                                 ('⭐⭐', '⭐⭐'),
                                                 ('⭐⭐⭐', '⭐⭐⭐'),
                                                 ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
                                                 ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐')], validators=[DataRequired()])
    cafe_location = StringField("Location", validators=[DataRequired()])
    cafe_summary = CKEditorField("Summary", validators=[DataRequired()])
    cafe_seats = StringField("Number of seats", validators=[DataRequired()])
    cafe_wifi = SelectField("Wifi", choices=[('✔️', 'Yes'), ('❌', 'No')], validators=[DataRequired()])
    cafe_toilet = SelectField("Toilet", choices=[('✔️', 'Yes'), ('❌', 'No')], validators=[DataRequired()])
    coffee_price = StringField("Coffee price", validators=[DataRequired()])
    cafe_map_url = StringField("Google Maps URL", validators=[DataRequired(), URL()])
    cafe_img_url = StringField("Cafe photo URL", validators=[DataRequired(), URL()])
    submit = SubmitField('Add')
