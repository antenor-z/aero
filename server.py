import threading
from flask import Flask, render_template
from airportDatabase import InfoError, get_all_names, get_info
from metarExt import IcaoError, get_metar, load_every_30_minutes
from metarDecoder import DecodeError, decode, get_wind_info
from wind.Wind import get_runway_in_use
app = Flask(__name__)

thread = threading.Thread(target=load_every_30_minutes, daemon=True)
thread.start()

@app.get("/")
def list_all():
    return render_template("index.html", airports=get_all_names())

@app.get("/info/<string:icao>")
def info(icao:str):
    icao = icao.upper()
    
    try:
        metar = get_metar(icao)
    except IcaoError as e:
        return render_template("error.html", error=e), 400
    
    try:
        info = get_info(icao)
    except InfoError as e:
        info = None

    decoded = decode(metar)
    
    rwy_in_use = None
    if info is not None:
        runways_list = []
        for rwy in info["rwy"]:
            runways_list.append(rwy["head"][0])
            runways_list.append(rwy["head"][1])
    
        try:
            wind = get_wind_info(metar[0])
            rwy_in_use = get_runway_in_use(runways_list, wind_dir=wind["direction"], wind_speed=wind["speed"])
        except:
            rwy_in_use = None

    return render_template("airport.html", info=info, icao=icao, metar=metar, decoded=decoded, rwy_in_use=rwy_in_use)

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", error="404 | Página não encontrada."), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)