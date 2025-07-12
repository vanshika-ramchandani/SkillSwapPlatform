# app/routes/user.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, Skill, UserSkill, UserWantSkill, AvailabilityEnum, SessionDurationEnum

profile = Blueprint('profile', __name__)

@profile.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    all_skills = Skill.query.order_by(Skill.name).all()
    offered_ids = [s.skill_id for s in current_user.offered_skills]
    wanted_ids = [s.skill_id for s in current_user.wanted_skills]

    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.location = request.form.get('location')
        current_user.availability = request.form.get('availability')
        current_user.session_duration = request.form.get('session_hours')
        current_user.is_public = request.form.get('is_public') == 'public'

        # Clear current skills
        UserSkill.query.filter_by(user_id=current_user.id).delete()
        UserWantSkill.query.filter_by(user_id=current_user.id).delete()

        # Offered skills (existing and custom)
        for skill_id in request.form.getlist('skills_offered[]'):
            if skill_id == "custom_offered":
                custom_skill = request.form.get("custom_offered", "").strip()
                if custom_skill:
                    new_skill = Skill(name=custom_skill, is_custom=True)
                    db.session.add(new_skill)
                    db.session.flush()
                    db.session.add(UserSkill(user_id=current_user.id, skill_id=new_skill.id))
            else:
                db.session.add(UserSkill(user_id=current_user.id, skill_id=int(skill_id)))

        # Wanted skills (existing and custom)
        for skill_id in request.form.getlist('skills_wanted[]'):
            if skill_id == "custom_wanted":
                custom_skill = request.form.get("custom_wanted", "").strip()
                if custom_skill:
                    new_skill = Skill(name=custom_skill, is_custom=True)
                    db.session.add(new_skill)
                    db.session.flush()
                    db.session.add(UserWantSkill(user_id=current_user.id, skill_id=new_skill.id))
            else:
                db.session.add(UserWantSkill(user_id=current_user.id, skill_id=int(skill_id)))

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('auth.profile'))

    # Dropdown options
    availability_options = [a.value for a in AvailabilityEnum]
    session_options = [s.value for s in SessionDurationEnum]

    return render_template(
        'edit_profile.html',
        all_skills=all_skills,
        offered_ids=offered_ids,
        wanted_ids=wanted_ids,
        availability_options=availability_options,
        session_options=session_options
    )