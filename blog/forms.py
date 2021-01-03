from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Length, Email
from blog.models import User, Community


class CreateCommunityForm(FlaskForm):
    name = StringField('Name of Community:', validators=[DataRequired()])
    about = StringField('About the Community:')
    submit = SubmitField('Create Community')

    def validate_name(self, name):
        name = Community.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError(f'The name {name.data} has already been taken. Please use a different one.')

class CreateDiscussionForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    body = StringField('Discuss:')
    submit = SubmitField('Create Discussion')

class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Email(), DataRequired()])
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username has already been taken. Please use a different one.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email has already been taken. Please use a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me:')
    submit = SubmitField('Sign In')