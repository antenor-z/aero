from flask import Flask, render_template
from airportDatabase import get_all_names, get_info
from metar import get_metar_only
from metarDecoder import decode
from util import is_icao_valid

app = Flask(__name__)

@app.get("/")
def list_all():
    return render_template("index.html", airports=get_all_names())

@app.get("/metar/<string:icao>")
def metar(icao: str):
    if not is_icao_valid(icao):
        return "fail"
    
    return decode(icao)

@app.get("/<string:icao>/json")
def info_json(icao:str):
    if not is_icao_valid(icao):
        return "fail"
    
    return get_info(icao)

@app.get("/<string:icao>")
def info(icao:str):
    if not is_icao_valid(icao):
        return "fail"
    
    metar = get_metar_only(icao)
    info = get_info(icao)
    return render_template("airport.html", info=info, metar=metar)
