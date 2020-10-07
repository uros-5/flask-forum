from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SelectField,FileField,TextAreaField,BooleanField
from wtforms.validators import InputRequired,ValidationError,EqualTo
from flask_wtf.file import FileField, FileRequired
from my_app.uefa_comps.models import Users,Videos
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



class AddVideosForm(FlaskForm):
	naslov = StringField("naslov", validators=[InputRequired()])
	podforum = SelectField("podforum", validators=[InputRequired()],
						   coerce=int,choices=[(1,"Champions League"),(2,"Europe League"),(3,"EURO")])
	slika = FileField("slika", validators=[FileRequired()])
	dl_link = StringField("dl_link", validators=[InputRequired()])

	def add_video(self,db,app,allowed_file):

		db.session.add(video)
		db.session.commit()

class AdminUserCreateForm(FlaskForm):
	username = StringField("username",[InputRequired()])
	password = StringField("password",[InputRequired()])
	admin  = BooleanField("Is Admin ?")

class AdminUserUpdateForm(FlaskForm):
	username = StringField('Username', [InputRequired()])
	admin = BooleanField('Is Admin ?')

class VideosForm(FlaskForm):
	komentar = TextAreaField("komentar",validators=[InputRequired()])