from flask_wtf import Form
from wtforms import TextAreaField
from wtforms import validators

class CommentUpdateForm(Form):
    comment = TextAreaField('commentTextArea', [validators.required(), validators.length(max=400)])
	#rating = IntegerField('rating', validators=[DataRequired()])
