from flask import Blueprint,render_template,request,flash,redirect,url_for,session,g,jsonify
from my_app.uefa_comps.models import *
from my_app.uefa_comps.forms import *
from my_app import login_manager
from my_app import db,ALLOWED_EXTENSIONS,os,app
from flask_login import current_user,login_user,logout_user,login_required
from functools import wraps
from flask import abort
import random,pyperclip
import datetime

uefa_comps = Blueprint("uefa_comps", __name__)

@login_manager.user_loader
def load_user(id):
	return Users.query.get(int(id))

@uefa_comps.before_request
def get_current_user():
	g.user = current_user

def admin_login_required(func):
	@wraps(func)
	def decorated_view(*args, **kwargs):
		if not current_user.is_admin():
			return abort(403)
		return func(*args, **kwargs)
	return decorated_view


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
		if not form.check_form(login_user):
			flash("Netacno korisnicko ime ili sifra.","danger")
			return render_template("login.html", form=form)
		else:
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
		if not form.check_form(db):
			flash("Ovaj username vec posotoji.","warning")
			return render_template("register.html",form = form)
		else:
			flash("Sada ste registrovani,prijavite se.","success")
			return redirect(url_for("uefa_comps.login"))
	if form.errors:
		flash(form.errors,"danger")
	return render_template("register.html",form = form)


# PODFORUM
@uefa_comps.route("/<podforum>/<int:page>")
@login_required
def forum(podforum,page):
	videos = Videos.query.filter(Videos.podforum == podforum_name(podforum)).order_by(Videos.id.desc()).paginate(page, 5)
	return render_template("podforum.html", videos= videos, podforum = podforum_name(podforum))

# VIDEO
@uefa_comps.route("/video/<video>/<int:page>/",methods=["GET"])
@login_required
def video(video,page):
	video_obj = Videos.query.filter(Videos.url_view == video).first()
	form = VideosForm()
	if(video_obj!=None):
		user = Users.query.get(video_obj.objavio)
		komentari = KomentariNaVideu.query.filter(KomentariNaVideu.video == video_obj.id).paginate(page, 4)
		return render_template("video.html", form = form,video=video_obj, user=user,komentari = komentari)
	return render_template("base.html")

# ADDING COMMENTS ON VIDEO
@uefa_comps.route("/add_comment/<video>",methods=["POST"])
@login_required
def add_comment(video):
	form = VideosForm()
	if (request.method == "POST"):
		res = form.post_comment(request,video,current_user.id,db,get_pages)
		return redirect(url_for("uefa_comps.video", video=res["video"], page=res["page"]))


@uefa_comps.context_processor
def utility_processor():
	def set_url(video,id=""):
		video = video.replace(" ","_").lower()
		if(id!=""):
			return video + "_"+str(id)
		return video

	def message_posted(podforum):
		sekunde = Videos.get_time_for_index(podforum)
		if(sekunde<60):
			return "nedavno"
		elif(sekunde>60 and sekunde<3600):
			return "pre {} min".format(int(sekunde/60))

		elif (sekunde > 3600 and sekunde <86400):
			return "pre {} sati".format(int(sekunde / 3600))

		elif (sekunde > 86400 and sekunde <2592000):
			return "pre {} dana".format(int(sekunde / 86400))

		elif (sekunde > 2592000 and sekunde <31104000):
			return "pre {} meseci".format(int(sekunde / 2592000))

		elif (sekunde > 31104000):
			return "pre {} godine".format(int(sekunde / 60))

	return dict(set_url=set_url,message_posted=message_posted)

# OTHER FUNCTIONS
def podforum_name(podforum):
	podforum = podforum.replace("_"," ")
	if " " in podforum:
		reci = [r.capitalize() for r in podforum.split(" ")]
		podforum = " ".join(reci)
		return podforum
	return podforum.upper()



def is_logged():
	return session.get('username')

def get_pages(items,page,video_obj):
	komentari = KomentariNaVideu.query.filter(KomentariNaVideu.video == video_obj.id).paginate(1, 4)
	return komentari.pages
