from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin


def create_app():
	app = Flask(__name__)
	db.init_app(app)
	return app

# BLUEPRINT ZA DRUGE MODULE
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tmp/uefa_comps.db"
app.secret_key = b'vsarTest/'

# LOKACIJA UPLOAD FOLDERA
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = os.path.realpath('.') +'\\my_app\\static\\uploads'

# OBJEKTNA BAZA PODATAKA
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# LOGIN MANAGER ZA LINKOVE SAJTA
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "uefa_comps.login"


# CIRCULAR IMPORT.. UVOZ views
from my_app.uefa_comps.views import uefa_comps,current_user,Users,Videos,KomentariNaVideu,allowed_file
app.register_blueprint(uefa_comps)
db.create_all()

# UVOZ AdminView ZA ADMINA
from my_app.uefa_comps.AdminView import *
admin = Admin(app,index_view=MyAdminIndexView(current_user))

admin.add_view(UserAdminView(Users, db.session,current_user))
videos_admin_view = VideosAdminView(Videos,db.session,current_user)
videos_admin_view.set_flask_tools(allowed_file,app.config['UPLOAD_FOLDER'])
admin.add_view(videos_admin_view)