from datetime import datetime, timezone, timedelta
from time import sleep
from DB.Getter import get_metar as db_get_metar, set_metar as db_set_metar
import requests

def update_metars(icao_list):
    print("METAR update start")
    for icao in icao_list:
        metar = requests.get(f"https://aviationweather.gov/api/data/metar?ids={icao}").text
        metar = metar.replace("\n", "")
        metar = metar.replace(f"{icao} ", "")
        db_set_metar(icao=icao, metar=metar)
        print(f"{icao}: {metar}")
        sleep(1)
    print("METAR update end")

def get_metar(icao: str) -> str | None:
    metar, _ = db_get_metar(icao=icao)
  
    return metar


class IcaoError(Exception):
    def __init__(self, message):
        super().__init__(message)

