
#! This file conains all the database models that are required for the models


from flask_sqlalchemy import SQLAlchemy
from flask_security.core import UserMixin,RoleMixin

db = SQLAlchemy()
class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,autoincrement = True, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean()) #* Used for validating the manager by the admin
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)  #* Used to generate JWT token
    roles = db.relationship('Role',secondary='roles_users',backref=db.backref('users',lazy='dynamic'))

class RoleUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column('user_id',db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column('role_id',db.Integer,db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True,autoincrement= True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Songs(db.Model):
    __tablename__= 'song'
    id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    name = db.Column(db.String,nullable = False)
    artist = db.Column(db.String,nullable = False)
    location = db.Column(db.String, nullable = False)
    lyrics = db.Column(db.String,nullable = False)
    rating = db.Column(db.Integer,nullable = False, default = 0)

class Playlist(db.Model):
    __tablename__ = 'playlist'
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    name = db.Column(db.String,nullable = False)
    songs = db.relationship('Songs',secondary = 'playlist_song',backref = 'playlist')

playlist_song = db.Table('playlist_song',
                         db.Column('playlist_id',db.Integer,db.ForeignKey('playlist.id'),primary_key = True),
                         db.Column('song_id',db.Integer,db.ForeignKey('song.id'),primary_key = True))