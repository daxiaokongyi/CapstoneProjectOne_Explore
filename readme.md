# Capstone One Project Proposal:

## What goal will your website be designed to achieve?
The goal of this project is to create a website that allows users to explore food or drinks based on their eating style. For example, people will get Japanese food in either their cities or a city which is put on the search bar if they search Japanese food. 
This app can give the best food suggestion if people don’t know what to eat or want to try something new. 
This application will also include restaurant’s information, such as contact number, address, reviews, open hours, map and so on. 

## What kind of users will visit your site? In other words, what is the demographic of your users?
The target users of this application are within a wide range. People at any age as long as they would like to try something new and enjoy eating, drinking, and exploring. For example, users could be: 
Travellers who would like to try the best local food. 
Students who would like to try all of the best restaurants around their campus
People who out of work and enjoy a time with friends
People who just want to find a quiet coffee shop to study
Foodies

## What data do you plan on using? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain.
Data could be:
Food category
Restaurant’s name, phone number, open hours, reviews, ratings, and pictures
Recommended restaurant based on the food categories
Recommended restaurant shown on the home page based on user’s eating style
Google map api used to guide user to the restaurant

# Outline my approach to creating my project

a. What does my database schema look like? 
Restaurant: sorted by distance at ascending order, each restaurant includes name, photo, phone numbers, open hours, rating, reviews, menu, website, map and so on 
 User: name, username, password, profile photo, age, email, and favorite food/drink items

b. What kinds of issues might my run into with my API? 
	No photo of restaurant available - use a default photo
	No review of rstaurant available - hide reviews block

c. Is there any sensitive information I need to secure? 
App key 
User’s password (It will be hashed)

d. What functionality will my app include? 
Search restaurant based on category and city on the search bar
Add favorite restaurant
User authentication and authorization
Get direction through google map
Get restaurants based on mile range (around user’s geo), rating, and personal recommendation
Able to sign up, sign in, edit, and delete a user
	 
e. What will the user flow look like? 

Register
Login
Browse restaurant list
Find more detail about the business
Add/removed a favorite business
Logout

Also this web application would like to ask for a permission to get user's location in order to recommond related business items nearby accurately 

f. What features make my site more than CRUD? Do you have any stretch goals?

Enable restaurant recommendation. 
Let people chat online on the future version

g. Links

Github Link: https://github.com/daxiaokongyi/CapstoneProjectOne_Foodie
API links: https://www.yelp.com/developers?ref=apilist.fun

# Technology Stack
## Front End:
JavaScript, HTML, CSS, BootStrap
## Back End:
Python, Flask
## Database:
PostgreSQL
## Testing:
Jest