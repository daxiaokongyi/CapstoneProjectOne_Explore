from flask import Flask, render_template, redirect, flash, session, request, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_uploads import configure_uploads, IMAGES, UploadSet
from sqlalchemy.exc import IntegrityError
from forms import SignInForm, SignUpForm, EditForm, DeleteForm
from models import db, User, Business, FavoriteBusiness, connect_db
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import Unauthorized, Forbidden
import requests
import json
import os

app = Flask(__name__)
app.debug = False

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secretkeyissecretkey')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql:///foods')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['UPLOADED_IMAGES_DEST'] = 'static'

if (os.environ.get('API_SECRET_KEY')):
    app.config['API_SECRET_KEY'] = os.environ.get('API_SECRET_KEY');
    API_SECRET_KEY = os.environ.get('API_SECRET_KEY');
else:
    from secrets import API_SECRET_KEY
    app.config['API_SECRET_KEY'] = API_SECRET_KEY;

API_BASE_URL = "https://api.yelp.com/v3"
headers = {'Authorization':'Bearer %s' % API_SECRET_KEY}

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

toolbar = DebugToolbarExtension(app)

CURR_USER_KEY = 'curr_user'

connect_db(app)
# Create all tables
db.create_all()

@app.before_request
def add_user_to_g():
    """if user logged in, add cur user to Flask global"""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Log in user"""
    session[CURR_USER_KEY] = user.username

def do_logout():
    """Log out user"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

# Home Page
@app.route('/')
def home():
    """Home Page"""
    business_array = []
    current_alias = None
    title = None

    # check if user signs in
    if g.user:
        businesses = g.user.favorite_business

        for business in businesses: 
            url = API_BASE_URL + '/businesses/' + business.business_id

            req = requests.get(url, headers = headers)
            business = json.loads(req.text)
            business_array.append(business)

        # get the latest alias
        if business_array != []:
            last_business = business_array[len(business_array) - 1]
            current_category = last_business.get('categories', None)
            current_title = list(current_category[0].get('title', None).split(' '))
            title = current_title[0]

        if (title):
            return redirect('/categories/' + title)
        else:
            default_city = session["location"]
            return render_template('homepage/defaultWithCity.html', city = default_city)
    else:
        if not session.get('current_latitude') and not session.get('current_longitude') and not session.get('current_city'):
            session['location'] = 'San Francisco'
            return render_template('homepage/default.html', city = 'San Francisco');
        else:
            default_lat = session['current_latitude']
            default_long = session['current_longitude']
            session['location'] = session['current_city']
            return render_template('homepage/defaultWithCity.html', city = session['location'])

# =============================================================================================================================

# User Sign Up 
@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    """User Register Page"""
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data
            email = form.email.data
            gender = form.gender.data
            age = form.age.data
            photo_url = form.photo_url.data
            favorite_business = []

            new_user = User.signup(username, password, email, age, gender, photo_url, favorite_business)

            if form.file.data is not None and form.file.data.filename is not '':
                filename = images.save(form.file.data)
                # if filename != None:
                # new_user.photo_url = f'/static/{filename}'
                new_user.photo_url = '/static/' + filename
            else:
                new_user.photo_url = User.image_url(new_user)

            db.session.add(new_user)            
            db.session.commit()

            flash('Welcome ' + new_user.username + '! Enjoy your foodie jouney', 'success')

        except IntegrityError:
            flash("User name or Email was already taken", "danger")
            return render_template("users/signup.html", form = form, city = session['location'])

        # keep user in the session
        do_login(new_user)
        return redirect('/users/' + new_user.username)
    else:    
        return render_template("users/signup.html", form = form, city = session['location'])

# =============================================================================================================================

