from flask import Flask, render_template, redirect, url_for, flash, request
from flask_security.utils import verify_password, hash_password
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, login_user, current_user
from flask_migrate import Migrate
from forms import RegistrationForm, LoginForm
from models import db, User, Role, UserRoles
import random
import string
import os

# Initialize the app
app = Flask(__name__)

# Configurations
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT', 'default_password_salt')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Security configurations
app.config['SECURITY_PASSWORD_HASH'] = 'argon2'

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Function to generate a random account number (10 digits)
def generate_account_number():
    return ''.join(random.choices(string.digits, k=10))

# Function to generate a random customer ID (5 digits)
def generate_customer_id():
    return ''.join(random.choices(string.digits, k=5))

# Initialize the user_datastore
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# Initialize Flask-Security
security = Security(app, user_datastore)

# Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the email already exists
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered. Please use a different email.", "danger")
            return render_template("register.html", form=form)

        account_number = generate_account_number()
        customer_id = generate_customer_id()

        # Ensure unique account number and customer ID
        while User.query.filter_by(account_number=account_number).first():
            account_number = generate_account_number()
        while User.query.filter_by(customer_id=customer_id).first():
            customer_id = generate_customer_id()

        # Create user and ensure default_role exists
        user = user_datastore.create_user(
            username=form.username.data,
            password=hash_password(form.password.data),
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone_number=form.phone_number.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            postal_code=form.postal_code.data,
            account_number=account_number,
            customer_id=customer_id,
            #full_name=f"{form.first_name.data} {form.last_name.data}"
        )

        # Ensure the default role exists in the database
        default_role = Role.query.filter_by(name='default_role').first()
        if default_role:
            user_datastore.add_role_to_user(user, default_role)
        else:
            flash("Default role not found, please ensure it exists in the database.", "danger")
            return redirect(url_for("register"))

        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    else:
        print("Form validation failed")
        print(form.errors)
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()  # Initialize the login form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and verify_password(form.password.data, user.password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password.", "danger")
    return render_template("login.html", form=form)  # Pass the form to the template

@app.route("/dashboard")
@login_required
def dashboard():
    user = current_user
    return render_template("dashboard.html", user=user)

@app.route("/withdraw", methods=["POST"])
@login_required
def withdraw():
    amount = float(request.form.get('amount'))
    if amount > 0 and amount <= current_user.balance:
        current_user.balance -= amount
        db.session.commit()
        flash("Withdrawal successful.", "success")
    else:
        flash("Invalid amount or insufficient balance.", "danger")
    return redirect(url_for("dashboard"))

@app.route("/deposit", methods=["POST"])
@login_required
def deposit():
    amount = float(request.form.get('amount'))
    if amount > 0:
        current_user.balance += amount
        db.session.commit()
        flash("Deposit successful.", "success")
    else:
        flash("Invalid amount.", "danger")
    return redirect(url_for("dashboard"))

@app.route("/logout")
@login_required
def logout():
    #logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))

# Run the application
if __name__ == "__main__":
    app.run(debug=True)