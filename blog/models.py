from blog import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    #variables
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), nullable=False, unique=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128))

    #relationship

    #methods
    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)
    
    def get_password_hash(self, password):
        return check_password_hash(self.password_hash, password)
