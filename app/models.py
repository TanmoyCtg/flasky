from datetime import datetime 
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from markdown import markdown 
# import bleach
from flask import current_app, request, url_for 
# from flask_login import UserMixin, AnonymousUserMixin
# from app.exceptions import validatorError
from . import db

class Permission:
	FOLLOW = 0x01
	COMMENT = 0x02
	WRITE_ARTICLES = 0x04
	MODERATE_COMMENTS = 0x08
	ADMINISTER = 0x80 

class Role(db.Model):
	__tablename__='roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	default = db.Column(db.Boolean, default=False, index=True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User', backref='role', lazy='dynamic')

	@staticmethod
	def insert_roles():
		roles = {
			'User':(Permission.FOLLOW|Permission.COMMENT|Permission.WRITE_ARTICLES, True),
			'Moderator':(Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES |Permission.MODERATE_COMMENTS, False),
			'Administrator':(0xff, False)
		}
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()

	def __repr__(self):
		return '<Role %r' %self.name 

class User(db.Model):
	__tablename__ = 'users' 
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	password_hash = db.Column(db.String(128))
	'''
	confirmed = db.Column(db.Boolean, default=False)
	name = db.Column(db.String(64))
	location = db.Column(db.String(64))
	about_me = db.Column(db.Text())
	member_since = db.Column(db.DateTime(), default=datetime.utcnow)
	last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
	avatar_hash = db.Column(db.String(32))
	posts = db.relationship('Post',backref='author', lazy='dynamic')
	'''
	'''
	followed = db.relationship('Follow', 
								foreign_keys=[Follow.follower_id],
								backref=db.backref('follower',lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orrphan')
	
	followers = db.relationship('Follow',
								foreign_keys=[Follow.followed_id],
								backref=db.backref('followed', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orrphan')
	comments = db.relationship('Comment', backref='author', lazy='dynamic')
	'''

	@property
	def password(self):
		raise AttributError('PASSWORD is not a readable attribute')
	
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
	

	def __repr__(self):
		return '<User %r>' %self.username 
