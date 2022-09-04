from flask_wtf import Form
from wtforms import IntegerField, SelectMultipleField
from wtforms.validators import DataRequired

class CommentUpdateForm(Form):
	comment = IntegerField('comment', validators=[DataRequired()])
	rating = IntegerField('rating', validators=[DataRequired()])


#class Top5(Form):
#	tops = SelectMultipleField('comment', choices=[], validators=[DataRequired()])