from flask import Flask, g
from flask_login import login_required
from flask_restful import Resource, Api, reqparse
from sqlalchemy import or_
from . import rotation
from .. import db, login_manager, app, production
from ..models import User, Prefrosh, Feedback, House, Dinner, Dessert, Rating

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
        user = g.user
        prefrosh = Prefrosh.query.get(prefrosh_id)
        if is_admin():
            comments = Feedback.query.filter_by(prefrosh=prefrosh).all()
        else:
            comments = Feedback.query.filter(or_(Feedback.user_id==user.id, Feedback.user_id==0)).filter_by(prefrosh=prefrosh).all()
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

class PrefroshRating(Resource):
    if production:
        decorators = [login_required]

    def get(self, prefrosh_id):
        user = g.user

        prefrosh = Prefrosh.query.get(prefrosh_id)
        # For admin, return average
        if is_admin():
            ratings = Rating.query.filter_by(prefrosh=prefrosh).all()
            if ratings:
                # Functional programming swag
                average_fit = reduce(lambda x, y: x + y.fit, ratings, 0) * 1.0 / len(ratings)
                average_comfort_level = reduce(lambda x, y: x + y.comfort_level, ratings, 0) * 1.0 / len(ratings)
                average_would_participate = reduce(lambda x, y: x + y.would_participate, ratings, 0) * 1.0 / len(ratings)
                average_camel = reduce(lambda x, y: x + y.camel, ratings, 0) * 1.0 / len(ratings)
                return {
                    "fit": average_fit,
                    "comfort_level": average_comfort_level,
                    "would_participate": average_would_participate,
                    "camel": average_camel,
                }
            else:
                return None
        # Else, return corresponding rating
        else:
            ratings = Rating.query.filter_by(user_id=user.id).filter_by(prefrosh=prefrosh).all()
            if ratings:
                return ratings[0].serialize()
            else:
                return None

    def post(self, prefrosh_id):
        user = g.user

        prefrosh = Prefrosh.query.get(prefrosh_id)
        args = parser.parse_args()
        new_fit = args["fit"]
        new_comfort_level = args["comfort_level"]
        new_would_participate = args["would_participate"]
        new_camel = args["camel"]
        ratings = Rating.query.filter_by(user_id=user.id).filter_by(prefrosh=prefrosh).all()

        if ratings:
            rating = ratings[0]
            rating.fit = new_fit
            rating.comfort_level = new_comfort_level
            rating.would_participate = new_would_participate
            rating.camel = new_camel
        else:
            rating = Rating(user.id, prefrosh, new_fit, new_comfort_level, new_would_participate, new_camel)
            db.session.add(rating)

        db.session.commit()
        return rating.serialize()


api.add_resource(PrefroshList, '/api/prefrosh')
api.add_resource(PrefroshIndividual, '/api/prefrosh/<int:prefrosh_id>')
api.add_resource(PrefroshComments, '/api/feedback/<int:prefrosh_id>')
api.add_resource(Comments, '/api/comments/<int:comment_id>')
api.add_resource(PrefroshRating, '/api/rating/<int:prefrosh_id>')
