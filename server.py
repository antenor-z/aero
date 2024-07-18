from os import environ
from flask import Flask, render_template, redirect, request, session
from DB.Getter import get_all_icao, get_all_names, get_info
from DB.ORM import User
from ext import IcaoError, get_metar, update_metars, update_tafs, get_taf
from metarDecoder import DecodeError, decode_metar, get_wind_info
from tafDecoder import decode_taf
from wind.Wind import get_components, get_components_one_runway, get_wind
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from security import password

scheduler = BackgroundScheduler()
scheduler.add_job(update_metars, CronTrigger(minute='0,8,21,41'), args=[get_all_icao()])
scheduler.add_job(update_tafs, CronTrigger(minute='10'), args=[get_all_icao()])
scheduler.start()

app = Flask(__name__)
DB_PASSWORD = None
with open(environ["SESSION_SECRET_KEY"]) as fp:
    app.config['SECRET_KEY'] = fp.read()

@app.get("/")
def list_all():
    return render_template("index.html", airports=get_all_names())

@app.get("/info/<string:icao>")
def info(icao:str):
    icao_upper = icao.upper()
    if icao != icao_upper:
        return redirect(f"/info/{icao_upper}")
    
    try:
        metar = get_metar(icao)
        info = get_info(icao)
        decoded = decode_metar(metar)
    except Exception:
        return render_template("error.html", error="Erro ao obter o METAR"), 400

    return render_template("airport.html", info=info, icao=icao, metar=metar, decoded=decoded)

@app.get("/info/taf/<string:icao>")
def info_taf(icao:str):
    icao_upper = icao.upper()
    if icao != icao_upper:
        return redirect(f"/info/taf/{icao_upper}")

    try:
        taf = get_taf(icao)
        info = get_info(icao)
        decoded = decode_taf(taf)
    except Exception:
        return render_template("error.html", error="Erro ao obter o TAF"), 400

    return render_template("taf.html", info=info, icao=icao, taf=taf, decoded=decoded)

@app.get("/wind/")
def wind():
    return render_template("wind.html")


@app.get("/windcalc/")
def windcalc():
    try:
        runway_head = int(request.args["runway_head"])
        wind_dir = int(request.args["wind_dir"])
        wind_speed = int(request.args["wind_speed"])
    except KeyError:
        return {"error": "mising args"}, 400
    except ValueError:
        return {"error": "invalid args"}, 400

    ret = get_components_one_runway(
        runway_head=runway_head,
        wind_dir=wind_dir,
        wind_speed=wind_speed)
    return ret


@app.get("/descent")
def descent():
    return render_template("vertical.html")

@app.get("/area/restrita")
def restricted_area():
    user: str | None = get_logged_user()
    if user is None:
        return redirect("/area/restrita/login")

    return user


@app.get("/area/restrita/login")
def get_login():
    return render_template("login.html")

@app.post("/area/restrita/login")
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

@app.get("/area/restrita/logout")
def get_logout():
    session.pop("logged_user")
    return redirect("/area/restrita")

def get_logged_user():
    user = session.get("logged_user")
    return user

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", error="404 | Página não encontrada."), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
