from app import db
from flask_login import UserMixin
from datetime import datetime
import enum

# ---------- ENUMS ----------
class AvailabilityEnum(enum.Enum):
    weekdays = 'Weekdays'
    weekends = 'Weekends'
    flexible = 'Flexible'
    evenings = 'Evenings'
    anytime = 'Anytime'

class SessionDurationEnum(enum.Enum):
    thirty_mins = '30 minutes'
    one_hour = '1 hour'
    one_half_hour = '1.5 hours'
    two_hours = '2 hours'

# ---------- MODELS ----------

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100))
    profile_photo = db.Column(db.String(255))  # Path or URL
    is_public = db.Column(db.Boolean, default=True)
    availability = db.Column(db.Enum(AvailabilityEnum))
    session_duration = db.Column(db.Enum(SessionDurationEnum))

    # Relationships
    offered_skills = db.relationship('UserSkill', backref='user', cascade="all, delete-orphan", passive_deletes=True)
    wanted_skills = db.relationship('UserWantSkill', backref='user', cascade="all, delete-orphan", passive_deletes=True)
    requests_sent = db.relationship('SwapRequest', backref='sender', foreign_keys='SwapRequest.sender_id', cascade="all, delete-orphan", passive_deletes=True)
    requests_received = db.relationship('SwapRequest', backref='receiver', foreign_keys='SwapRequest.receiver_id', cascade="all, delete-orphan", passive_deletes=True)

class AdminUser(db.Model):
    __tablename__ = 'admin_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Skill(db.Model):
    __tablename__ = 'skill'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    is_custom = db.Column(db.Boolean, default=False)  # True if user added manually

class UserSkill(db.Model):
    __tablename__ = 'user_skill'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id', ondelete='CASCADE'), nullable=False)

class UserWantSkill(db.Model):
    __tablename__ = 'user_want_skill'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id', ondelete='CASCADE'), nullable=False)

class SwapRequest(db.Model):
    __tablename__ = 'swap_request'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    skill_offered_id = db.Column(db.Integer, db.ForeignKey('skill.id', ondelete='SET NULL'))
    skill_requested_id = db.Column(db.Integer, db.ForeignKey('skill.id', ondelete='SET NULL'))
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SwapFeedback(db.Model):
    __tablename__ = 'swap_feedback'

    id = db.Column(db.Integer, primary_key=True)
    swap_id = db.Column(db.Integer, db.ForeignKey('swap_request.id', ondelete='CASCADE'), nullable=False)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer)  # 1 to 5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
