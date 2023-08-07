from flask import Flask, render_template
from airportDatabase import get_info
from metar import get_metar, get_metar_only
from metarDecoder import decode
from util import is_icao_valid

app = Flask(__name__)

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
    return render_template("template.html", info=info, metar=metar)
