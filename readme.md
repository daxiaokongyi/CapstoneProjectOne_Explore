# Capstone One Project Proposal:

## What goal will my website be designed to achieve?
The goal of this project is to create a website that allows users to explore food, drinks, activities, or events based on around their locations. They also can get research results from other cities as well. 
This app can also give you the best food/activity suggestions based on your search history. 
This application will also include restaurant’s information, such as clickable contact number and address, reviews, open hours, map and so on. 

## What kind of users will visit my site? In other words, what is the demographic of my users?
The target users of this application are within a wide range. People at any age as long as they would like to try something new and enjoy eating, drinking, and exploring. For example, users could be: 
Travellers who would like to try the best local food. 
Students who would like to try all of the best restaurants around their campus
People who out of work and enjoy a time with friends
People who just want to find a quiet coffee shop to study
Foodies

## What data do my plan on using? I may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain.
Data could be:
Category of business, business’s name, phone number, open hours, reviews, ratings, and pictures
Map API

# Outline my approach to creating my project

a. What does my database schema look like? 
Business: sorted by distance at ascending order, each business includes name, photo, phone numbers, open hours, rating, reviews, menu, website, map and so on 

User: name, username, password, profile photo, age, email, and favorite food/drink/activity items

b. What kinds of issues might my run into with my API? 
	No photo of restaurant available - use a default photo
	No review of rstaurant available - hide reviews block
	No permission of user's location - set a default business and location
	No business can be shown in a specific area - create 404 html page

c. Is there any sensitive information I need to secure? 
	App key 
	User’s password (It will be hashed)

d. What functionality will my app include? 
Search business based on category and city on the search bar
Add/Remove favorite business
User authentication and authorization
Get direction through google map
Get restaurants based on mile range (around user’s geo), rating, and personal recommendation
Able to sign up, sign in, edit, and delete a user
	 
e. What will the user flow look like? 

	Register
	Login
	Browse business list
	Find more detail about the business
	Add/removed a favorite business
	Logout

	Also this web application would like to ask for a permission to get user's location in order to recommond related business items nearby accurately 

f. What features make my site more than CRUD? Do you have any stretch goals?

	Let people chat online
	Let user be able to leave a comment or follow each other

g. Links

Github Link: https://github.com/daxiaokongyi/CapstoneProjectOne_Foodie
API links: https://www.yelp.com/developers?ref=apilist.fun
Map API: leaflet

# Technology Stack
## Front End:
JavaScript, HTML, CSS, BootStrap
## Back End:
Python, Flask
## Database:
PostgreSQL
## Testing:
Jest

# Installation
## Get API Key
Get a free API Key from Yelp at https://www.yelp.com/developers
## Clone
Clone the repo from https://github.com/daxiaokongyi/CapstoneProjectOne_Explore
## Install the packages
$ pip install -r requirements.txt
## Run the App
flask run 

# Testing
python -m unittest test_app.py
