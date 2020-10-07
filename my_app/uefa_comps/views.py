from flask import Blueprint,render_template,request,flash,redirect,url_for,session,g,jsonify
from my_app.uefa_comps.models import *
from my_app.uefa_comps.forms import *
from my_app import login_manager
from my_app import db,ALLOWED_EXTENSIONS,os,app
from flask_login import current_user,login_user,logout_user,login_required
from functools import wraps
from flask import abort
from flask_admin import BaseView,expose,AdminIndexView


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
	if (request.method == "POST"):
		kom_obj = KomentariNaVideu()
		video_obj = Videos.query.filter(Videos.url_view == video).first()
		kom_obj.komentar = request.form.get("komentar")
		kom_obj.napisao = current_user.id
		kom_obj.video = video_obj.id
		db.session.add(kom_obj)
		db.session.commit()
		page = get_pages(4,1,video_obj)
		return redirect(url_for("uefa_comps.video", video=video_obj.url_view, page=page))


# ADMIN URLS
@uefa_comps.route("/admin")
@login_required
@admin_login_required
def home_admin():
	return render_template("admin-home.html")

@uefa_comps.route("/admin/user-list")
@login_required
@admin_login_required
def user_list_admin():
	users = Users.query.all()
	return render_template("users-list-admin.html",users = users)

class VideosAdd(BaseView):
	@expose("/")
	def adding_videos(self):
		form = AddVideosForm(meta={'csrf': False})
		if request.method == "POST" and form.validate():
			form.add_video(db, app, allowed_file)
			return redirect("uefa_comps.pocetna")
		return render_template("test.html", text="Uspesno je!", form=form)

	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_uploader()




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

def get_pages(items,page,video_obj):
	komentari = KomentariNaVideu.query.filter(KomentariNaVideu.video == video_obj.id).paginate(1, 4)
	return komentari.pages