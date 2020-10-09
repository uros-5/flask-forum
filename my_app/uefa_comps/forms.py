from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SelectField,FileField,TextAreaField,BooleanField
from wtforms.validators import InputRequired,ValidationError,EqualTo
from flask_wtf.file import FileField, FileRequired
from my_app.uefa_comps.models import Users,Videos,KomentariNaVideu
import os


class RegistationForm(FlaskForm):
	username = StringField("username",[InputRequired()])
	password = PasswordField("password",[InputRequired(),
										 EqualTo("confirm",message="Lozinke moraju biti iste!")])
	confirm = PasswordField('Potvrdi sifru', [InputRequired()])

	def check_form(self,db):
		existing_username = Users.query.filter_by(username=self.username.data).first()
		if existing_username:
			return False
		user = Users(self.username.data,self.password.data)
		db.session.add(user)
		db.session.commit()
		return True



class LoginForm(FlaskForm):
	username = StringField("Username",[InputRequired()])
	password = PasswordField("Password",[InputRequired()])

	def check_form(self,login_user):
		existing_user = Users.query.filter_by(username=self.username.data).first()
		if not (existing_user and existing_user.check_password(self.password.data)):
			return False
		login_user(existing_user,remember=True)
		return True

class AdminUserCreateForm(FlaskForm):
	username = StringField("username",[InputRequired()])
	password = StringField("password",[InputRequired()])
	admin  = BooleanField("Is Admin ?")

class AdminUserUpdateForm(FlaskForm):
	username = StringField('Username', [InputRequired()])
	admin = BooleanField('Is Admin ?')

class VideosForm(FlaskForm):
	komentar = TextAreaField("komentar",validators=[InputRequired()])

	def post_comment(self,request,video,korisnik,db,get_pages):
		kom_obj = KomentariNaVideu()
		video_obj = Videos.query.filter(Videos.url_view == video).first()
		kom_obj.komentar = request.form.get("komentar")
		kom_obj.napisao = korisnik
		kom_obj.video = video_obj.id
		db.session.add(kom_obj)
		db.session.commit()
		page = get_pages(4, 1, video_obj)
		return {"video":video_obj.url_view,"page":page}