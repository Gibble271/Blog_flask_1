from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user
from blog import app, db
from blog.forms import RegistrationForm, LoginForm
from blog.models import User

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()

@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html', title='About')


# In register, be sure to add the send email to new user for verification.
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email = form.email.data, username = form.username.data, first_name=form.first_name.data,
                        last_name = form.last_name.data)
        new_user.set_password_hash(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'User {form.username.data} has been created!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user.get_password_hash(form.password.data) and user:
            login_user(user, remember=form.remember_me.data)
            flash(f'User {form.username.data} has logged in successfully')
            return redirect(url_for('about'))
        else:
            flash('Either the username or password is incorrect. Please try again.')
    return render_template('login.html', title='Login', form = form)

@app.route('/logout')
def logout():
    logout_user()
    flash(f'You have successfully logged out')
    return redirect(url_for('about'))