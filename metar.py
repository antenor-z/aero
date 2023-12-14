import requests, json
from datetime import datetime, timedelta
import re

from IcaoError import IcaoError
from util import is_icao_valid

cache = {}
def get_metar(icao: str) -> str:
    if not is_icao_valid(icao):
        raise IcaoError(f"O ICAO informado não é válido ou não é de um aeródromo brasileiro.")
    
    metar = cache.get(icao)
    
    if metar is not None:
        [(day, hour)] = re.findall(r"(\d{2})(\d{2})\d{2}Z", metar)
        now = datetime.utcnow()
        if now.day == int(day) and now.hour == int(hour):
            return "cache", metar

    resp = requests.get(f"https://aviationweather.gov/cgi-bin/data/metar.php?ids={icao}").text
    print(resp)
    if not resp.startswith(icao):
        raise IcaoError("Houve um erro ao obter a informação.")
    metar = f"METAR {resp}"
    cache[icao] = metar
    return "not cache", metar


if __name__ == "__main__":
    print(get_metar("SBMN"))
