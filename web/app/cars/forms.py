from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField 
from wtforms import TextAreaField, FileField, DecimalField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange

class AddNewCarForm(FlaskForm):
	manufacturer = StringField('Manufacturer', validators=[DataRequired(), Length(min=3, max=30)])
	model = StringField('Model', validators=[DataRequired(), Length(min=2, max=50)])
	summary = TextAreaField('Summary', validators=[DataRequired()])
	description = TextAreaField('Description', validators=[DataRequired()])
	year = DecimalField('Year', validators=[DataRequired()])
	mileage = IntegerField('Mileage', validators=[DataRequired()])
	transmission = StringField('Transmission', validators=[DataRequired(), Length(min=1, max=10)])
	fuel = StringField('Fuel', validators=[DataRequired(), Length(min=1, max=10)])
	engine_size = DecimalField('Engine Size', validators=[DataRequired()])
	seats = IntegerField('Seats', validators=[DataRequired()])
	doors = IntegerField('Doors', validators=[DataRequired()])
	colour = StringField('Colour', validators=[DataRequired(), Length(min=3, max=20)])
	mot = BooleanField('Has MOT', validators=[DataRequired()])
	last_mot = TextAreaField('Last MOT', validators=[DataRequired()])
	has_warranty = BooleanField('Has Warranty', validators=[DataRequired()])
	photo = FileField('Upload photo', validators=[FileAllowed(['jpg', 'png'])])
	price = DecimalField('Price', default=1.99, validators=[DataRequired()])
	submit = SubmitField('Add New Car')

class EditCarForm(FlaskForm):
	manufacturer = StringField('Manufacturer', validators=[DataRequired(), Length(min=3, max=30)])
	model = StringField('Model', validators=[DataRequired(), Length(min=2, max=50)])
	summary = TextAreaField('Summary', validators=[DataRequired()])
	description = TextAreaField('Description', validators=[DataRequired()])
	year = DecimalField('Year', validators=[DataRequired()])
	mileage = IntegerField('Mileage', validators=[DataRequired()])
	transmission = StringField('Transmission', validators=[DataRequired(), Length(min=1, max=10)])
	fuel = StringField('Fuel', validators=[DataRequired(), Length(min=1, max=10)])
	engine_size = DecimalField('Engine Size', validators=[DataRequired()])
	seats = IntegerField('Seats', validators=[DataRequired()])
	doors = IntegerField('Doors', validators=[DataRequired()])
	colour = StringField('Colour', validators=[DataRequired(), Length(min=3, max=20)])
	mot = BooleanField('MOT', validators=[DataRequired()])
	last_mot = TextAreaField('Last MOT', validators=[DataRequired()])
	has_warranty = BooleanField('Has Warranty', validators=[DataRequired()])
	photo = FileField('Update Car photo - Only replace if old or incorrect', validators=[FileAllowed(['jpg', 'png'], 'Images only with extension .jpg or .png') ])
	price = DecimalField('Price', default=1.99)
	update = SubmitField('Update Car')
	cancel = SubmitField('Cancel')