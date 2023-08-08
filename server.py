from flask import Flask, render_template
from ICAONotFound import ICAONotFound
from airportDatabase import get_all_names, get_info
from metar import get_metar_only
from metarDecoder import decode
from util import is_icao_valid

app = Flask(__name__)

@app.get("/")
def list_all():
    return render_template("index.html", airports=get_all_names())


@app.get("/<string:icao>")
def info(icao:str):
    icao = icao.upper()
    
    if not is_icao_valid(icao):
        return render_template("error.html", error=f"ICAO '{icao}' não encontrado.")
    
    try:
        metar = get_metar_only(icao)
        info = get_info(icao)
    except ICAONotFound as e:
        return render_template("error.html", error=e)

    return render_template("airport.html", info=info, metar=metar)
