from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import BaseView, expose, AdminIndexView
from wtforms import FileField, SelectField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired
import os
from werkzeug.utils import secure_filename
from PIL import Image
import re, random
from flask import request


class MyAdminIndexView(AdminIndexView):
	def __init__(self, current_user):
		super().__init__()
		self.current_user = current_user

	def is_accessible(self):
		return self.current_user.is_authenticated and self.current_user.is_uploader()


class UserAdminView(ModelView):
	column_searchable_list = ('username',)
	column_sortable_list = ('username', 'uploader')
	column_exclude_list = ('password',)
	form_excluded_columns = ('password',)
	form_edit_rules = ('username', 'uploader')

	def __init__(self, model, session, current_user):
		super().__init__(model, session)
		self.current_user = current_user

	def is_accessible(self):
		return self.current_user.is_authenticated and self.current_user.is_uploader()

	def scaffold_form(self):
		form_class = super(UserAdminView, self).scaffold_form()
		form_class.password = PasswordField('Password')
		return form_class

	def create_model(self, form):
		model = self.model(
			form.username.data, form.password.data,
			form.admin.data
		)

		form.populate_obj(model)
		self.session.add(model)
		self._on_model_change(form, model, True)
		self.session.commit()


class VideosAdminView(ModelView):
	column_searchable_list = ('naslov',)
	column_sortable_list = ('naslov', 'objavljeno')
	column_exclude_list = ('korisnici', 'podforum', 'slika', 'dl_link')
	form_excluded_columns = ('korisnici', 'objavljeno', 'url_view')
	selector_choices = [(1, "Champions League"), (2, "Europe League"), (3, "EURO")]
	current_video = 0

	editing = False

	request = None

	def __init__(self, model, session, current_user):
		super().__init__(model, session)
		self.current_user = current_user

	def is_accessible(self):
		return self.current_user.is_authenticated and self.current_user.is_uploader()

	def _handle_view(self, name, **kwargs):
		if name == "edit_view":
			self.editing = True
			self._refresh_cache()
		else:
			self.editing = False
			self._refresh_cache()

		return super()._handle_view(name, **kwargs)

	def create_model(self, form):
		model = self.model(
			form.naslov.data, form.podforum.data,
			form.dl_link.data, self.current_user.id
		)

		if self.allowed_file(form.slika.data.filename):
			filename = self.save_photo(form.slika.data.filename, form)

		model.slika = str(filename)
		# form.populate_obj(model)
		self.session.add(model)
		self._on_model_change(form, model, True)
		self.session.commit()

	def update_model(self, form, model):
		if form.naslov.data != model.naslov:
			model.naslov = form.naslov.data

		if form.dl_link.data != model.dl_link:
			model.dl_link = form.dl_link.data

		if form.podforum.data != model.podforum:
			model.podforum = form.podforum.data

		if form.slika.data != model.slika:
			filename = self.save_photo(form.slika.data.filename, form)
			model.slika = filename

		self.session.commit()

	def scaffold_form(self):
		form_class = super(VideosAdminView, self).scaffold_form()

		if self.editing == True:
			form_class.slika = FileField("slika")
		else:
			form_class.slika = FileField("slika", validators=[FileRequired()])
			self.selector_choices = ["Champions League", "Europe League", "EURO"]

		form_class.podforum = SelectField("podforum", validators=[InputRequired()],
										  coerce=str, choices=self.selector_choices)
		return form_class

	def set_flask_tools(self, allowed_file, UPLOAD_FOLDER, request):
		self.allowed_file = allowed_file
		self.secure_filename = secure_filename
		self.UPLOAD_FOLDER = UPLOAD_FOLDER
		self.request = request

	def save_photo(self, fajl, form):
		filename = self.secure_filename(fajl)
		if filename in os.listdir(self.UPLOAD_FOLDER):
			sablon = re.compile("(.*)\.(.*)")
			file_info = sablon.findall(fajl)
			filename = "{}{}.{}".format(file_info[0][0], random.randint(1, 100), file_info[0][1]).replace(" ","_")

		form.slika.data.save(os.path.join(self.UPLOAD_FOLDER, filename))

		putanja = "my_app/static/uploads/{}".format(filename)

		image = Image.open(putanja)
		slika2 = image.resize((523, 246))
		slika2.save(putanja)
		image.close()

		return filename
