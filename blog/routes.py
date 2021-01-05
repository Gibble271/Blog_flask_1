from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from blog import app, db
from blog.forms import RegistrationForm, LoginForm, CreateCommunityForm, CreateDiscussionForm
from blog.models import User, Community, Discussion
from sqlalchemy import desc

def saveToDatabase(newData):
    db.session.add(newData)
    db.session.commit()

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()

@app.route('/')
@app.route('/about')
def about():
    communities = Community.query.filter_by().all()
    return render_template('about.html', title='About', communities=communities)

@login_required
@app.route('/create/community', methods=['POST', 'GET'])
def createCommunity():
    form = CreateCommunityForm()
    if form.validate_on_submit():
        newCommunityInfo = Community(name=form.name.data, about=form.about.data, founder_id=current_user.id)
        saveToDatabase(newCommunityInfo)
        flash(f'You have successfully {form.name.data}')
        return redirect(url_for('about'))
    return render_template('create_Community.html', title='Create Community', form=form)

#important chain method to remember that will help with sorting.
#Discussion.query.filter_by(community_id=community_id).order_by(Discussion.timestamp.desc()).all()
@app.route('/view/community/<community_id>', methods=['GET'])
def viewCommunity(community_id):
    community_name= Community.query.get(community_id).name
    discussions = Discussion.query.filter_by(community_id=community_id).order_by(Discussion.timestamp.desc()).all()
    return render_template('community_Page.html', title=community_name, discussions=discussions, id_of_community=community_id)

@login_required
@app.route('/create/<community_id>/discussion', methods=['GET', 'POST'])
def createDiscussion(community_id):
    form = CreateDiscussionForm()
    if form.validate_on_submit():
        newDiscussion = Discussion(title=form.title.data, body=form.body.data, user_id=current_user.id,
                                    community_id=community_id)
        saveToDatabase(newDiscussion)
        flash(f'You have successfully uploaded discussion {form.title.data}')
        return redirect(url_for('viewCommunity', community_id=community_id))
    return render_template('create_Discussion.html', form=form, title='Create Discussion')

@login_required
@app.route('/view/discussion/<discussion_id>', methods=['GET'])
def viewDiscussion(discussion_id):
    discussion = Discussion.query.get(discussion_id)
    return render_template('discussion_page.html', title="View Discussion", discussion = discussion)

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

# In register, be sure to add the send email to new user for verification.
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email = form.email.data, username = form.username.data, first_name=form.first_name.data,
                        last_name = form.last_name.data)
        new_user.set_password_hash(form.password.data)
        saveToDatabase(new_user)
        flash(f'User {form.username.data} has been created!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form = form)
