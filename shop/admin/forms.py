from wtforms import Form, BooleanField, StringField, IntegerField, TextAreaField, PasswordField, validators
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileAllowed, FileField, FileRequired


class RegistrationForm(Form):
    first_name = StringField('First Name', [validators.Length(min=2, max=25)])
    last_name = StringField('Last Name', [validators.Length(min=2, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35),validators.Email()])
    password = PasswordField('New Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35),validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])


class UploadForm(Form):
    #upload picture, photo name, photo description, photo price
    item_name = StringField('Photo Name', [validators.DataRequired()])
    item_desc = TextAreaField('Photo Description', [validators.DataRequired()])
    item_price = IntegerField('Price', [validators.DataRequired()])
    item_file = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
