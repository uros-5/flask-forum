from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField
from werkzeug.security import generate_password_hash,check_password_hash
from flask_admin import BaseView,expose,AdminIndexView


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
	column_sortable_list = ('naslov', 'podforum','objavljeno')
	column_exclude_list = ('slika','dl_link','url_view')
	form_excluded_columns = ('slika','dl_link','url_view')
	form_edit_rules = ('naslov', 'podforum','objavljeno')

	def __init__(self, model, session, current_user):
		super().__init__(model, session)
		self.current_user = current_user

	def create_model(self, form):
		model = self.model(
			form.naslov.data, form.podforum.data,
			form.dl_link.data,form.objavio.data
		)
		form.populate_obj(model)
		self.session.add(model)
		self._on_model_change(form, model, True)
		self.session.commit()

	def scaffold_form(self):
		form_class = super(VideosAdminView, self).scaffold_form()
		return form_class