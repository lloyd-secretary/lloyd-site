from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_required, current_user, login_user, logout_user
from . import lloyd
from .. import db, login_manager
from ..models import User
from .forms import *

@lloyd.route('/')
@lloyd.route('/index')
def index():
    return render_template("index.html")

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@lloyd.before_request
def before_request():
    g.user = current_user

@lloyd.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        next = request.args.get('next')
        return redirect(next or url_for('lloyd.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next = request.args.get('next')
            return redirect(next or url_for('lloyd.index'))
        flash('Incorrect username and password combination')
        render_template('login.html', form=form)
    return render_template('login.html', form=form)

@lloyd.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('lloyd.index'))

@lloyd.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    password_form = PasswordUpdateForm(request.form, prefix='password_form')


    email_form = SubscriptionsForm(request.form, prefix='email_form')
    # presset nomail field
    email_form.nomail.default = current_user.get_nomail()
    email_form.nomail.process(request.form)
    # preset other mailing list fields
    preselect = current_user.get_mailing_lists()
    email_form.mailinglists.choices = [(k, k) for k in sorted(preselect.keys())]
    email_form.mailinglists.default = [k for k in preselect.keys() if preselect[k] == True]
    email_form.mailinglists.process(request.form)


    account_form = AccountUpdateForm(request.form, prefix='account_form', obj=current_user)


    if password_form.submit.data and password_form.validate_on_submit():
        if not current_user.verify_password(password_form.old.data):
            flash('Incorrect password', 'password')
        elif password_form.new1.data != password_form.new2.data:
            flash('gotta make the new ones match doe', 'password')
        else:
            current_user.set_password(password_form.new1.data)
            db.session.commit()
            flash('password changed successfully', 'password')

    elif email_form.submit.data and email_form.validate_on_submit():
        current_user.set_nomail(email_form.nomail.data)
        current_user.set_mailing_lists(dict({(l, l in email_form.mailinglists.data) for l in preselect.keys()}))
        db.session.commit()
        flash('subscriptions successfully updated', 'email')

    elif account_form.submit.data and account_form.validate_on_submit():
        account_form.populate_obj(current_user)
        db.session.commit()
        flash('personal info successfully updated', 'account')


    return render_template("account.html",
                            password_form=password_form,
                            email_form=email_form,
                            account_form=account_form,
                            user=current_user)

# @lloyd.route('/setpasswords', methods=['GET', 'POST'])
# def setpasswords():
#     users = User.query.all()
#     for u in users:
#         u.set_password(u.temp_pass)
#     db.session.commit()
#     return redirect(url_for('lloyd.index')) 

@lloyd.route('/prefrosh')
def prefrosh():
    return render_template("prefrosh.html")

@lloyd.route('/bylaws')
def bylaws():
    return render_template("bylaws.html")

@lloyd.route('/calendar')
def calendar():
    return render_template("calendar.html")

@lloyd.route('/contact')
def contact():
    return render_template("contact.html")

@lloyd.route('/gallery')
@login_required
def gallery():
    return render_template("gallery.html")

@lloyd.route('/houselist')
@login_required
def houselist():
    people = User.query.all()
    return render_template("houselist.html", people=people)

@lloyd.route('/pong')
@login_required
def pong():
    users = User.query.all()
    return render_template("pong/index.html", users=users)
