from flask import Flask
from flask_cors import CORS

from joshBack.config import DbEngine_config
from joshBack import create_db_engine, create_db_sessionFactory

engine = create_db_engine(DbEngine_config)
SQLSession = create_db_sessionFactory(engine)

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.from_object(DbEngine_config())

CORS(app, supports_credentials=True)


@app.route("/")
def get():
    return "<h1> Hello, Welcome to backend of JoshTalks </h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
