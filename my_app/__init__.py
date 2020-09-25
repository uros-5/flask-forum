from flask import Flask

from flask_sqlalchemy import SQLAlchemy
import os

def create_app():
	app = Flask(__name__)
	db.init_app(app)
	return app


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tmp/uefa_comps.db"
db = SQLAlchemy(app)

from my_app.uefa_comps.views import uefa_comps
app.register_blueprint(uefa_comps)
db.create_all()
