from flask import Flask
from airportDatabase import get_info
from metarDecoder import decode
from util import is_icao_valid

app = Flask(__name__)

@app.get("/metar/<string:icao>")
def metar(icao: str):
    if not is_icao_valid(icao):
        return "fail"
    
    return decode(icao)

@app.get("/<string:icao>")
def info(icao:str):
    if not is_icao_valid(icao):
        return "fail"
    
    return get_info(icao)