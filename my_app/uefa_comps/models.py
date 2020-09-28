from my_app import db
import datetime
class Users(db.Model):
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	username = db.Column(db.String(10),nullable=False,unique=True)
	email = db.Column(db.String(30),nullable=False,unique=True)
	password = db.Column(db.String(20),nullable=False)
	datum_registracije = db.Column(db.Date(),nullable=False,default=datetime.datetime.utcnow)
	uploader = db.Column(db.Boolean(),default=False)

	def __init__(self,username,email,password,uploader = False):
		self.username = username
		self.email = email
		self.password = password
		self.uploader = uploader

	def __repr__(self):
		return self.id

class Videos(db.Model):
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	naslov = db.Column(db.String(10),nullable=False)
	podforum = db.Column(db.String(30),nullable=False)
	objavljeno = db.Column(db.Date(), nullable=False,default=datetime.datetime.utcnow)
	slika = db.Column(db.String(80),nullable=False)
	dl_link = db.Column(db.String(80),nullable=False)
	objavio = db.Column(db.Integer(),db.ForeignKey("users.id"))


	def __repr__(self):
		return self.id

class KomentariNaVideu(db.Model):
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	komentar = db.Column(db.Text(400),nullable=False)
	napisano = db.Column(db.Date(),nullable=False,default=datetime.datetime.utcnow)
	video = db.Column(db.Integer(),db.ForeignKey("videos.id"))
	napisao = db.Column(db.Integer(),db.ForeignKey("users.id"))

	def __repr__(self):
		return self.id

class VideoLikes(db.Model):
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	video = db.Column(db.Integer(),db.ForeignKey("videos.id"))
	ocenio = db.Column(db.Integer(),db.ForeignKey("users.id"))

	def __repr__(self):
		return self.id


