from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, UserMixin

auth = Blueprint('auth', __name__)

# 🔒 Mock in-memory user storage
mock_users = {
    "test@example.com": {
        "email": "test@example.com",
        "first_name": "Test",
        "password": generate_password_hash("password123", method='pbkdf2:sha256')
    }
}

# 👤 Mock user model for Flask-Login
class MockUser(UserMixin):
    def __init__(self, email, first_name):
        self.id = email
        self.email = email
        self.first_name = first_name
    def get_id(self):
        return self.id

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_data = mock_users.get(email)
        if user_data:
            if check_password_hash(user_data['password'], password):
                flash('Logged in successfully!', category='success')
                user = MockUser(email, user_data['first_name'])
                login_user(user, remember=True)
                return redirect(url_for('auth.profile'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Email not found.', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if email in mock_users:
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
            mock_users[email] = {
                "email": email,
                "first_name": first_name,
                "password": generate_password_hash(password1, method='pbkdf2:sha256')
            }
            user = MockUser(email, first_name)
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.profile'))

    return render_template('signup.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', category='info')
    return redirect(url_for('auth.login'))

@auth.route('/profile')
@login_required
def profile():
    return f"<h2>Welcome, {current_user.first_name}!</h2><br><a href='/logout'>Logout</a>"
