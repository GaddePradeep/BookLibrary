from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField,IntegerField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
  first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
  last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
  email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
  submit = SubmitField('Sign up')

class LoginForm(Form):
  email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
  submit = SubmitField("Sign in")


class AddBookForm(Form):
  book_name = StringField('Book name', validators=[DataRequired("Please enter the book name.")])
  contributor_name = StringField('Contributor name', validators=[DataRequired("Please enter the contributor name.")])
  description = StringField('Description', validators=[DataRequired("Please enter a description.")])
  setcount = IntegerField('Set Count', validators=[DataRequired("Please enter the book count in the set.")])
  email = StringField('Email', validators=[DataRequired("Please enter contributor email address."), Email("Please enter contributor email address.")])
  submit = SubmitField('Add Book')
