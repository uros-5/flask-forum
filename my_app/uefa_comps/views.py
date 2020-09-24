from flask import Blueprint,render_template,request
from my_app.uefa_comps.models import FORUM

uefa_comps = Blueprint("uefa_comps", __name__)

@uefa_comps.route("/")
def pocetna():
	return render_template("index.html", forum=FORUM)

@uefa_comps.route("/<podforum>")
def forum(podforum):

	podaci = FORUM[podforum]
	return render_template("podforum.html",podaci= podaci)

@uefa_comps.route("/register")
def register():
	return render_template("register.html")


@uefa_comps.route("/login")
def login():
	return render_template("login.html")


