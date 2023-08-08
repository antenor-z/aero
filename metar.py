import requests, json
from datetime import datetime, timedelta
import re

from ICAONotFound import ICAONotFound

cache = {}
def get_metar(icao: str) -> str:
    metar = cache.get(icao)
    
    if metar is not None:
        [(day, hour)] = re.findall(r"(\d{2})(\d{2})\d{2}Z", metar)
        now = datetime.utcnow()
        if now.day == int(day) and now.hour == int(hour):
            return metar, "cache"

    with open("apikey.txt") as fp:
        key = fp.read()
    data_ini = datetime.utcnow().strftime("%Y%m%d%H")
    uma_hora = timedelta(hours=1)
    data_fim = (datetime.utcnow() + uma_hora).strftime("%Y%m%d%H")
    resp = requests.get(f"https://api-redemet.decea.mil.br/mensagens/metar/{icao}", 
                        params={"api_key": key, 
                                "data_ini": data_ini, "data_fim": data_fim})

    resp_dict = json.loads(resp.text)
    if resp_dict['data']['total'] == 0:
        raise ICAONotFound(f"ICAO '{icao}' não encontrado.")
    
    metar = resp_dict["data"]["data"][0]["mens"]

    cache[icao] = metar
    return metar, "not cache"

def get_metar_only(icao: str) -> str:
    metar, is_cached = get_metar(icao)
    return re.findall(icao.upper() + "(.*?)=", metar)[0], is_cached

if __name__ == "__main__":
    print(get_metar("SBMN"))