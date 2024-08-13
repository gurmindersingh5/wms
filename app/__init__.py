from flask import Flask
from flask_session import Session
from datetime import timedelta

from .dashapp import init_dash_app
from .extensions import db, migrate, login_manager, oauth, jwt

def create_app():
    app = Flask(__name__, static_url_path='/app/static')

    init_dash_app(app) # initializing dash app
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = "super_secret_key"

    # config session in app
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False  # Sessions won't expire on browser close
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)  # Session timeout

    # Configure JWT settings
    app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'  # Replace with your secret key

    db.init_app(app)
    migrate.init_app(app, db)
    Session(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'
    jwt.init_app(app)

    # Auth0 initation
    oauth.init_app(app)

    from app.blueprints.home.home import home_bp
    from app.blueprints.inventory.inventory import inventory_bp
    from app.blueprints.customer.customer import customer_bp
    from app.blueprints.addproduct.addproduct import addproduct_bp
    from app.blueprints.editproduct.editproduct import editproduct_bp
    from app.blueprints.register.register import register_bp
    from app.blueprints.sales.sales import sales_bp
    from app.blueprints.addcustomer.addcustomer import addcustomer_bg
    from app.blueprints.profile.profile import profile_bp
    from app.blueprints.analytics_api.analytics_api import analytics_api_bs

    from app.blueprints.login.login import login_bp
    from app.blueprints.google.google import google_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(addproduct_bp)
    app.register_blueprint(editproduct_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(addcustomer_bg)
    app.register_blueprint(profile_bp)
    app.register_blueprint(analytics_api_bs)

    app.register_blueprint(google_bp, url_prefix="/login")

    # created database table
    with app.app_context():
        db.create_all()

    return app

