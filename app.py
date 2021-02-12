from flask import Flask, render_template, redirect, flash, session, request, g
from flask_debugtoolbar import DebugToolbarExtension
from flask_uploads import configure_uploads, IMAGES, UploadSet
from forms import SignInForm, SignUpForm, EditForm, DeleteForm
from models import db, User, Business, FavoriteBusiness, connect_db
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import Unauthorized, Forbidden
from secrets import API_SECRET_KEY
import requests
import json
import geocoder

API_BASE_URL = "https://api.yelp.com/v3"
headers = {'Authorization':'Bearer %s' % API_SECRET_KEY}
CURR_USER_KEY = 'curr_user'

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkeyissecretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///food'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['UPLOADED_IMAGES_DEST'] = 'static'

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

debug = DebugToolbarExtension(app)

connect_db(app)

# db.drop_all()
# db.create_all()

# ================================================================================================
# Home Page

@app.route('/')
def home():
    """Home Page"""
    business_array = []
    current_alias = None

    # check if user signs in
    if g.user:
        businesses = g.user.favorite_business

        for business in businesses: 
            url = f'{API_BASE_URL}/businesses/{business.business_id}'
            req = requests.get(url, headers = headers)
            business = json.loads(req.text)
            # print(business)
            business_array.append(business)

        # print(business_array)
        # get the latest alias
        if len(business_array) >= 1:
            last_business = business_array[len(business_array) - 1]
            current_categore = last_business.get('categories', None)
            current_title = list(current_categore[0].get('title', None).split(' '))
            title = current_title[0]
    else:
        return render_template('users/default.html')

    # return render_template("users/home.html", business_array = business_array)
    if {title}:
        return redirect(f'/categories/{title}')
    else:
        return redirect('/')
# ================================================================================================
# User signup login logout

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

            if form.file.data.filename != '':
                filename = images.save(form.file.data)
                # if filename != None:
                new_user.photo_url = f'/static/{filename}'
            else:
                new_user.photo_url = User.image_url(new_user)

            db.session.add(new_user)            
            db.session.commit()
            flash(f'Welcome {new_user.username}! Enjoy your foodie jouney', 'success')

        except IndentationError:
            flash("User name already taken", "danger")
            return render_template("users/signup.html", form = form)

        # keep user in the session
        do_login(new_user)
        return redirect(f'/users/{new_user.username}')
    else:    
        return render_template("users/signup.html", form = form)

@app.route('/edit', methods=['GET', 'POST'])
def edit_profile():
    """Update profile for the current user"""
    if not g.user:
        flash("Access unauthorized.", "danger")

    user = g.user
    form = EditForm(obj = user)

    if form.validate_on_submit():
        try:
            if User.authenticate(user.username, form.password.data):
                user.email = form.email.data
                user.gender = form.gender.data
                user.age = form.age.data
                user.photo_url = form.photo_url.data

                if form.file.data.filename != '':
                    filename = images.save(form.file.data)
                    # if filename != None:
                    user.photo_url = f'/static/{filename}'
                else:
                    user.photo_url = User.image_url(user)

                db.session.commit()
                flash(f'Thank you {user.username}! Your profile has been updated', 'success')
                return redirect(f'/users/{user.username}')
                        
            flash("Wrong password, please try again.", "danger")
            return render_template("users/edit.html", form = form)

        except IndentationError:
            flash("Unauthorized.", "danger")
            return render_template("users/edit.html", form = form)

        # keep user in the session
        do_login(user)
        return redirect(f'/users/{user.username}')
    else:    
        return render_template("users/edit.html", form = form)

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
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Incorrect username or password. Please try again']

    return render_template('users/signin.html', form = form)

@app.route('/logout')
def log_out():
    """Log user out"""
    do_logout()
    flash("Logged out successfully", "success")
    return redirect('/')

# ================================================================================================
# user's info
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

@app.route('/users/delete', methods=['POST'])
def delete_user():
    """Delete user"""
    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect('/')

    do_logout()
    db.session.delete(g.user)
    db.session.commit()

    return redirect('/signup')

