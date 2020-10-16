from my_app import db
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SelectField,TextField

import secrets
from werkzeug.security import generate_password_hash,check_password_hash

class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(10), nullable=False, unique=True)
	password = db.Column(db.String(), nullable=False)
	datum_registracije = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow())
	uploader = db.Column(db.Boolean(), default=False)

	def __init__(self, username, password, uploader=False):
		self.username = username
		self.password = generate_password_hash(password)
		self.uploader = uploader

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymus(self):
		return False

	def get_id(self):
		return str(self.id)

	def check_password(self,password):
		return check_password_hash(self.password,password)

	def __repr__(self):
		return self.id

	def is_uploader(self):
		return self.uploader

	def __str__(self):
		return str(self.id)


class Videos(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	naslov = db.Column(db.String(80), nullable=False)
	podforum = db.Column(db.String(30), nullable=False)
	objavljeno = db.Column(db.DateTime(), nullable=False, default=lambda : datetime.datetime.utcnow())
	slika = db.Column(db.String(255), nullable=False)
	dl_link = db.Column(db.String(80), nullable=False)
	objavio = db.Column(db.Integer(), db.ForeignKey("users.id"))
	url_view = db.Column(db.String(60), nullable=False,unique=True,default=lambda nbytes=16: secrets.token_hex(nbytes))
	korisnici = db.relationship(
		'Users', backref=db.backref('objavio', lazy='dynamic')
	)
	def __init__(self,naslov,podforum,dl_link,objavio=1):
		self.naslov = naslov
		self.podforum = podforum
		self.dl_link = dl_link
		self.objavio = objavio
		self.slika = ""

	def __repr__(self):
		return str(self.id)

	def __str__(self):
		return str(self.id)

	def get_time_for_index(podforum):
		obj = Videos.query.filter(Videos.podforum==podforum).order_by(Videos.id.desc()).first()
		vreme = (datetime.datetime.utcnow() - obj.objavljeno).total_seconds()
		return vreme


class KomentariNaVideu(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	komentar = db.Column(db.Text(400), nullable=False)
	napisano = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow)
	video = db.Column(db.Integer(), db.ForeignKey("videos.id"))
	napisao = db.Column(db.Integer(), db.ForeignKey("users.id"))
	korisnici = db.relationship(
		'Users', backref=db.backref('napisao', lazy='dynamic')
	)

	def __repr__(self):
		return self.id


class VideoLikes(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	video = db.Column(db.Integer(), db.ForeignKey("videos.id"))
	ocenio = db.Column(db.Integer(), db.ForeignKey("users.id"))

	def __repr__(self):
		return self.id





