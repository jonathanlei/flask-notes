from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


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


class AddNoteForm(FlaskForm):
    """ form for adding notes"""
    title = StringField("Title",
                        validators=[InputRequired(), Length(max=100)])
    content = TextAreaField("Content",
                            validators=[InputRequired()])


class EditNoteForm(FlaskForm):
    """ form for editing notes"""
    title = StringField("Title",
                        validators=[InputRequired(), Length(max=100)])
    content = TextAreaField("Content",
                            validators=[InputRequired()])