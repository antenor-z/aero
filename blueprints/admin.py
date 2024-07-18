from flask import render_template, redirect, request, Blueprint, session, redirect

from DB.ORM import User
from security import password

admin = Blueprint('admin', __name__)

@admin.get("/area/restrita")
def restricted_area():
    user: str | None = get_logged_user()
    if user is None:
        return redirect("/area/restrita/login")

    return user


@admin.get("/area/restrita/login")
def get_login():
    return render_template("login.html")


@admin.post("/area/restrita/login")
def post_login():
    user_name = request.form.get('user')
    passwd = request.form.get('password')
    totp = request.form.get('totp')
    try:
        user: User = password.authenticate(user_name=user_name,
                                           passwd=passwd,
                                           totp_token=totp)
        session["logged_user"] = user.Name
        return redirect("/area/restrita")
    except Exception:
        return "Invalid credentials", 401


@admin.get("/area/restrita/logout")
def get_logout():
    session.pop("logged_user")
    return redirect("/area/restrita")


def get_logged_user():
    user = session.get("logged_user")
    return user