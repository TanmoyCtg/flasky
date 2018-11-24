from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField

from wtforms.validators import Required, Length, Email, Regexp 

from wtforms import ValidationError 

# from flask_pagedown.fields import PageDownField

from ..models import Role, User 

class NameForm(FlaskForm):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Submit')