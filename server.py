from flask import Flask, render_template
from IcaoNotFound import IcaoNotFound
from airportDatabase import get_all_names, get_info
from metar import get_metar
from metarDecoder import decode, get_wind_info
from wind.Wind import get_runway_in_use
app = Flask(__name__)

@app.get("/")
def list_all():
    return render_template("index.html", airports=get_all_names())


@app.get("/info/<string:icao>")
def info(icao:str):
    icao = icao.upper()
    
    try:
        metar = get_metar(icao)
        info = get_info(icao)
    except IcaoNotFound as e:
        return render_template("error.html", error=e)

    #try:
    print(metar)
    metar_only = metar[0]
    decoded = decode(metar_only)
    #except:
    #return render_template("error.html", error="Erro ao decodificar o METAR")
    
    runways_list = []
    for rwy in info["rwy"]:
        runways_list.append(rwy["head"][0])
        runways_list.append(rwy["head"][1])

    #return runways_list

    try:
        wind = get_wind_info(metar[0])
        rwy_in_use = get_runway_in_use(runways_list, wind_dir=wind["direction"], wind_speed=wind["speed"])
    except:
        rwy_in_use = None

    return render_template("airport.html", info=info, metar=metar, decoded=decoded, rwy_in_use=rwy_in_use)
