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
    username = db.Column(db.Text, nullable = False, unique = True, primary_key = True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, nullable = False, unique = True)
    age = db.Column(db.Integer, nullable = True)
    gender = db.Column(db.Text, nullable = True)
    photo_url = db.Column(db.String(500), nullable = True)
    favorite_business = db.relationship('Business', secondary = 'business_favorited', backref='foodie')

    def __repr__(self):
        """Show user info"""
        return f"<User name = {self.username} email = {self.email}>"

    def image_url(self):
        """Set image link with a default img if no link available"""
        return self.photo_url or DEFAULT_IMG

    @classmethod
    def signup(cls, username, pwd, email, age, gender, photo_url, fav):
        """Register user with hashed pasword and return an user object"""
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        user = User(
            username = username, 
            password = hashed_utf8, 
            email = email, 
            age = age, 
            gender = gender, 
            photo_url = photo_url,
            favorite_business = fav
        )

        return user

    @classmethod
    def authenticate(cls, username, password):
        """validate user with password"""
        u = User.query.filter_by(username = username).first()
        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False

class Business(db.Model):
    """Collect all Favorites"""
    __tablename__ = "businesses"

    id = db.Column(db.Integer, primary_key=True, autoincrement = True, nullable = False)
    business_id = db.Column(db.Text, nullable = False)
    business_name = db.Column(db.Text, nullable = False)

class FavoriteBusiness(db.Model):
    __tablename__ = 'business_favorited'
    username = db.Column(db.Text, db.ForeignKey('foodie.username'), primary_key = True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), primary_key = True)