from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    users = db.relationship('User', secondary='user_roles', back_populates='roles')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    address = db.Column(db.String(500), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    account_number = db.Column(db.String(120), unique=True, nullable=False)
    customer_id = db.Column(db.String(5), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)  # Added by Flask-Security

    roles = db.relationship('Role', secondary='user_roles', back_populates='users')

    # Adding a representation method for better debugging and logging
    def __repr__(self):
        return f'<User {self.username}, Account Number: {self.account_number}, Customer ID: {self.customer_id}>'

    # Verify password for login
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    # Set password (hashing it before saving)
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Save the user instance to the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Generate a unique account number (this could be an example, adjust as needed)
    @staticmethod
    def generate_account_number():
        return "AC" + str(db.session.query(db.func.max(User.account_number)).scalar() + 1)

    # Generate a customer ID (you can set your own logic here for generating unique customer IDs)
    @staticmethod
    def generate_customer_id():
        return "CUS" + str(db.session.query(db.func.max(User.customer_id)).scalar() + 1)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)