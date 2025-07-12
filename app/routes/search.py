from flask import Blueprint, render_template, request
from app.models import User
from app import db

search_bp = Blueprint('search', __name__)

@search_bp.route('/browse')
def browse():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Fetch public users
    pagination = User.query.filter_by(is_public=True).paginate(page=page, per_page=per_page)

    return render_template('browse.html', pagination=pagination)
