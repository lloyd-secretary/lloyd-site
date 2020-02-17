from flask_wtf import Form
from wtforms import SubmitField, StringField, BooleanField, PasswordField, SelectMultipleField, RadioField, DateField, widgets
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import DataRequired, Length, Regexp
# from wtforms_components import PhoneNumberField

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()], render_kw={"placeholder": "username"})
	password = PasswordField('password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

class AccountUpdateForm(Form):
	nickname = StringField('nickname', validators=[], render_kw={"placeholder": "nickname"})
	major = StringField('major', validators=[], render_kw={"placeholder": "major"})
	email = EmailField('email', validators=[DataRequired()], render_kw={"placeholder": "email"})
	cellphone = TelField('cellphone', validators=[Regexp("^\d{10}$", message=u"Enter 10 digits")], render_kw={"placeholder": "cellphone"})
	birthday = DateField('birthday', validators=[])
	submit = SubmitField("Update Account")
	

class PasswordUpdateForm(Form):
	old = PasswordField('old', validators=[DataRequired()])
	new1 = PasswordField('new1', validators=[DataRequired()])
	new2 = PasswordField('new2', validators=[DataRequired()])
	submit = SubmitField("Update Password")


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SubscriptionsForm(Form):
	nomail = BooleanField('nomail')
	mailinglists = MultiCheckboxField('mailinglists', choices=[], default=[])
	submit = SubmitField("Update Subscriptions")

