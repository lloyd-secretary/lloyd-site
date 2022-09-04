from flask import render_template, g, send_from_directory, flash, redirect, session, url_for, request

from flask_login import login_required, current_user
from . import rotation
from .. import db, login_manager
from ..models import *
from forms import *


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
    if not g.user.rotation:
        return redirect(url_for('lloyd.index'))

def is_admin():
    return g.user.admin

@rotation.route('/')
@login_required
def rotation_home():
    return render_template("rotationUI.html")

@rotation.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img/', path)



# @rotation.route('/top5', methods=['GET', 'POST'])
# @login_required
# def top5():
#     form = Top5(request.form)
#     frosh = Prefrosh.query.all()
#     form.tops.choices = [(str(f.id), f.getFullName()) for f in frosh]
#     if form.validate_on_submit():
#     	if current_user.top5 == 0:
# 	    	res = form.tops.data
# 	    	if len(res) <= 5 and len(res) > 0:
# 		    	for r in res:
# 		    		f = Prefrosh.query.get(int(r))
# 		    		f.top5 += 1
# 		    	current_user.top5 = 1
# 		    	db.session.commit()

#     return render_template("top5.html",
#                             form=form)

# @rotation.route('/bottom5', methods=['GET', 'POST'])
# @login_required
# def bottom5():
#     form = Top5(request.form)
#     frosh = Prefrosh.query.all()
#     form.tops.choices = [(str(f.id), f.getFullName()) for f in frosh]
#     if form.validate_on_submit():
#     	if current_user.bottom5 == 0:
# 	    	res = form.tops.data
# 	    	if len(res) <= 5 and len(res) > 0:
# 		    	for r in res:
# 		    		f = Prefrosh.query.get(int(r))
# 		    		f.bottom5 += 1
# 		    	current_user.bottom5 = 1
# 		    	db.session.commit()

#     return render_template("top5.html",
#                             form=form)

# @rotation.route('/fuckingobfuscatethisurlrealquikshiet', methods=['GET', 'POST'])
# @login_required
# def ratings():
#     form = CommentUpdateForm(request.form)

#     if form.validate_on_submit():
#     	comment = Feedback.query.get(form.comment.data)
#     	comment.rating = form.rating.data
#     	db.session.commit()
#     return render_template("rotationaccount.html",
#                             form=form)
