from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField 
from wtforms import TextAreaField, FileField, DecimalField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange

class AddFAQForm(FlaskForm):
	question = TextAreaField('FAQ Question', validators=[DataRequired()])
	answer = TextAreaField('FAQ Answer', validators=[DataRequired()])
	submit = SubmitField('Add New FAQ')