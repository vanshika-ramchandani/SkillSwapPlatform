# app/routes/home.py
from flask import Blueprint, render_template
from app.models import User, AvailabilityEnum

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    users = User.query.filter_by(is_public=True).all()
    availability_options = [e.value for e in AvailabilityEnum]
    return render_template('index.html', users=users, availability_options=availability_options)
