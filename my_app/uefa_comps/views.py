from flask import Blueprint,render_template,request
from my_app.uefa_comps.models import *
from my_app import db
import random

uefa_comps = Blueprint("uefa_comps", __name__)

@uefa_comps.route("/")
@uefa_comps.route("/home")
def pocetna():
	forum = db.session.query(Videos.podforum).group_by(Videos.id).distinct()
	return render_template("index.html",forum = forum)

@uefa_comps.route("/<podforum>")
def forum(podforum):

	videos = Videos.query.filter(Videos.podforum == set_podforum(podforum)).all()

	return render_template("podforum.html",videos= videos,podforum = podforum)

@uefa_comps.route("/<podforum>/<id>")
def video(podforum,id):
	print("ok")


@uefa_comps.route("/register")
def register():
	return render_template("register.html")


@uefa_comps.route("/login")
def login():
	return render_template("login.html")

@uefa_comps.route("/podforum/id")
def watch(podforum,id):
	video = Videos.query.get(id)
	return render_template("video.html",video = video)


# TEPMLATE FILTERS
@uefa_comps.app_template_filter("set_url")
def set_url(podforum):
	return str(podforum).replace(" ","_").lower()


def set_podforum(podforum):
	podforum = podforum.replace("_"," ")
	if " " in podforum:
		reci = [r.capitalize() for r in podforum.split(" ")]
		podforum = " ".join(reci)
		return podforum
	return podforum.upper()

