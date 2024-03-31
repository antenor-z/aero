import threading
from flask import Flask, render_template, redirect
from airportDatabase import InfoError, get_all_names, get_info
from metarExt import IcaoError, get_metar, load_every_10_minutes, load_now
from metarDecoder import DecodeError, decode, get_wind_info
from wind.Wind import get_components, get_wind
app = Flask(__name__)

thread = threading.Thread(target=load_every_10_minutes, daemon=True)
thread.start()

load_now()

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
    except IcaoError as e:
        return render_template("error.html", error=e), 400
    
    try:
        info = get_info(icao)
    except InfoError as e:
        return render_template("error.html", error=e), 400

    decoded = decode(metar)

    return render_template("airport.html", info=info, icao=icao, metar=metar, decoded=decoded)

@app.get("/wind/<string:icao>")
def wind(icao:str):
    icao_upper = icao.upper()
    if icao != icao_upper:
        return redirect(f"/wind/{icao_upper}")
    
    try:
        metar = get_metar(icao)
    except IcaoError as e:
        return render_template("error.html", error=e), 400
    
    wind_direction, wind_speed = get_wind(metar)
    
    try:
        info = get_info(icao)
    except InfoError as e:
        info = None

    get_components(icao, metar)
    return render_template("wind.html", runways=get_components(icao, metar), 
                           nome_aeroporto=info["nome"], 
                           icao=icao,
                           wind_direction=wind_direction,
                           wind_speed=wind_speed,
                           lat=info["lat"],
                           lon=info["lon"])
@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", error="404 | Página não encontrada."), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
