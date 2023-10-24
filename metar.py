import requests, json
from datetime import datetime, timedelta
import re

from IcaoNotFound import IcaoNotFound
from util import is_icao_valid

cache = {}
def get_metar(icao: str) -> str:
    if not is_icao_valid(icao):
        raise IcaoNotFound(f"ICAO '{icao}' não encontrado.")
    
    metar = cache.get(icao)
    
    if metar is not None:
        [(day, hour)] = re.findall(r"(\d{2})(\d{2})\d{2}Z", metar)
        now = datetime.utcnow()
        if now.day == int(day) and now.hour == int(hour):
            return metar, "cache"

    with open("apikey.txt") as fp:
        key = fp.read()

    key = key.split("\n")[0] # Discard after \n (including newline)
    data_ini = datetime.utcnow().strftime("%Y%m%d%H")
    uma_hora = timedelta(hours=1)
    data_fim = (datetime.utcnow() + uma_hora).strftime("%Y%m%d%H")
    
    """
    resp = requests.get(f"https://api-redemet.decea.mil.br/mensagens/metar/{icao}", 
                        params={"api_key": key, 
                                "data_ini": data_ini, "data_fim": data_fim}).json()

    resp_data = resp.get("data") 
    if resp_data is not None:
        metar = resp["data"]["data"][0]["mens"]
    else:
        # Alternate
        resp = requests.get(f"https://beta.aviationweather.gov/cgi-bin/data/metar.php?ids={icao}").text
        # NGMI
        if not resp.startswith(icao):
            raise IcaoNotFound(f"Houve um problema para obter o {icao=}.")
        metar = f"METAR {resp}"
    """

    resp = requests.get(f"https://aviationweather.gov/cgi-bin/data/metar.php?ids={icao}").text
    # NGMI
    if not resp.startswith(icao):
        raise IcaoNotFound(f"Houve um problema para obter o {icao=}.")
    metar = f"METAR {resp}"
    cache[icao] = metar
    return metar, "not cache"


if __name__ == "__main__":
    print(get_metar("SBMN"))
