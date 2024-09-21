#import sys
from flask import render_template, g, send_from_directory, flash, redirect, session, url_for, request, redirect

from flask_login import login_required, current_user
from sqlalchemy.sql.functions import now
from . import rotation
from .. import db, login_manager
from ..models import *
from forms import *

import datetime


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# validate all rotation users before serving any page
@rotation.before_request
def before_request():
    if current_user.is_authenticated:
        g.user = current_user
    else:
        return redirect(url_for('lloyd.login'))
    # require user.rotation to see any pages
    if not (g.user.rotation):
       return redirect(url_for('lloyd.account'))
    # for non-rotation season let's not show the frosh this lol
    # return redirect(url_for('lloyd.login'))
    
    
    #print(g.user, file=sys.stderr)

    if g.user.membership == 's':
       return redirect(url_for('lloyd.index'))

def is_admin():
    return g.user.admin

@rotation.route('/')
@rotation.route('/index')
@login_required
def rotation_index():
    dinner = request.args.get('dinner')
    if dinner == None:
        dinner = None
    else:
        try:
            dinner = int(dinner)
        except:
            dinner = None

    # check if the provided dinner is valid
    dinner_info = None
    if dinner != None:
        # get info on dinner
        dinner_info = Dinner.query.filter_by(id=dinner).first()

    if dinner_info == None:
        dinner = None

    # here's a default dinner
    # we want to choose the one that most recently happened
    if dinner == None:
        prevDinners = Dinner.query.order_by(-Dinner.timestamp).filter(Dinner.timestamp < datetime.datetime.now()).first()
        if prevDinners == None:
            firstQuery = Dinner.query.first()
            if firstQuery == None:
                return render_template(
                    "rot_index.html", 
                    prefrosh=[], 
                    left="",
                    right="",
                    dinner="No Dinner",
                    all_prefrosh=[]
                )
            
            dinner = Dinner.query.first().id
        else:
            dinner = prevDinners.id

        dinner_info = Dinner.query.filter_by(id=dinner).first()
    
    # get all the prefrosh for the specific dinner ID
    prefrosh_list = map(lambda el: el.frosh_id, FroshDinners.query.filter_by(dinner_id=dinner).all())
    # get all the details for each prefrosh
    prefrosh_details = Prefrosh.query.filter(Prefrosh.id.in_(prefrosh_list)).all()

    # i admit a bit over-engineered, could just -1 and +1 but I guess this is more versatile 
    # if we were comparing dates or its not intervals of 1 for some reason

    # find the dinner ID that is less (by sorting in reverse order, not that this returns what we sorted by... so negative dinner id)
    left=db.session.query(Dinner.id).distinct().order_by(-Dinner.id).filter(Dinner.id < dinner).first()
    # find the dinner ID that is greater (by sorting in normal order)
    right=db.session.query(Dinner.id).distinct().order_by(Dinner.id).filter(Dinner.id > dinner).first()

    # since it sorts by the negative, we need to flip flop it
    if left != None:
        left = -left.id

    # this one is normal
    if right != None:
        right = right.id
        
    all_prefrosh = map(lambda item: {'id': str(item.id), 'name': '"' + item.firstname + " " + item.lastname + '"'}, Prefrosh.query.all())
    
    # the left and right variables are LINKS that might be empty if there is no link in that direction
    return render_template(
        "rot_index.html", 
        prefrosh=prefrosh_details, 
        left=url_for('rotation.rotation_index', dinner=left) if left != None else "",
        right=url_for('rotation.rotation_index', dinner=right) if right != None else "",
        dinner=datetime.datetime.strftime(dinner_info.timestamp, '%b %d, %I:%M %p'),
        all_prefrosh=all_prefrosh
    )

@rotation.route('/frosh/<int:frosh_id>', methods=['GET', 'POST'])
def rotation_frosh(frosh_id):
    form = CommentUpdateForm()
    # if a form was submitted render this
    if form.validate_on_submit():
        loggedin_user_id = int(current_user.get_id())
        newComment = Feedback(loggedin_user_id, frosh_id, form.comment.data, now())
        db.session.add(newComment)
        db.session.commit()
        return redirect(url_for('rotation.rotation_frosh', frosh_id=frosh_id))

    # otherwise get info on the frosh
    prefrosh = Prefrosh.query.filter_by(id=frosh_id).first()
    comments = Feedback.query.filter_by(frosh_id=frosh_id).all()
    comment_users = [x.user_id for x in comments]
    user_details = User.query.filter(User.id.in_(comment_users)).all()
    user_map = {u.id: u.firstname+" "+u.lastname for u in user_details}
    comments_full = [
        {
         "author": user_map[comments[i].user_id],
         "timestamp": comments[i].timestamp,
         "comment": comments[i].comment
         } for i in range(len(comments))]
    #  oops they don't exist
    if prefrosh is None:
        return redirect(url_for('rotation.index'))

    # normal
    return render_template("frosh.html", prefrosh=prefrosh, comments=comments_full, form=form)

@rotation.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img/', path)
