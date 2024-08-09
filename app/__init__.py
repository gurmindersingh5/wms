import os

from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth

app = Flask(__name__, static_url_path='/app/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = os.environ.get('super_secret')

# config session in app
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False  # Sessions won't expire on browser close
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)  # Session timeout

# Configure JWT settings
app.config['JWT_SECRET_KEY'] = os.environ.get('jwt_token')  # Replace with your secret key
jwt = JWTManager(app)

Session(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.login_view = 'login.login'
login_manager.init_app(app)


# Auth0 initation
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=os.environ.get(''),
    client_secret=os.environ.get(''),
    api_base_url=os.environ.get(''),
    access_token_url=os.environ.get(''),
    authorize_url=os.environ.get(''),
    client_kwargs={
        'scope': 'openid profile email',
    },
    jwks_uri=f'https://dev-ide3i4bsx5n6mct1.us.auth0.com/.well-known/jwks.json'
)







from . import models

with app.app_context():
    db.create_all()


