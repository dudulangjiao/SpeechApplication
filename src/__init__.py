# src/__init__.py
from flask import Flask
#import src.config.default

app = Flask(__name__, template_folder='/vagrant/SpeechApplication/src/application/templates',
            static_folder='/src/application/static',
            instance_path='/vagrant/SpeechApplication/src/instance', instance_relative_config=True)

# Load the default configuration
app.config.from_object('src.config.development')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
#application.config.from_envvar('APP_CONFIG_FILE')

# 必须引入视图函数
import src.application.views

# set the secret key.  keep this really secret:
app.secret_key = app.config['SECRET_KEY']

app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0