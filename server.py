from flask import Flask
from metarDecoder import decode
from util import is_icao_valid

app = Flask(__name__)

@app.get("/<string:icao>")
def metar(icao: str):
    if not is_icao_valid(icao):
        return "fail"
    
    return decode(icao)