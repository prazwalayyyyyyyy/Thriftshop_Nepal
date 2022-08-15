from wsgiref.validate import validator

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (BooleanField, PasswordField, IntegerField, StringField, SubmitField,
                     validators)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    user_type = StringField('user_type', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class GoodsForm(FlaskForm):
    photo = FileField('Upload Photo')
    name = StringField('Name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    descripton = StringField('Description')
    submit = SubmitField('Submit')

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    user_type = StringField('User Role', validators=[DataRequired()])
    submit = SubmitField('Edit Users')