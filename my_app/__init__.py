from flask import Flask
from my_app.uefa_comps.views import uefa_comps

app = Flask(__name__)
app.register_blueprint(uefa_comps)