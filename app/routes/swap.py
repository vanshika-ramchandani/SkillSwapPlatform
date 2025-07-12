# app/routes/swap.py
from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required

swap_bp = Blueprint('swap', __name__, url_prefix='/swap')

@swap_bp.route('/request/<int:receiver_id>', methods=['GET', 'POST'])
@login_required
def send_request(receiver_id):
    # Implement actual logic to create a swap request
    flash("Swap request sent!", "success")
    return redirect(url_for('search.index'))
