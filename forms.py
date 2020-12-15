from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Optional, Email, URL, AnyOf, Length


class RegisterUserForm(FlaskForm):
    """ The registering form for new user"""
    username = StringField("User Name",
                           validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password",
                             validators=[InputRequired()])
    email = StringField("Email",
                        validators=[InputRequired(), Email(), Length(max=50)])
    first_name = StringField("First Name",
                             validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name",
                            validators=[InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """ for User login, takes username and password """
    username = StringField("User Name",
                           validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password",
                             validators=[InputRequired()])