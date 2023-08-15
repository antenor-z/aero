from flask import Flask, render_template
from IcaoNotFound import IcaoNotFound
from airportDatabase import get_all_names, get_info
from metar import get_metar
from metarDecoder import decode
app = Flask(__name__)

@app.get("/")
def list_all():
    return render_template("index.html", airports=get_all_names())


@app.get("/<string:icao>")
def info(icao:str):
    icao = icao.upper()
    
    try:
        metar = get_metar(icao)
        info = get_info(icao)
    except IcaoNotFound as e:
        return render_template("error.html", error=e)

    try:
        metar_only = metar[0]
        decoded = decode(metar_only)
    except:
        return render_template("error.html", error="Erro ao decodificar o METAR")

    return render_template("airport.html", info=info, metar=metar, decoded=decoded)
