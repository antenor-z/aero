from flask import render_template, redirect, request, Blueprint, session, redirect

from DB.AdminGetter import get_comm_types, get_communication, get_ils, get_pavement_codes, get_runway, get_vor
from DB.AdminSetter import create_comm, create_ils, create_runway, create_vor, del_comm, del_ils, del_runway, del_vor, patch_aerodrome, patch_ils, patch_runway, patch_comm, patch_vor
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
    return render_template("admin/login.html")


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
        print(get_pavement_codes())
        return render_template("admin/runway.html",
                               icao=icao,
                               runway=empty_runway,
                               action=f"/area/restrita/{icao}/runway/add",
                               pavementCodes=get_pavement_codes())
    else:
        head1 = request.form.get('Head1')
        head2 = request.form.get('Head2')
        runway_length = request.form.get('RunwayLength')
        runway_width = request.form.get('RunwayWidth')
        pavement_code = request.form.get('PavementCode')

        if (exc := create_runway(icao=icao, 
                                 head1=head1, 
                                 head2=head2, 
                                 runway_length=runway_length, 
                                 runway_width=runway_width, 
                                 pavement_code=pavement_code)) is not None:
            return exc, 401
        
        return redirect(f"/area/restrita/{icao}")
    
@admin.route("/area/restrita/<string:icao>/runway/<string:runwayHead>/edit", methods=['GET', 'POST'])
def edit_runway(icao: str, runwayHead):
    get_logged_user()
    if request.method == 'GET':
        runway = get_runway(icao=icao, runway_head=runwayHead)
        return render_template("admin/runway.html",
                               icao=icao,
                               runway=runway,
                               action=f"/area/restrita/{icao}/runway/{runwayHead}/edit",
                               pavementCodes=get_pavement_codes())
    else:
        head1 = request.form.get('Head1')
        head2 = request.form.get('Head2')
        runway_length = request.form.get('RunwayLength')
        runway_width = request.form.get('RunwayWidth')
        pavement_code = request.form.get('PavementCode')

        if (exc := patch_runway(icao=icao, 
                                head1_old=runwayHead, 
                                head1=head1, 
                                head2=head2, 
                                runway_length=runway_length, 
                                runway_width=runway_width, 
                                pavement_code=pavement_code)) is not None:
            return exc, 401
        
        return redirect(f"/area/restrita/{icao}")

@admin.post("/area/restrita/<string:icao>/runway/<string:runwayHead>/delete")
def delete_runway(icao: str, runwayHead: str):
    get_logged_user()
    del_runway(icao, runwayHead)
    return redirect(f"/area/restrita/{icao}")

@admin.route("/area/restrita/<string:icao>/communication/add", methods=['GET', 'POST'])
def add_communication(icao: str):
    get_logged_user()
    if request.method == 'GET':
        empty_comm = {"Frequency": "", "CommType": ""}
        return render_template("admin/communication.html",
                               icao=icao,
                               communication=empty_comm,
                               action=f"/area/restrita/{icao}/communication/add",
                               CommTypes=get_comm_types())
    else:
        frequency = request.form.get('Frequency')
        comm_type = request.form.get('CommType')

        if (exc := create_comm(icao=icao, frequency=frequency, comm_type=comm_type)) is not None:
            return exc, 401

        return redirect(f"/area/restrita/{icao}")

@admin.route("/area/restrita/<string:icao>/communication/<int:frequency>/edit", methods=['GET', 'POST'])
def edit_communication(icao: str, frequency: int):
    get_logged_user()
    if request.method == 'GET':
        communication = get_communication(icao=icao, frequency=frequency)
        return render_template("admin/communication.html",
                               icao=icao,
                               communication=communication,
                               action=f"/area/restrita/{icao}/communication/{frequency}/edit",
                               CommTypes=get_comm_types())
    else:
        frequency_new = request.form.get('Frequency')
        comm_type = request.form.get('CommType')

        if (exc := patch_comm(icao, frequency, frequency_new, comm_type)) is not None:
            return exc, 401
        
        return redirect(f"/area/restrita/{icao}")


