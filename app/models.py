from flask import session
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'<User {self.username}>'


class OAuthUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
        

@login_manager.user_loader
def load_user(user_identifier):
    method = None
    if 'login_method' in session.keys():
        method = session.get('login_method')

    # Check in the OAuthUser model
    if method == 'auth0':
        user = OAuthUser.query.get(int(user_identifier))
        return user
    
    # Check in the User model
    if method == 'internal_login':
        user = User.query.get(int(user_identifier))
        return user
    
    return None


# add new customer
class CEntry(db.Model):
    cust_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=60), nullable=False)
    address = db.Column(db.String(length=150), nullable=True)
    contact = db.Column(db.Integer, nullable=True)
    d_entries = db.relationship('DEntry', backref='customer', lazy=True)

    def __repr__(self):
        return f"{self.name} {self.address} {self.contact}"


# add new products
class PEntry(db.Model):
    part_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=150), nullable=False)
    container_qty = db.Column(db.Integer, nullable=False)
    pieces_qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(scale=2), nullable=False)
    container_capacity = db.Column(db.Integer, nullable=False)
    d_entries = db.relationship('DEntry', backref='part', lazy=True)

    @property
    def total_qty(self):
        return self.container_qty * self.container_capacity + self.pieces_qty
    
    def __repr__(self):
        return f"{self.part_id} {self.name} {self.price} {self.total_qty}"
   
    
# add purchased/sale data
class DEntry(db.Model):
    entry_id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('p_entry.part_id') ,nullable=False)
    container_qty = db.Column(db.Integer, nullable=False)
    pieces_qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(scale=2), nullable=False)
    time = db.Column(db.DateTime(timezone=True), server_default=func.now())
    cust_id = db.Column(db.Integer, db.ForeignKey('c_entry.cust_id'), nullable=False)
    invoice_no = db.Column(db.String(length=150), nullable=False)

    def __repr__(self):
        return f"{self.entry_id} {self.part_id} {self.container_qty} {self.pieces_qty} {self.price} {self.time} {self.cust_id} {self.invoice_no}"


# generate invoice number for each bill
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(20), nullable=False)

    def __init__(self, invoice_number):
        self.invoice_number = invoice_number

    def __repr__(self):
        return f"Invoice Number: {self.invoice_number}"


