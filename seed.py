from models import User, Business, FavoriteBusiness, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

User.query.delete()
Business.query.delete()
FavoriteBusiness.query.delete()

user1 = User(username = 'user_one', password = '123', email = 'user1@gmail.com', age = 5, gender = 'male', photo_url = "", favorite_business = [])
user1= User.signup(username = 'user_one', pwd = '123', email = 'user1@gmail.com', age = 5, gender = 'male', photo_url = "", fav = [])

user2 = User(username = 'user_two', password = '123', email = 'user2@gmail.com', age = 6, gender = 'female', photo_url = "http://img.71acg.net/sykb~sykb/20200107/15451081135", favorite_business = [])
user2 = User.signup(username = 'user_two', pwd = '123', email = 'user2@gmail.com', age = 6, gender = 'female', photo_url = "http://img.71acg.net/sykb~sykb/20200107/15451081135", fav = [])

user3 = User(username = 'user_three', password = '123', email = 'user3@gmail.com', age = 7, gender = 'male', photo_url = "", favorite_business = [])
user3 = User.signup(username = 'user_three', pwd = '123', email = 'user3@gmail.com', age = 7, gender = 'male', photo_url = "", fav = [])

db.session.add_all([user1, user2, user3])
db.session.commit()

