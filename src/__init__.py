# src/__init__.py
from flask import Flask
from src.config import default

app = Flask(__name__, instance_path='/vagrant/SpeechApplication/src/instance', instance_relative_config=True)

# Load the default configuration
# app.config.from_object('config.default')

# Load the configuration from the instance folder
# app.config.from_pyfile('config.py')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
#application.config.from_envvar('APP_CONFIG_FILE')

"""
@app.route('/')
def index():
    return '欢迎'
"""

