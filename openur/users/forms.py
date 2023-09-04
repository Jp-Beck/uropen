# users/forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import current_user
from openur.models import User


class RegistrationForm(FlaskForm):
    # Fields for registration
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])  # Minimum length added
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Custom validators
    def validate_username(self, username):
        # Check if username already exists
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different username.')
    
    def validate_email(self, email):
        # Check if email already exists
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Please choose a different email.')

class UpdateAccountForm(FlaskForm):
    # Fields for updating account
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])   
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) 
    submit = SubmitField('Update')

    # Custom validators
    def validate_username(self, username):
        # Check if username already exists
        if username.data != current_user.username: # if the username is different from the current username
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists. Please choose a different username.')
    
    def validate_email(self, email):
        # Check if email already exists
        if email.data != current_user.email: # if the email is different from the current email
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists. Please choose a different email.')


class LoginForm(FlaskForm):
    # Fields for logging in
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ResetRequestForm(FlaskForm):
    # Fields for requesting a password reset
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    # Custom validators
    def validate_email(self, email):
        # Check if email already exists
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account assosiated with that email. Please register first!')
        

class ResetPasswordForm(FlaskForm):
    # Fields for resetting password
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])  # Minimum length added
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')