from flask import Flask

app = Flask(__name__)

from blog import routes, models