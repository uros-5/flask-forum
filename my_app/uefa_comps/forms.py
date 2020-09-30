from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SelectField,TextField,FileField
from wtforms.validators import InputRequired,ValidationError,EqualTo
from flask_wtf.file import FileField, FileRequired

class RegistationForm(FlaskForm):
	username = StringField("username",[InputRequired()])
	password = PasswordField("password",[InputRequired(),
										 EqualTo("confirm",message="Lozinke moraju biti iste!")])
	confirm = PasswordField('Potvrdi sifru', [InputRequired()])

class LoginForm(FlaskForm):
	username = StringField("Username",[InputRequired()])
	password = PasswordField("Password",[InputRequired()])

class VideosForm(FlaskForm):
	naslov = StringField("naslov", validators=[InputRequired()])
	podforum = SelectField("podforum", validators=[InputRequired()],
						   coerce=int,choices=[(1,"Champions League"),(2,"Europe League"),(3,"EURO")])
	slika = FileField("slika", validators=[FileRequired()])
	dl_link = StringField("dl_link", validators=[InputRequired()])