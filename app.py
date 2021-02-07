from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_uploads import configure_uploads, IMAGES, UploadSet
from forms import SignInForm, SignUpForm, DeleteForm
from models import db, User, connect_db
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import Unauthorized, Forbidden
from secrets import API_SECRET_KEY
import requests
import json
import folium
import geocoder

API_BASE_URL = "https://api.yelp.com/v3"
headers = {'Authorization':'Bearer %s' % API_SECRET_KEY}

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

@app.route('/')
def home():
    """Home Page"""
    return render_template("base.html")

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    """User Register Page"""
    form = SignUpForm()
    if form.validate_on_submit():
        # data = {k: v for k,v in form.data.items() if k != 'csrf_token' and k != 'file'}
        # new_user = User(**data)

        username = form.username.data
        password = form.password.data
        email = form.email.data
        gender = form.gender.data
        age = form.age.data
        photo_url = ""

        new_user = User.signup(username, password, email, age, gender, photo_url)

        if form.file.data.filename != '':
            filename = images.save(form.file.data)
            # if filename != None:
            new_user.photo_url = f'static/{filename}'
        else:
            new_user.photo_url = User.image_url(new_user)

        db.session.add(new_user)
        db.session.commit()

        # keep user in the session
        session['username'] = new_user.username
        flash(f'Welcome {new_user.username}! Enjoy your foodie jouney', 'success')
        return redirect(f'/users/{new_user.username}')
    else:    
        return render_template("signup.html", form = form)

@app.route('/signin', methods = ['GET', 'POST'])
def sign_in():
    """Sign In Page"""
    form = SignInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Incorrect username or password. Please try again']

    return render_template('signin.html', form = form)

@app.route('/users/<username>')
def detail_user(username):
    """Show the detail of the user"""
    if "username" not in session:
        raise Unauthorized()

    if username != session['username']:
        raise Forbidden()

    form = DeleteForm()

    user = User.query.get(session['username'])

    return redirect('/')

@app.route('/logout')
def log_out():
    """Log user out"""
    session.pop('username')
    flash("Logged out successfully", "success")
    return redirect('/')

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

@app.route('/categories/<alias>')
def get_alias(alias):
    url = f'{API_BASE_URL}/businesses/search' 
    location = session['location']
    params = {'term':alias, 'location':location}
    req = requests.get(url, params = params, headers = headers)
    parsed = json.loads(req.text)   
    businesses = parsed['businesses']
    return render_template('items.html', businesses = businesses)

@app.route('/foodies/details/<id>')
def get_detail(id):
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
    print('\n')

    latitude = business['coordinates']['latitude']
    longitude = business['coordinates']['longitude']
    location = [latitude, longitude]

    return render_template('detail.html', business = business, my_lat = my_lat, my_long = my_long)



    

