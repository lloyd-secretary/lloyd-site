from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_required, current_user, login_user, logout_user
from . import lloyd
from .. import db, login_manager
from ..models import User, FroshDinners, Prefrosh, Dinner
from .forms import *
import json
import datetime
import re
from oauthlib.oauth2 import WebApplicationClient
import requests
import unicodedata
import os

OAuthEnabled = True
try:
    import secrets

    GOOGLE_CLIENT_ID = secrets.Google_ID
    GOOGLE_CLIENT_SECRET = secrets.Google_Client
    GOOGLE_DISCOVERY_URL = secrets.Google_URL

    client = WebApplicationClient(GOOGLE_CLIENT_ID)
except:
    OAuthEnabled = False



def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@lloyd.route('/')
@lloyd.route('/index')
def index():
    questions = [
        "When is Red Door open? Can I really get a quesadilla at 1:55am?",
        "What do I do if there are ants in my room?",
        "Are all rooms in lloyd doubles? Also, what's a double?",
        "Summarize the process of rotation for me",
        "What are the excomm positions? How do I become president of Lloyd?"
    ]
    return render_template("index.html", questions=questions)

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

@lloyd.route('/Glogin', methods=['GET', 'POST'])
def Glogin():
    if not OAuthEnabled:
        flash("Google Authentication not enabled. Contact Secretary for details")
        return redirect(url_for('lloyd.login'))
        
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@lloyd.route("/Glogin/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Gets users information based on the tokens
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # Verify user email and get email address
    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
    
    user = User.query.filter_by(email=users_email).first()
    if user is not None:
        login_user(user)
        return redirect(url_for('lloyd.index'))
    else:
        flash("Email not recognized, contact Lloyd secretary to reset email")
        return redirect(url_for('lloyd.login'))  

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

    rotation_form = RotationForm(request.form, prefix="rotation_form", rotation=current_user.get_rotation())

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

    elif rotation_form.submit.data and rotation_form.validate_on_submit():
        current_user.rotation = rotation_form.rotation.data
        db.session.commit()
        
        if current_user.rotation == 1:
            return redirect(url_for('rotation.rotation_index'))
        
        flash('rotation status info successfully updated', 'rotation')


    return render_template("account.html",
                            password_form=password_form,
                            email_form=email_form,
                            account_form=account_form,
                            rotation_form=rotation_form,
                            user=current_user)


@lloyd.route('/checkin', methods=['GET', 'POST'])
def checkin():
    checkin_form = CheckinForm(request.form, prefix='checkin_form')

    if checkin_form.submit.data and checkin_form.validate_on_submit():
        print ("here")
        print (dir(datetime.datetime))
        # get the most recent dinner
        prevDinners = Dinner.query.order_by(-Dinner.timestamp).filter(Dinner.timestamp < datetime.datetime.now()).first()

        # get the frosh that matches based on email
        froshName = checkin_form.name.data
        if len(froshName.split(" ")) == 1:
            flash("Please provide your full name.")
            return render_template("checkin.html",
                            checkin_form=checkin_form)

        froshFound = Prefrosh.query.filter(Prefrosh.firstname + " " + Prefrosh.lastname == checkin_form.name.data).first()

        if froshFound == None:
            candidates = []
            firstName = froshName.split(" ")[0].lower()
            lastName = froshName.split(" ")[-1].lower()
            
            for frosh in Prefrosh.query.filter(Prefrosh.firstname.ilike(firstName)).all():
                candidates.append(frosh.firstname + " " + frosh.lastname)
            for frosh in Prefrosh.query.filter(Prefrosh.lastname.ilike(lastName)).all():
                candidates.append(frosh.firstname + " " + frosh.lastname)

            print (candidates)

            if len(candidates) == 0:
                flash("Hmm.... we couldn't find a prefrosh with that first or last name")
                return render_template("checkin.html",
                            checkin_form=checkin_form)
            else:
                flash("Hmm.... we couldn't find a prefrosh with that name. Here are the people we have with the same first or last names: " + ", ".join(candidates))
                flash("Try using the exact name we have on record... it might be legal name...")
                return render_template("checkin.html",
                            checkin_form=checkin_form)

        frosh = FroshDinners(frosh_id=froshFound.id, dinner_id=prevDinners.id)
        try:
            db.session.add(frosh)
            db.session.commit()
            flash('You\'ve checked in!', 'checkin')
        except:
            db.session.rollback()
            flash('You\'ve already checked in!', 'error')

    return render_template("checkin.html",
                            checkin_form=checkin_form)



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
def gallery():
    relfolder = 'static/img/album/'
    dirname = os.path.dirname(__file__)
    folder = os.path.join(dirname, relfolder)
    hists = os.listdir(folder)
    hists.sort()
    hists = ['img/album/' + file for file in hists]
    return render_template("gallery.html", hists = hists)

@lloyd.route('/privacy')
def privacy():
    return render_template("privacy.html")

@lloyd.route('/houselist')
@login_required
def houselist():
    people = User.query.all()
    is_admin = current_user.admin()
    return render_template("houselist.html", people=people, is_admin=is_admin)

@lloyd.route('/getUserDetails',methods=['POST'])
@login_required
def getUserDetails():
    people = User.query.all()
    colNames = ['year', 'membership', 'firstname', 'nickname', 'lastname', 'address', 'major', 'email', 'cellphone', 'birthday']
    
    candidates = filter(lambda x: x.email == request.form['email'], people)
    if len(candidates) == 0:
        data = {val: None for val in colNames}
    else:
        target = candidates[0]
        def format(x):
            if isinstance(x, datetime.date):
                return x.strftime("%m/%d/%Y")
            else:
                return x
        data = {val: format(getattr(target, val)) for val in colNames}
    return json.dumps(data)

@lloyd.route('/updateUserDetails',methods=['POST'])
@login_required
def updateUserDetails():
    if not current_user.is_admin:
        return "Failed"
    
    people = User.query.all()
    colNames = ['year', 'membership', 'firstname', 'nickname', 'lastname', 'address', 'major', 'email', 'cellphone', 'birthday']
    
    candidates = filter(lambda x: x.email == request.form['email'], people)
    if len(candidates) == 0:
        data = {val: None for val in colNames}
    else:
        target = candidates[0]
        if request.form['membership'] in ['s', 'f']:
            target.set_full(request.form['membership'])
        db.session.commit()
        return json.dumps(request.form)
    
@lloyd.route('/addUserDetails',methods=['POST'])
@login_required
def addUserDetails():
    if not current_user.is_admin:
        return "Failed"
    
    username = re.sub("[^A-Za-z]", "", (request.form['firstname']+request.form['lastname']).lower())
    firstname = request.form['firstname'].title()
    lastname = request.form['lastname'].title()
    email = request.form['email'].lower()
    birthday = request.form['birthday']
    if birthday == "":
        birthday = u'0000-00-00'
        
    user = User(username=username, year=request.form['year'], membership=request.form['membership'], firstname=firstname, lastname=lastname, nickname=request.form['nickname'], address=request.form['address'], major=request.form['major'], email=email, cellphone=request.form['cellphone'], birthday=birthday)
    db.session.add(user)
    db.session.commit()
    return json.dumps(request.form)

@lloyd.route('/removeUser',methods=['POST'])
@login_required
def removeUser():
    if not current_user.is_admin:
        return "Failed"

    email = request.form['email']
    User.query.filter_by(email=email).delete()
    db.session.commit()
    return json.dumps(request.form)

# @lloyd.route('/pong')
# @login_required
# def pong():
#     users = User.query.all()
#     return render_template("pong.html", users=users)

@lloyd.route('/resources')
@login_required
def resources():
    return render_template("resources.html")
