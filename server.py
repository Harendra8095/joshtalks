from flask import Flask
from flask_cors import CORS

from joshBack.config import DbEngine_config
from joshBack import create_db_engine, create_db_sessionFactory
from joshBack.api import *

engine = create_db_engine(DbEngine_config)
SQLSession = create_db_sessionFactory(engine)

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.from_object(DbEngine_config())

CORS(app, supports_credentials=True)


@app.route("/")
def get():
    return "<h1> Hello, Welcome to backend of JoshTalks </h1>"


app.register_blueprint(youtubeBP, url_prefix="/{}/youtube".format(API_VERSION_V1))
app.register_blueprint(homeBP, url_prefix="/{}/home".format(API_VERSION_V1))


if __name__ == "__main__":
    # run_background_job()
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
