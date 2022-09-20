from flask import Flask, g
from flask_login import login_required
from flask_restful import Resource, Api, reqparse
from sqlalchemy import or_
from . import rotation
from .. import db, production
from ..models import Prefrosh, Feedback

api = Api(rotation)

parser = reqparse.RequestParser()
parser.add_argument('comment')
'''
parser.add_argument('fit', type=int)
parser.add_argument('comfort_level', type=int)
parser.add_argument('would_participate', type=int)
parser.add_argument('camel', type=int)
'''

def is_admin():
    return g.user.is_admin

class PrefroshList(Resource):
    if production:
        decorators = [login_required]

    def get(self):
        all_prefrosh = Prefrosh.query.all()
        return {
            'prefroshList': [prefrosh.serialize() for prefrosh in all_prefrosh]
        }

class PrefroshIndividual(Resource):
    if production:
        decorators = [login_required]

    def get(self, prefrosh_id):
            return Prefrosh.query.get(prefrosh_id).serialize()

class PrefroshComments(Resource):
    if production:
        decorators = [login_required]

    def get(self, prefrosh_id):
        print(self)
        user = g.user
        prefrosh = Prefrosh.query.get(prefrosh_id)
        if is_admin():
            comments = Feedback.query.filter_by(Feedback.prefrosh=prefrosh_id).all()
        else:
            comments = Feedback.query.filter(or_(Feedback.user_id==user.id, Feedback.user_id==0)).filter_by(Feedback.prefrosh=prefrosh_id).all()
        return {
            'comments': [comment.serialize() for comment in comments]
        }

    def post(self, prefrosh_id):
        user = g.user
        args = parser.parse_args()
        comment = args["comment"]
        prefrosh = Prefrosh.query.get(prefrosh_id)
        feedback = Feedback(user.id, prefrosh, comment)
        db.session.add(feedback)
        db.session.commit()
        return feedback.serialize()

class Comments(Resource):
    if production:
        decorators = [login_required]

    def delete(self, comment_id):
        feedback = Feedback.query.get(comment_id)
        if feedback:
            db.session.delete(feedback)
            db.session.commit()
        return '', 204

api.add_resource(PrefroshList, '/api/prefrosh')
api.add_resource(PrefroshIndividual, '/api/prefrosh/<int:prefrosh_id>')
api.add_resource(PrefroshComments, '/api/feedback/<int:prefrosh_id>')
api.add_resource(Comments, '/api/comments/<int:comment_id>')
