from flask import Flask
from flask_app import init_app
from flask_cors import CORS

app = Flask(__name__)
init_app(app)
CORS(app)
