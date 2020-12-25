from flask import render_template
from blog import app

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')