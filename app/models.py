from app import db, bcrypt
from flask_login import UserMixin

db.reflect()

# Anish's picture is temporarily the default
default_photo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Jeb_Bush_by_Gage_Skidmore_2.jpg/1200px-Jeb_Bush_by_Gage_Skidmore_2.jpg"

class User(db.Model, UserMixin):
    __tablename__ = 'houselist'

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)

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

def load_user(user_id):
    return User.query.get(int(user_id))

class Prefrosh(db.Model):
    __tablename__ = 'prefrosh'
    __bind_key__ = 'rotation'

    def __repr__(self):
        return '<Prefrosh %r>' % (self.firstname + " " + self.lastname)

    def getFullName(self):
        fullname = [self.firstname]
        if self.nickname:
            fullname += ["(" + self.nickname + ")"]
        if self.middlename:
            fullname += [self.middlename]
        fullname += [self.lastname]
        return " ".join(fullname)

    def getPreferredName(self):
        if self.nickname:
            return self.nickname
        return self.firstname

    def serialize(self):
        photo_url = default_photo_url
        if self.photo_url and self.photo_url != '':
            photo_url = self.photo_url
        return {
            'id': self.id,
            'displayName': self.getFullName(),
            'preferredName': self.getPreferredName(),
            'photo_url': photo_url,
            'rotationHouse': self.house.name,
            'dinner_id': self.dinner.id,
            'dessert_id': self.dessert.id,
            'comeback': self.comeback,
        }

class Feedback(db.Model):
    __tablename__ = 'feedback'
    __bind_key__ = 'rotation'

    def __repr__(self):
        return '<Feedback %r>' % (str(self.user_id) + " for " + str(self.frosh_id))

    def __init__(self, user_id, pf, comment):
        self.user_id = user_id
        self.prefrosh = pf
        self.comment = comment

    def serialize(self):
        return {
            'id': self.id,
            'user': load_user(self.user_id).username,
            'prefrosh': self.prefrosh.getFullName(),
            'content': self.comment,
            'rating': self.rating,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %I:%M %p'),
        }

class House(db.Model):
    __tablename__ = 'houses'
    __bind_key__ = 'rotation'

class Dinner(db.Model):
    __tablename__ = 'dinners'
    __bind_key__ = 'rotation'

class Dessert(db.Model):
    __tablename__ = 'desserts'
    __bind_key__ = 'rotation'

class Rating(db.Model):
    __tablename__ = 'ratings'
    __bind_key__ = 'rotation'

    def __init__(self, user_id, pf, fit, comfort_level, would_participate, camel):
        self.user_id = user_id
        self.prefrosh = pf
        self.fit = fit
        self.comfort_level = comfort_level
        self.would_participate = would_participate
        self.camel = camel

    def serialize(self):
        return {
            'id': self.id,
            'user': load_user(self.user_id).username,
            'prefrosh': self.prefrosh.getFullName(),
            'fit': self.fit,
            'comfort_level': self.comfort_level,
            'would_participate': self.would_participate,
            'camel': self.camel,
        }
