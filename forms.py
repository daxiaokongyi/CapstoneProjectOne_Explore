from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, FileField, PasswordField
from wtforms.validators import InputRequired, Optional, URL, NumberRange

class SignUpForm(FlaskForm):
    username = StringField("User Name", validators = [InputRequired(message="User name is required.")])
    password = PasswordField("Password", validators = [InputRequired(message="Password is required.")])
    email = StringField("Email", validators = [InputRequired(message="Email is required.")])
    gender = SelectField('Gender', choices = [('male', 'Male'), ('female', 'Female')])
    age = IntegerField("Age", validators = [NumberRange(min=0, max=110), Optional()])
    photo_url = StringField("Photo Link", validators = [Optional(), URL()])
    file = FileField('File')

class SignInForm(FlaskForm):
    username = StringField("User Name", validators = [InputRequired(message="User name is required.")])
    password = PasswordField("Password", validators = [InputRequired(message="Password is required.")])

class DeleteForm(FlaskForm):
    """Delete Form"""