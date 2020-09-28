from flask import Blueprint,render_template,request
from my_app.uefa_comps.models import *
from my_app import db
from flask import jsonify
import pyperclip,random

uefa_comps = Blueprint("uefa_comps", __name__)

# POCETNA
@uefa_comps.route("/")
@uefa_comps.route("/home/")
def pocetna():
	forum = db.session.query(Videos.podforum).group_by(Videos.id).distinct()
	return render_template("index.html",forum = forum)

# REGISTER
@uefa_comps.route("/register/")
def register():
	return render_template("register.html")

# LOGIN
@uefa_comps.route("/login/")
def login():
	return render_template("login.html")

# PODFORUM
@uefa_comps.route("/<podforum>/<int:page>")
def forum(podforum,page):
	videos = Videos.query.filter(Videos.podforum == set_podforum(podforum)).paginate(page,5)
	return render_template("podforum.html",videos= videos,podforum = set_podforum(podforum))

# VIDEO
@uefa_comps.route("/<podforum>/<video>/<int:page>/")
def video(podforum,video,page):
	id = int(video.split("_")[-1])
	video_obj = Videos.query.get(id)
	try:
		user = Users.query.get(video_obj.objavio)
		if (video_obj.podforum == set_podforum(podforum)):
			komentari = KomentariNaVideu.query.filter(KomentariNaVideu.video == video_obj.id).paginate(page, 4)
			return render_template("video.html", video=video_obj, user=user,komentari = komentari)
		else:
			return render_template("base.html")
	except:
		return render_template("base.html")



@uefa_comps.context_processor
def utility_processor():
	def set_url(video,id=""):
		video = video.replace(" ","_").lower()
		if(id!=""):
			return video + "_"+str(id)
		return video
	return dict(set_url=set_url)


# OTHER FUNCTIONS
def set_podforum(podforum):
	podforum = podforum.replace("_"," ")
	if " " in podforum:
		reci = [r.capitalize() for r in podforum.split(" ")]
		podforum = " ".join(reci)
		return podforum
	return podforum.upper()