# User Edit Info Page 
@app.route('/edit', methods=['GET', 'POST'])
def edit_profile():
    """Update profile for the current user"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect('/')

    user = g.user
    form = EditForm(obj = user)

    if form.validate_on_submit():
        try:
            if User.authenticate(user.username, form.password.data):
                user.email = form.email.data
                user.gender = form.gender.data
                user.age = form.age.data
                user.photo_url = form.photo_url.data

                if form.file.data is not None and form.file.data.filename != '':
                    filename = images.save(form.file.data)
                    # if filename != None:
                    # user.photo_url = f'/static/{filename}'
                    user.photo_url = '/static/' + filename
                else:
                    user.photo_url = User.image_url(user)

                db.session.commit()
                flash('Thank you ' + user.username + '! Your profile has been updated', 'success')
                return redirect('/users/' + user.username)
                        
            flash("Wrong password, please try again.", "danger")
            return render_template("users/edit.html", form = form, city = session['location'])

        except IndentationError:
            flash("Unauthorized.", "danger")
            return render_template("users/edit.html", form = form, city = session['location'])

        # keep user in the session
        do_login(user)
        return redirect('/users/' + user.username)
    else:    
        return render_template("users/edit.html", form = form, city = session['location'])

# =============================================================================================================================

# User Sign In 
@app.route('/signin', methods = ['GET', 'POST'])
def sign_in():
    """Sign In Page"""
    form = SignInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            do_login(user);
            flash('Welcome back, ' + user.username + '!', "success")
            return redirect('/users/' + user.username)
        else:
            form.username.errors = ['Incorrect username or password. Please try again']

    return render_template('users/signin.html', form = form, city = session['location'])

@app.route('/logout')
def log_out():
    """Log user out"""
    do_logout()
    flash("Logged out successfully", "success")
    return redirect('/')

# =============================================================================================================================

# User's info 
@app.route('/users/<username>')
def detail_user(username):
    """Show the detail of the user"""
    if CURR_USER_KEY not in session:
        raise Unauthorized()

    if username != session[CURR_USER_KEY]:
        raise Forbidden()

    user = User.query.get(session[CURR_USER_KEY])
    
    if g.user:
        businesses_favorited = g.user.favorite_business
    else:
        businesses_favorited = None

    return render_template('users/info.html', user = user, businesses = businesses_favorited, city = session['location'])

# =============================================================================================================================

# Delete User 
@app.route('/users/delete', methods=['POST'])
def delete_user():
    """Delete user"""
    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect('/')
    else:
        flash("User was deleted successfully", "danger")

    do_logout()
    db.session.delete(g.user)
    db.session.commit()

    return redirect('/')

# =============================================================================================================================

# Search for Business 
@app.route('/businesses/search')
def businesses_search():
    url = API_BASE_URL + '/businesses/search' 

    # check if term is valid 
    if request.args['term']:
        term = request.args['term']
    else:
        term = 'Restaurants'

    # check if location is valid
    if request.args['location']:
        location = request.args['location']
        session['location'] = location
    else:
        if session.get('current_city'):
            location = str(session['current_latitude']) + ', ' + str(session['current_longitude'])
            session['location'] = session['current_city']
        else:
            location = 'San Francisco'
            session['location'] = location

    params = {'term':term, 'location':location}
    req = requests.get(url , params = params, headers = headers)

    # check if res.status code is 400
    if req.status_code == 400:
        return render_template('404.html', city = session['location'])

    parsed = json.loads(req.text)
    businesses = parsed['businesses']

    # check if businesses is an empty array
    if businesses == []:
        return render_template('404.html', city = session['location'])
    else: 
        return render_template('business/items.html', businesses = businesses, city = session['location'])

# =============================================================================================================================

# Search for a specific categories 
@app.route('/categories/<title>')
def get_alias(title):
    # default latitude and longitude
    url = API_BASE_URL + '/businesses/search' 
        
    if 'current_latitude' not in session and 'current_longitude' not in session:
        # set a default latitude and longitude
        my_lat = 37.7749
        my_long = -122.4194
        location = str(my_lat) + ',' + str(my_long)
        city = 'San Francisco'
        session['location'] = 'San Francisco'
    else:
        # get current location
        current_lat = session['current_latitude']
        current_log = session['current_longitude']
        location = str(current_lat) + ', ' + str(current_log)
        city = session.get('current_city')

    params = {'term':title, 'location': location}
    req = requests.get(url, params = params, headers = headers)
    parsed = json.loads(req.text)    

    businesses = parsed['businesses']

    # check if businesses is empty or not
    if businesses == []:
        return render_template('404.html')

    session['category'] = title
    print(session['category'])
    return render_template('business/items.html', businesses = businesses, city = city)

# =============================================================================================================================

# Get business's detail 
@app.route('/foodies/details/<id>')
def get_detail(id):
    business_favorited = False 
    
    # check if this business marked as favorited or not
    # if user logs in already
    if g.user and g.user.favorite_business != []:
        # if Business.query.all() != [] and Business.query.filter(Business.business_id == id).first():
        fav_businesses = g.user.favorite_business
        for each_fav_business in fav_businesses:
            if each_fav_business.business_id == id:
                business_favorited = True           
    else:
        business_favorited = False

    my_lat = 37.7749
    my_long = 122.4194

    url = API_BASE_URL + '/businesses/' + id

    req = requests.get(url, headers = headers)
    business = json.loads(req.text)

    # get business's review    
    url_review = API_BASE_URL + '/businesses/' + id + '/reviews'
    req_review = requests.get(url_review, headers = headers)
    reviews = json.loads(req_review.text).get('reviews', None)
    # get location of the business
    latitude = business['coordinates']['latitude']
    longitude = business['coordinates']['longitude']
    location = [latitude, longitude]
    # add Week array used for daily open hours 
    week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    category = business['categories'][0]['title']

    return render_template('business/detail.html', business = business, reviews = reviews, my_lat = my_lat, my_long = my_long, favorited = business_favorited, week = week, category = category, city = session['location'])

# =============================================================================================================================

# Add a Favoriate Business to User
@app.route('/users/favorites/<business_id>')
def add_favorite(business_id):
    """Add favorite business to the current user"""
    if not g.user:
        flash("Please log in first.", "danger")
        return redirect('/signin')

    # get business's name
    url = API_BASE_URL + '/businesses/' + business_id
    req = requests.get(url, headers = headers)
    business = json.loads(req.text)
    business_name = business.get('name', None)

    # check if the item is on the Business models
    # if Business.query.all() == [] or not Business.query.filter(Business.business_id == business_id).first():
    # get id for user's favorite businesses
    fav_business_ids = []
    for each_fav_business in g.user.favorite_business:
        fav_business_ids.append(each_fav_business.business_id)

    # check if current id is in favourite businesses already
    if business_id not in fav_business_ids:        
        new_business = Business(business_id = business_id, business_name = business_name)
        g.user.favorite_business.append(new_business)
        db.session.commit()

    return redirect('/users/' + g.user.username)

# =============================================================================================================================

# Unfavorite a business of user's 
@app.route('/users/unfavorite/<business_id>')
def delete_item(business_id):
    """Delete a favorite business from the current user"""
    if not g.user:
        flash("Please log in first.", "danger")
        return redirect('/signin')

    for each_business in g.user.favorite_business:
        if each_business.business_id == business_id:
            g.user.favorite_business.remove(each_business)
            db.session.commit()

    return redirect('/users/' + g.user.username)    

# =============================================================================================================================

# API used to get current location 
@app.route('/api/location', methods=['POST'])
def current_location():
    latitude = request.json["latitude"]
    longitude = request.json["longitude"]
    city = request.json["city"]
    
    print(latitude, longitude, city)
    session['current_latitude'] = latitude
    session['current_longitude'] = longitude
    session['current_city'] = city

    print(session['current_latitude'], session['current_longitude'], session['current_city'])
    
    return redirect('/')

# =============================================================================================================================
