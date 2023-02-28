from flask import Blueprint, request, jsonify, Flask
from flask_login import login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin, LoginManager
import os
from flask_sqlalchemy import SQLAlchemy

from src.models import User



db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SECRET_KEY"] = "oaejaoeijaoiejasoj"
    db.init_app(app)
    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        with app.app_context():
            return User.user.get(int(id))
    
    app.register_blueprint(blog, url_prefix="")
    app.register_blueprint(auth, url_prefix="/auth")
    return app


def create_database(app):
    if not os.path.exists("instance/" + "db.sqlite"):
        with app.app_context():
            db.create_all()
        print("Database created")




auth = Blueprint("auth", __name__)

@auth.post("/login")
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            return (
                jsonify({
                    "status": "SUCESS",
                    "message": "User Logged in successfully"
                }), 200
            )
        else:
            return (
                jsonify({
                    "status": "FAILED",
                    "message": "Incorrect Password"
                }), 400 # Bad Request Error Client Side
            )
    else:
        return (
            jsonify({
                "status": "FAILED",
                "message": "user does not exist"
            }), 400 # Bad Request Error Client Side
        )
        
        
@auth.get("/me")
def me():
    if current_user.is_autheticated:
        return (
            jsonify({
                "status": "SUCESS",
                "message": "User Logged in successfully",
                "data" : {
                    "username": current_user.username,
                }
            }), 200
        )
        
    else:
        return (
            jsonify({
                "status": "FAILED",
                "message": "Not Authenticated"
            }), 400
        )
        

@auth.post("/register")
def register():
    data = request.json
    username = request.get("username")
    email = request.get("email")
    password_1 = request.get("password-1")
    password_2 = request.get("password-2")
    
    if password_1 != password_2:
        return (
            jsonify({
                "status": "FAILED",
                "message": "Passwords do not match"
            }), 400
        )
    else:
        user = User(
            email = email,
            username = username,
            password = generate_password_hash(password_1, "sha256")
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            print(f"Error: {e}")
        else:
            login_user(user, remember=True)
            return (
                jsonify({
                    "status": "SUCESS",
                    "message": "User Logged in successfully"
                }), 200
            )
            
            
blog = Blueprint("blog", __name__)


@blog.get("/")
def status():
    return jsonify({"status":"Up and Running"}), 200


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)