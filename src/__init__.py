from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .blog import blog
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    db.init_app(app)
    
    create_database(app)
    
    app.register_blueprint(blog, url_prefix="")
    return app


def create_database(app):
    if not os.path.exists("instance/" + "db.sqlite"):
        with app.app_context():
            db.create_all()
        print("Database created")