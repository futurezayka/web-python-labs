from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, IntegerField, SelectField, PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email

class AuthorCreationForm(FlaskForm):
    name = StringField("Name: ")
    pseudonym = StringField("Pseudonym: ")
    submit = SubmitField("Submit")

class BookCreationForm(FlaskForm):
    name = StringField("Name: ")
    page = IntegerField("Total pages: ")
    year = IntegerField("Year: ")
    genres = SelectMultipleField('Genres: ', coerce=int)
    author_id = SelectField('Author: ', coerce=int)
    submit = SubmitField("Submit")

class GenreCreationForm(FlaskForm):
    name = StringField("Name: ")
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField()

class RegisterForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    username = StringField("Username: ", validators=[DataRequired()])
    email = EmailField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField()