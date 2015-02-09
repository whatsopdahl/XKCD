from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectField
from wtforms.validators import DataRequired

class ParamForm(Form):
	minWl = SelectField('minWL', 1, choices=[1,2,3,4,5,6,7,8])
	maxWl = SelectField('maxWL', 5, choices=[1,2,3,4,5,6,7,8,9,10])
	maxPswd = StringField('maxPswd', validators=[DataRequired()])
	e = BooleanField('e', default=false)
	o = BooleanField('o', default=false)
	l = BooleanField('l', default=false)
	firstWord = BooleanField('firstword', default=false)
	secondWord = BooleanField('secondword', default=false)
	thirdWord = BooleanField('thirdword', default=false)
	fourthWord = BooleanField('fourthword', default=false)
	optimization = BooleanField('optimizaiton', default=false)
	