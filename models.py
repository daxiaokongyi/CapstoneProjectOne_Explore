from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

# default user image if no image for user 
DEFAULT_IMG = "https://mylostpetalert.com/wp-content/themes/mlpa-child/images/nophoto.gif"

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'foodie'
    username = db.Column(db.String(50), nullable = False, unique = True, primary_key = True)
    password = db.Column(db.String(500), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    age = db.Column(db.Integer, nullable = True)
    gender = db.Column(db.String(50), nullable = True)
    photo_url = db.Column(db.String(500), nullable = True)

    def __repr__(self):
        """Show user info"""
        return f"<User name = {self.username} email = {self.email}>"

    def image_url(self):
        """Set image link with a default img if no link available"""
        return self.photo_url or DEFAULT_IMG

    @classmethod
    def signup(cls, username, pwd, email, age, gender, photo_url):
        """Register user with hashed pasword and return an user object"""
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username = username, password = hashed_utf8, email = email, age = age, gender = gender, photo_url = photo_url)

    @classmethod
    def authenticate(cls, username, password):
        """validate user with password"""
        u = User.query.filter_by(username = username).first()
        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False