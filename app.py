from flask import Flask, render_template, redirect, flash, session, request, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_uploads import configure_uploads, IMAGES, UploadSet
from sqlalchemy.exc import IntegrityError
from forms import SignInForm, SignUpForm, EditForm, DeleteForm
from models import db, User, Business, FavoriteBusiness, connect_db
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import Unauthorized, Forbidden
from secrets import API_SECRET_KEY
import requests
import json

API_BASE_URL = "https://api.yelp.com/v3"
headers = {'Authorization':'Bearer %s' % API_SECRET_KEY}
CURR_USER_KEY = 'curr_user'

app = Flask(__name__)
app.debug = False

app.config['SECRET_KEY'] = 'secretkeyissecretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///foods'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['UPLOADED_IMAGES_DEST'] = 'static'

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

toolbar = DebugToolbarExtension(app)

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
            url = API_BASE_URL + '/businesses/{business.business_id}'

            req = requests.get(url, headers = headers)
            business = json.loads(req.text)
            business_array.append(business)

        # get the latest alias
        if len(business_array) >= 1:
            last_business = business_array[len(business_array) - 1]
            current_category = last_business.get('categories', None)
            current_title = list(current_category[0].get('title', None).split(' '))
            title = current_title[0]

        if (title):
            return redirect('/categories/' + title)
        else:
            default_city = session["current_city"]
            return render_template('homepage/defaultWithCity.html', city = default_city)
    else:
        if not session.get('current_latitude') and not session.get('current_longitude') and not session.get('current_city'):
            return render_template('users/default.html');
        else:
            default_lat = session['current_latitude']
            default_long = session['current_longitude']
            default_city = session['current_city']
            # location = str(default_lat) + ',' + str(default_long) + ',' + default_city

            return render_template('homepage/defaultWithCity.html', city = default_city)

# ====================================================================================================================================

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
            # flash(f'Welcome {new_user.username}! Enjoy your foodie jouney', 'success')
            flash('Welcome ' + new_user.username + '! Enjoy your foodie jouney', 'success')

        except IntegrityError:
            flash("User name or Email was already taken", "danger")
            return render_template("users/signup.html", form = form)

        # keep user in the session
        do_login(new_user)
        # return redirect(f'/users/{new_user.username}')
        return redirect('/users/' + new_user.username)
    else:    
        return render_template("users/signup.html", form = form)

# ====================================================================================================================================

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
                # flash(f'Thank you {user.username}! Your profile has been updated', 'success')
                flash('Thank you ' + user.username + '! Your profile has been updated', 'success')
                # return redirect(f'/users/{user.username}')
                return redirect('/users/' + user.username)
                        
            flash("Wrong password, please try again.", "danger")
            return render_template("users/edit.html", form = form)

        except IndentationError:
            flash("Unauthorized.", "danger")
            return render_template("users/edit.html", form = form)

        # keep user in the session
        do_login(user)
        # return redirect(f'/users/{user.username}')
        return redirect('/users/' + user.username)
    else:    
        return render_template("users/edit.html", form = form)

# ====================================================================================================================================

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
            # flash(f"Welcome back, {user.username}!", "success")
            flash('Welcome back, ' + user.username + '!', "success")
            # return redirect(f'/users/{user.username}')
            return redirect('/users/' + user.username)
        else:
            form.username.errors = ['Incorrect username or password. Please try again']

    return render_template('users/signin.html', form = form)

@app.route('/logout')
def log_out():
    """Log user out"""
    do_logout()
    flash("Logged out successfully", "success")
    return redirect('/')

# ====================================================================================================================================

# User's info 
@app.route('/users/<username>')
def detail_user(username):
    """Show the detail of the user"""
    if CURR_USER_KEY not in session:
        raise Unauthorized()

    if username != session[CURR_USER_KEY]:
        raise Forbidden()

    # form = DeleteForm()

    user = User.query.get(session[CURR_USER_KEY])
    
    if g.user:
        businesses_favorited = g.user.favorite_business
    else:
        businesses_favorited = None

    return render_template('users/info.html', user = user, businesses = businesses_favorited)

# ====================================================================================================================================

# Delete User 
@app.route('/users/delete', methods=['POST'])
def delete_user():
    """Delete user"""
    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect('/')

    do_logout()
    db.session.delete(g.user)
    db.session.commit()

    return redirect('/')

# ====================================================================================================================================

# Add a Favoriate Business to User
@app.route('/users/favorites/<business_id>')
def add_favorite(business_id):
    """Add favorite business to the current user"""
    if not g.user:
        flash("Please log in first.", "danger")
        return redirect('/signin')

    # get business's name
    # url = f'{API_BASE_URL}/businesses/{business_id}'
    url = API_BASE_URL + '/businesses/' + business_id
    req = requests.get(url, headers = headers)
    business = json.loads(req.text)
    business_name = business.get('name', None)

    # check if the item is on the Business models
    if Business.query.all() == [] or not Business.query.filter(Business.business_id == business_id).first():
        new_business = Business(business_id = business_id, business_name = business_name)
        g.user.favorite_business.append(new_business)
        db.session.commit()

    # return redirect(f"/users/{g.user.username}")
    return redirect('/users/' + g.user.username)

# ====================================================================================================================================

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
        location = 'San Francisco'
        session['location'] = location

    params = {'term':term, 'location':location}
    req = requests.get(url , params = params, headers = headers)

    # check if res.status code is 400
    if req.status_code == 400:
        return render_template('404.html')

    parsed = json.loads(req.text)
    businesses = parsed['businesses']

    # check if businesses is a empty array
    if businesses == []:
        return render_template('404.html')
    else: 
        return render_template('business/items.html', businesses = businesses)

# ====================================================================================================================================

# Search for a specific categories 
@app.route('/categories/<title>')
def get_alias(title):
    # default latitude and longitude
    url = API_BASE_URL + '/businesses/search' 
        
    if 'current_latitude' not in session and 'current_longitude' not in session:
        # set a default latitude and longitude
        my_lat = 37.7749
        my_long = -122.4194
        location = [my_lat, my_long]    
    else:
        # get current location
        current_lat = session['current_latitude']
        current_log = session['current_longitude']
        location = str(current_lat) + ', ' + str(current_log)
    
    params = {'term':title, 'location': location}
    req = requests.get(url, params = params, headers = headers)
    parsed = json.loads(req.text)       
    businesses = parsed['businesses']

    session['category'] = title
    return render_template('business/items.html', businesses = businesses)

# ====================================================================================================================================

# Get business's detail 
@app.route('/foodies/details/<id>')
def get_detail(id):
    business_favorited = False
    
    # check if this business marked as favorited or not
    if Business.query.all() != [] and Business.query.filter(Business.business_id == id).first():
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

    return render_template('business/detail.html', business = business, reviews = reviews ,my_lat = my_lat, my_long = my_long, favorited = business_favorited, week = week)

# ====================================================================================================================================

# Unfavorite a business of user's 
@app.route('/users/unfavorite/<business_id>')
def delete_item(business_id):
    """Delete a favorite business from the current user"""
    if not g.user:
        flash("Please log in first.", "danger")
        return redirect('/signin')

    current_favorite = Business.query.filter(Business.business_id == business_id).first()
    g.user.favorite_business.remove(current_favorite)

    db.session.commit()

    return redirect('/users/' + g.user.username)    

# ====================================================================================================================================

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

# ====================================================================================================================================


