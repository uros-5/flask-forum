from flask import Blueprint,render_template,request,flash,redirect,url_for,session,g
from my_app.uefa_comps.models import *
from my_app.uefa_comps.forms import *
from my_app import login_manager
from my_app import db,ALLOWED_EXTENSIONS,os,app
import random,pyperclip
from werkzeug.utils import secure_filename
from flask_login import current_user,login_user,logout_user,login_required


uefa_comps = Blueprint("uefa_comps", __name__)

@login_manager.user_loader
def load_user(id):
	return Users.query.get(int(id))
@uefa_comps.before_request
def get_current_user():
	g.user = current_user

# POCETNA
@uefa_comps.route("/")
@uefa_comps.route("/home/")
@login_required
def pocetna():
	forum = db.session.query(Videos.podforum).group_by(Videos.id).distinct()
	return render_template("index.html",forum = forum)

# LOGIN
@uefa_comps.route("/login/",methods=["GET","POST"])
def login():
	if current_user.is_authenticated:
		flash("Vec ste prijavljeni","info")
		return redirect(url_for("uefa_comps.pocetna"))

	form = LoginForm()
	if form.validate_on_submit():
		username = request.form.get("username")
		password = request.form.get("password")
		existing_user = Users.query.filter_by(username=username).first()
		if not (existing_user and existing_user.check_password(password)):
			flash("Netacno korisnicko ime ili sifra.","danger")
			return render_template("login.html",form=form)

		login_user(existing_user,remember=True)
		return redirect(url_for("uefa_comps.pocetna"))
	if form.errors:
		flash(form.errors,"danger")
	return render_template("login.html",form=form)

# LOGOUT
@uefa_comps.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("uefa_comps.pocetna"))

# REGISTER
@uefa_comps.route("/register/",methods=["GET","POST"])
def register():
	if is_logged():
		flash("Vec ste prijavljeni","info")
		return redirect(url_for("uefa_comps.pocetna"))

	form = RegistationForm()

	if form.validate_on_submit():
		username = request.form.get("username")
		password = request.form.get("password")

		existing_username = Users.query.filter_by(username=username).first()

		if existing_username:
			flash("Ovaj username vec posotoji.","warning")
			return render_template("register.html",form = form)
		user = Users(username,password)
		db.session.add(user)
		db.session.commit()
		flash("Sada ste registrovani,prijavite se.","success")
		return redirect(url_for("uefa_comps.login"))
	if form.errors:
		flash(form.errors,"danger")
	return render_template("register.html",form = form)



# PODFORUM
@uefa_comps.route("/<podforum>/<int:page>")
@login_required
def forum(podforum,page):
	videos = Videos.query.filter(Videos.podforum == podforum_name(podforum)).paginate(page, 5)
	return render_template("podforum.html", videos= videos, podforum = podforum_name(podforum))

# VIDEO
@uefa_comps.route("/video/<video>/<int:page>/")
@login_required
def video(video,page):
	video_obj = Videos.query.filter(Videos.url_view == video).first()
	if(video_obj!=None):
		user = Users.query.get(video_obj.objavio)
		komentari = KomentariNaVideu.query.filter(KomentariNaVideu.video == video_obj.id).paginate(page, 4)
		return render_template("video.html", video=video_obj, user=user,komentari = komentari)
	return render_template("base.html")

# ADDING VIDEO
@uefa_comps.route("/add_video/",methods=["GET","POST"])
@login_required
def add_video():
	form = VideosForm(meta={'csrf': False})
	if request.method == "POST" and form.validate():
		naslov = form.naslov.data
		podforum = form.podforum.data
		slika = form.slika.data
		dl_link = form.dl_link.data
		if allowed_file(slika.filename):
			filename = secure_filename(slika.filename)
			slika.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

		video = Videos(naslov,podforum,dl_link,1)
		video.slika = filename
		db.session.add(video)
		db.session.commit()
		return redirect("uefa_comps.pocetna")
	return render_template("test.html",text="Uspesno je!",form=form)



@uefa_comps.context_processor
def utility_processor():
	def set_url(video,id=""):
		video = video.replace(" ","_").lower()
		if(id!=""):
			return video + "_"+str(id)
		return video
	return dict(set_url=set_url)


# OTHER FUNCTIONS
def podforum_name(podforum):
	podforum = podforum.replace("_"," ")
	if " " in podforum:
		reci = [r.capitalize() for r in podforum.split(" ")]
		podforum = " ".join(reci)
		return podforum
	return podforum.upper()

def allowed_file(filename):
	return '.' in filename and filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def is_logged():
	return session.get('username')