@app.route('/users/favorites/<business_id>')
def add_favorite(business_id):
    """Add favorite business to the current user"""
    if not g.user:
        flash("Please log in first.", "danger")
        return redirect('/signin')

    # get business's name
    url = f'{API_BASE_URL}/businesses/{business_id}'
    req = requests.get(url, headers = headers)
    business = json.loads(req.text)
    business_name = business.get('name', None)

    # check if the item is on the Business models
    if Business.query.all() == [] or not Business.query.filter(Business.business_id == business_id).first():
        new_business = Business(business_id = business_id, business_name = business_name)
        g.user.favorite_business.append(new_business)
        db.session.commit()

    return redirect(f"/users/{g.user.username}")

@app.route('/businesses/search')
def businesses_search():
    url = f'{API_BASE_URL}/businesses/search' 
    term = request.args['term']
    location = request.args['location']
    session['location'] = location
    params = {'term':term, 'location':location}
    req = requests.get(url , params = params, headers = headers)
    parsed = json.loads(req.text)
    businesses = parsed['businesses']

    # for business in businesses:
    #     print('Name:', business['name'])
    #     print('Rating:', business['rating'])
    #     print('Address:', business['location']['display_address'])
    #     print('Phone:', business['display_phone'])
    #     print('img_url:', business['image_url'])
    #     print('Open?:',business['is_closed'])
    #     print('Distance:', business['distance'])
    #     print('Coordinates:', business['coordinates'])
    #     print('Transactions:', business['transactions'])
    #     print(business['transactions'] == [])
    #     print('Price:', business.get('price', None))
    #     print(business.get('price',None) == None)
    #     print('Categories:', business['categories'])
    #     print('\n')
    return render_template('items.html', businesses = businesses)
 
@app.route('/categories/<title>')
def get_alias(title):
    # get user's location
    my_geo = geocoder.ip('me')
    print(my_geo.latlng[0])
    my_lat = my_geo.latlng[0]
    print(my_geo.latlng[1])
    my_long = my_geo.latlng[1]    

    url = f'{API_BASE_URL}/businesses/search' 
        
    if 'location' not in session:
        location = [my_lat, my_long]    
    else:
        location = session['location']
    
    params = {'term':title, 'location':str(location)}
    req = requests.get(url, params = params, headers = headers)
    parsed = json.loads(req.text)       
    
    businesses = parsed['businesses']
    return render_template('items.html', businesses = businesses)

@app.route('/foodies/details/<id>')
def get_detail(id):
    business_favorited = False
    
    if Business.query.all() != [] and Business.query.filter(Business.business_id == id).first():
        business_favorited = True         
    else:    
        business_favorited = False

    my_geo = geocoder.ip('me')
    print(my_geo.latlng[0])
    my_lat = my_geo.latlng[0]
    print(my_geo.latlng[1])
    my_long = my_geo.latlng[1]

    url = f'{API_BASE_URL}/businesses/{id}'
    req = requests.get(url, headers = headers)
    business = json.loads(req.text)
    print(business)
    print('Name:', business['name'])
    print('Rating:', business['rating'])
    print('Address:', business['location']['display_address'])
    print('Phone:', business['display_phone'])
    print('img_url:', business['image_url'])
    print('Open?:',business['is_closed'])
    print('Coordinates:', business['coordinates'])
    print('Transactions:', business['transactions'])
    print(business['transactions'] == [])
    print('Price:', business.get('price', None))
    print(business.get('price',None) == None)
    print('Categories:', business['categories'])
    if business.get('hours', None):
        print('Hours:', business['hours'][0])
    if business.get('special_hours', None):
        print('Special Hours:', business['special_hours'][0])
    print('\n')

    # get business's review    
    url_review = f'{API_BASE_URL}/businesses/{id}/reviews'
    req_review = requests.get(url_review, headers = headers)
    reviews = json.loads(req_review.text).get('reviews',None)

    latitude = business['coordinates']['latitude']
    longitude = business['coordinates']['longitude']
    location = [latitude, longitude]

    return render_template('detail.html', business = business, reviews = reviews ,my_lat = my_lat, my_long = my_long, favorited = business_favorited)

@app.route('/users/unfavorite/<business_id>')
def delete_item(business_id):
    """Delete a favorite business from the current user"""
    if not g.user:
        flash("Please log in first.", "danger")
        return redirect('/signin')

    current_favorite = Business.query.filter(Business.business_id == business_id).first()
    g.user.favorite_business.remove(current_favorite)

    db.session.commit()

    return redirect(f"/users/{g.user.username}")    


    

