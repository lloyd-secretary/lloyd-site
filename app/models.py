from app import db, bcrypt
from flask_login import UserMixin
from sqlalchemy.inspection import inspect

db.reflect()

# Anish's picture is temporarily the default
default_photo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Jeb_Bush_by_Gage_Skidmore_2.jpg/1200px-Jeb_Bush_by_Gage_Skidmore_2.jpg"

DATABASE_NAME = 'rotation2024'

class User(db.Model, UserMixin):
    __tablename__ = 'houselist'

    def __init__(self, username, password=None, year=None, membership=None, firstname=None, lastname=None, nickname=None, address=None, major=None, email=None, cellphone=None, birthday=None):
        self.username = username
        if password is not None:
            self.password = bcrypt.generate_password_hash(password)
        self.year = year
        self.membership = membership
        self.firstname = firstname
        self.lastname = lastname
        self.nickname = nickname
        self.address = address
        self.major = major 
        self.email = email
        self.cellphone = cellphone
        self.birthday = birthday

    def __repr__(self):
        return '<User %r>' % self.username

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def get_nomail(self):
        return self.nomail

    def set_nomail(self, nomail):
        self.nomail = nomail

    def get_rotation(self):
        return self.rotation

    def set_full(self, membership):
        self.membership = membership

    __subscribable_mailing_lists = ['all',
                                    'lloydspam',
                                    'spam',
                                    'pastandpresent',
                                    'summer',
                                   ]

    def get_mailing_lists(self):
        # returns a dictionary of  'mailinglistname': subscribedOrNot pairs
        return {l: getattr(self, l) for l in self.__subscribable_mailing_lists}

    def set_mailing_lists(self, subscriptions):
        # subscriptions should be an iterable of (string, boolean) key value pairs
        # ex: 'mailinglistname': subscribedOrNot
        for s in self.__subscribable_mailing_lists:
            # then we set the db values to those in subscriptions
            setattr(self, s, int(subscriptions[s]))

    def admin(self):
        return self.is_admin == 1

def load_user(user_id):
    return User.query.get(int(user_id))

class Prefrosh(db.Model):
    __tablename__ = 'prefrosh'
    __bind_key__ = DATABASE_NAME

    def __repr__(self):
        return '<Prefrosh %r>' % (self.firstname + " " + self.lastname)

    def getFullName(self):
        return self.firstname + " " + self.lastname

    def serialize(self):
        photo_url = default_photo_url
        if self.photo_url and self.photo_url != '':
            photo_url = self.photo_url
        return {
            'id': self.id,
            'displayName': self.getFullName(),
            'preferredName': self.getFullName(),
            'photo_url': photo_url
        }

class Feedback(db.Model):
    __tablename__ = 'feedback'
    __bind_key__ = DATABASE_NAME

    def __repr__(self):
        return '<Feedback %r>' % (str(self.user_id) + " for " + str(self.frosh_id))

    def __init__(self, user_id, pf, comment, timestamp):
        self.user_id = user_id
        self.frosh_id = pf
        self.comment = comment
        self.timestamp = timestamp

    def serialize(self):
        return {
            'id': self.id,
            'user': load_user(self.user_id).username,
            'prefrosh': self.frosh_id,
            'content': self.comment,
            'timestamp': self.timestamp,
        }

class Dinner(db.Model):
    __tablename__ = 'dinners'
    __bind_key__ = DATABASE_NAME


class FroshDinners(db.Model):
    __tablename__ = 'froshdinners'
    __bind_key__ = DATABASE_NAME
   
    def __init__(self, frosh_id, dinner_id):
        self.frosh_id = frosh_id
        self.dinner_id = dinner_id

