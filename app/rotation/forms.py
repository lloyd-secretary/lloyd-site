from flask_wtf import Form
from wtforms import TextAreaField
from wtforms import validators

class CommentUpdateForm(Form):
    comment = TextAreaField('comment', [validators.required(), validators.length(max=200)])
	#rating = IntegerField('rating', validators=[DataRequired()])
