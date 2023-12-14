from flask import Flask, render_template
from IcaoError import IcaoError
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
        is_cached, metar = get_metar(icao)
    except IcaoError as e:
        return render_template("error.html", error=e)
    
    try:
        info = get_info(icao)
    except IcaoError as e:
        info = None

    print(is_cached, metar)
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)