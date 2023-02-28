from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)
    
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id', ondelete="CASCADE"))
    
    created_organizations = db.relationship("Organization", backref="admin", primaryjoin="User.id==Organization.creator_id")
    organization = db.relationship("Organization", backref="members", foreign_keys=[organization_id])