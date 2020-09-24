from flask import Flask
app = Flask(__name__,static_folder="/static/css",static_url_path="/difcss",
			instance_path="/instance/",instance_relative_config=True)
app.config["DEBUG"] = False
app.config.from_pyfile("config.cfg",silent=True)

@app.route("/")
def pocetna():
	return "evo je moja pocetna"

# if __name__ == '__main__':
# 	app.run()