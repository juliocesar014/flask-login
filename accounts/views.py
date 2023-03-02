from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user
from accounts.forms import RegisterForm
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