from flask_wtf import Form
from wtforms import IntegerField
from wtforms.validators import DataRequired

class CommentUpdateForm(Form):
	comment = IntegerField('comment', validators=[DataRequired()])
	rating = IntegerField('rating', validators=[DataRequired()])