from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(32), unique = True)
    username = db.Column(db.String(32), unique = True)
    password = db.Column(db.String(32))

    date = db.Column(db.DateTime(timezone = True), default = func.now())

    folders = db.relationship('Section', backref = 'user', passive_deletes = True)

class Section(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32))

    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'), nullable = False)

    photos = db.relationship('Photo', backref = 'section', passive_deletes = True)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(512))

    data = db.Column(db.LargeBinary)

    folder = db.Column(db.Integer, db.ForeignKey('section.id', ondelete = 'CASCADE'), nullable = False)
