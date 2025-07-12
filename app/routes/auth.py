from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from authlib.integrations.flask_client import OAuth
from app import db
from app.models import User
import os

auth = Blueprint('auth', __name__)

# ---------- OAuth Setup ----------
oauth = OAuth()
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@auth.record_once
def init_oauth(state):
    oauth.init_app(state.app)

# ---------- Routes ----------

@auth.route('/')
def home():
    return render_template("home.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash('Logged in successfully!', category='success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Invalid email or password.', category='error')

    return render_template('login.html')

@auth.route('/login/google')
def login_google():
    redirect_uri = url_for('auth.authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri, prompt='select_account')

@auth.route('/authorize/google')
def authorize_google():
    try:
        token = google.authorize_access_token()

        # ✅ Get user info endpoint from Google's OpenID config
        userinfo_endpoint = google.load_server_metadata().get("userinfo_endpoint")
        resp = google.get(userinfo_endpoint)
        user_info = resp.json()

        if not user_info:
            flash("Failed to retrieve user info.", "error")
            return redirect(url_for('auth.login'))

        email = user_info.get("email")
        name = user_info.get("name", "GoogleUser")

        if not email:
            flash("Google account doesn't have an email.", "error")
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                email=email,
                name=name,
                password=generate_password_hash("google_login", method='pbkdf2:sha256')
            )
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash("Logged in with Google!", "success")
        return redirect(url_for('auth.profile'))

    except Exception as e:
        flash(f"Google authentication error: {str(e)}", "error")
        return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be longer.', category='error')
        elif len(first_name) < 2:
            flash('Name must be longer.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password too short.', category='error')
        else:
            new_user = User(
                email=email,
                name=first_name,
                password=generate_password_hash(password1, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.profile'))

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', category='info')
    return redirect(url_for('auth.login'))

@auth.route('/profile')
@login_required
def profile():
    return f"<h2>Welcome, {current_user.name}!</h2><br><a href='/logout'>Logout</a>"