@admin.post("/area/restrita/<string:icao>/communication/<int:frequency>/delete")
def delete_communication(icao: str, frequency: int):
    get_logged_user()
    del_comm(icao, frequency)
    return redirect(f"/area/restrita/{icao}")

@admin.route("/area/restrita/<string:icao>/ils/add", methods=['GET', 'POST'])
def add_ils(icao: str):
    get_logged_user()
    if request.method == 'GET':
        ils = {"Ident": "", 
               "RunwayHead": "",
               "Frequency": "",
               "Category": "",
               "CRS": "",
               "Minimum": ""}
        return render_template("admin/ils.html", icao=icao, ils=ils, action=f"/area/restrita/{icao}/ils/add")
    else:
        ident = request.form.get('Ident')
        runway_head = request.form.get('RunwayHead')
        frequency = request.form.get('Frequency')
        category = request.form.get('Category')
        crs = request.form.get('CRS')
        minimum = request.form.get('Minimum')

        if (exc := create_ils(icao=icao,
                              ident=ident, 
                              runway_head=runway_head, 
                              frequency=frequency, 
                              category=category, 
                              crs=crs, 
                              minimum=minimum)) is not None:
            return exc, 401

        return redirect(f"/area/restrita/{icao}")

@admin.route("/area/restrita/<string:icao>/ils/<int:frequency>/edit", methods=['GET', 'POST'])
def edit_ils(icao: str, frequency: int):
    get_logged_user()
    if request.method == 'GET':
        ils = get_ils(icao=icao, frequency=frequency)
        return render_template("admin/ils.html", icao=icao, ils=ils, action=f"/area/restrita/{icao}/ils/{frequency}/edit")
    else:
        ident = request.form.get('Ident')
        runway_head = request.form.get('RunwayHead')
        frequency_new = request.form.get('Frequency')
        category = request.form.get('Category')
        crs = request.form.get('CRS')
        minimum = request.form.get('Minimum')

        if (exc := patch_ils(icao=icao,
                            frequency_old=frequency,
                            ident=ident,
                            runway_head=runway_head,
                            frequency=frequency_new,
                            category=category,
                            crs=crs,
                            minimum=minimum)) is not None:
            return exc, 401
        
        return redirect(f"/area/restrita/{icao}")


@admin.post("/area/restrita/<string:icao>/ils/<int:frequency>/delete")
def delete_ils(icao: str, frequency: int):
    get_logged_user()
    del_ils(icao, frequency)
    return redirect(f"/area/restrita/{icao}")

@admin.route("/area/restrita/<string:icao>/vor/add", methods=['GET', 'POST'])
def add_vor(icao: str):
    get_logged_user()
    if request.method == 'GET':
        vor = {"Ident": "", 
               "Frequency": "",
              }
        return render_template("admin/vor.html", icao=icao, vor=vor, action=f"/area/restrita/{icao}/vor/add")
    else:
        ident = request.form.get('Ident')
        frequency = request.form.get('Frequency')

        if (exc := create_vor(icao=icao,
                              ident=ident, 
                              frequency=frequency, 
                            )) is not None:
            return exc, 401

        return redirect(f"/area/restrita/{icao}")

@admin.route("/area/restrita/<string:icao>/vor/<int:frequency>/edit", methods=['GET', 'POST'])
def edit_vor(icao: str, frequency: int):
    get_logged_user()
    if request.method == 'GET':
        vor = get_vor(icao=icao, frequency=frequency)
        return render_template("admin/vor.html", icao=icao, vor=vor, action=f"/area/restrita/{icao}/vor/{frequency}/edit")
    else:
        ident = request.form.get('Ident')
        frequency_new = request.form.get('Frequency')

        if (exc := patch_vor(icao=icao,
                            frequency_old=frequency,
                            ident=ident,
                            frequency=frequency_new,
                            )) is not None:
            return exc, 401
        
        return redirect(f"/area/restrita/{icao}")


@admin.post("/area/restrita/<string:icao>/vor/<int:frequency>/delete")
def delete_vor(icao: str, frequency: int):
    get_logged_user()
    del_vor(icao, frequency)
    return redirect(f"/area/restrita/{icao}")

@admin.errorhandler(NotLoggedException)
def not_logged(e):
    return redirect("/area/restrita/login")