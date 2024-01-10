from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField
from wtforms.validators import DataRequired
from src.custom_validators import OptionalInteger

class AddComponentForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    category = StringField('category', validators=[DataRequired()])
    description = StringField('description')
    datasheet = FileField('datasheet') 
    image = FileField('image')
    io_number = OptionalInteger('io_number')