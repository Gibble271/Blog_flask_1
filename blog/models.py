from blog import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Community(db.Model):
    #variables
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    about = db.Column(db.String(120))
    
    #relationships
    founder_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class User(db.Model, UserMixin):
    #variables
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), nullable=False, unique=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128))

    #relationship
    createdCommunities = db.relationship('Community', backref='founder', lazy=True)

    #methods
    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)
    
    def get_password_hash(self, password):
        return check_password_hash(self.password_hash, password)
