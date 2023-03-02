from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from accounts.forms import RegisterForm, LoginForm
from src import db
from accounts.models import User

accounts_bp = Blueprint('accounts', __name__)


@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in", "info")
        return redirect(url_for("core.home"))
    form = RegisterForm(request.form)
    if form.validate.on_submit():
        user = User(form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash("You have successfully registered and are now logged in. Welcome", "success")
        
        return redirect(url_for("core.home"))
    
    return render_template("accounts/register.html", form=form)


@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in", "info")
        return redirect(url_for("core.home"))
    form = LoginForm(request.form)
    if form.validate.on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("You have successfully logged in", "success")
            return redirect(url_for("core.home"))
        else:
            flash("Invalid email or password", "danger")
            return render_template("accounts/login.html", form=form)
    return render_template("accounts/login.html", form=form)



@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out", "success")
    return redirect(url_for("accounts.login"))