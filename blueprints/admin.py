from flask import render_template, redirect, request, Blueprint, session, redirect

from DB.AdminGetter import get_runway
from DB.AdminSetter import create_runway, patch_aerodrome, patch_runway
from DB.Getter import get_info
from DB.ORM import User
from ext import get_metar
from metarDecoder import decode_metar
from security import password

admin = Blueprint('admin', __name__)

@admin.get("/area/restrita")
def restricted_area():
    user = get_logged_user()

    return user

@admin.get("/area/restrita/<string:icao>")
def restricted_area_airport(icao:str):
    get_logged_user()

    icao_upper = icao.upper()
    if icao != icao_upper:
        return redirect(f"/info/{icao_upper}")
    
    try:
        metar = get_metar(icao)
        info = get_info(icao)
        decoded = decode_metar(metar)
    except Exception:
        return render_template("error.html", error="Erro ao obter o METAR"), 400

    return render_template("airport.html", info=info, icao=icao, metar=metar, decoded=decoded, isAdmin=True)


@admin.get("/area/restrita/login")
def get_login():
    return render_template("edit/login.html")


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

class NotLoggedException(Exception):
    ...

def get_logged_user():
    user = session.get("logged_user")
    if user is None: raise NotLoggedException
    return user

@admin.route("/area/restrita/<string:icao>/edit", methods=['GET', 'POST'])
def edit_aerodrome(icao: str):
    get_logged_user()
    if request.method == 'GET':
        return render_template("admin/airport.html", icao=icao)
    else:
        aerodrome_name = request.form.get('AerodromeName')
        patch_aerodrome(icao, aerodrome_name)
        return redirect(f"/area/restrita/{icao}")

@admin.route("/area/restrita/<string:icao>/runway/add", methods=['GET', 'POST'])
def add_runway(icao: str):
    get_logged_user()
    if request.method == 'GET':
        empty_runway = {"Head1": "", "Head2": "", "RunwayLength": "", "RunwayWidth": "", "PavementCode": ""}
        return render_template("admin/runway.html", icao=icao, runway=empty_runway, action=f"/area/restrita/{icao}/runway/add")
    else:
        head1 = request.form.get('Head1')
        head2 = request.form.get('Head2')
        runway_length = request.form.get('RunwayLength')
        runway_width = request.form.get('RunwayWidth')
        pavement_code = request.form.get('PavementCode')

        if (exc := create_runway(icao, head1, head2, runway_length, runway_width, pavement_code)) is not None:
            return exc, 401
        
        return redirect(f"/area/restrita/{icao}")
    
@admin.route("/area/restrita/<string:icao>/runway/<string:runwayHead>/edit", methods=['GET', 'POST'])
def edit_runway(icao: str, runwayHead):
    get_logged_user()
    if request.method == 'GET':
        runway = get_runway(icao=icao, runway_head=runwayHead)
        return render_template("admin/runway.html", icao=icao, runway=runway, action=f"/area/restrita/{icao}/runway/{runwayHead}/edit")
    else:
        head1 = request.form.get('Head1')
        head2 = request.form.get('Head2')
        runway_length = request.form.get('RunwayLength')
        runway_width = request.form.get('RunwayWidth')
        pavement_code = request.form.get('PavementCode')

        if (exc := patch_runway(icao, runwayHead, head1, head2, runway_length, runway_width, pavement_code)) is not None:
            return exc, 401
        
        return redirect(f"/area/restrita/{icao}")
        
    
@admin.errorhandler(NotLoggedException)
def not_logged(e):
    return redirect("/area/restrita/login")