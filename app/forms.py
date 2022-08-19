from wsgiref.validate import validator

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (BooleanField, PasswordField, IntegerField, StringField, SubmitField, SelectField
                     )
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.widgets.core import html_params
from markupsafe import Markup
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
    condition_choices = ["New", "Good", "Used Many times"]
    category_choices = ["Male", "Female"]

    photo = FileField('Upload Photo')
    name = StringField('Name', validators=[DataRequired()])
    buy_price = IntegerField('Price', validators=[DataRequired()])
    condition = SelectField('condition', choices=condition_choices, validators=[DataRequired()])
    category = SelectField('category', choices=category_choices, validators=[DataRequired()])
    submit = SubmitField('Submit')

    # def __call__(self, field, **kwargs):
    #     breakpoint()
    #     kwargs.setdefault("id", field.id)
    #     if self.multiple:
    #         kwargs["multiple"] = True
    #     flags = getattr(field, "flags", {})
    #     for k in dir(flags):
    #         if k in self.validation_attrs and k not in kwargs:
    #             kwargs[k] = getattr(flags, k)
    #     html = ["<select class='form-select' aria-label=\"Default select example\"%s>" % html_params(name=field.name, **kwargs)]
    #     if field.has_groups():
    #         for group, choices in field.iter_groups():
    #             html.append("<optgroup %s>" % html_params(label=group))
    #             for val, label, selected in choices:
    #                 html.append(self.render_option(val, label, selected))
    #             html.append("</optgroup>")
    #     else:
    #         for val, label, selected in field.iter_choices():
    #             html.append(self.render_option(val, label, selected))
    #     html.append("</select>")
    #     return Markup("".join(html))

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    user_type = StringField('User Role', validators=[DataRequired()])
    submit = SubmitField('Edit Users')