from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField 
from wtforms import TextAreaField, FileField, DecimalField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange

class SubmitQueryForm(FlaskForm):
	first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=30)])
	last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=30)])
	store = SelectField(u'Stores', choices=[('Leicester'), ('Nottingham'), ('London'), ('Brighton')], validators=[DataRequired()])
	query = StringField('Query', validators=[DataRequired()])
	submit = SubmitQueryForm('Submit Question')