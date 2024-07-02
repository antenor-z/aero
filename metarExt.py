from datetime import datetime, timezone, timedelta
from DB.Getter import get_metar as db_get_metar, set_metar as db_set_metar
import requests


def get_metar(icao: str) -> str | None:
    metar, METAR_gotOn = db_get_metar(icao=icao)
    print("get_metar() called")
    if not is_metar_valid(metar=metar, METAR_gotOn=METAR_gotOn):
        print("METAR was not valid. Updating...")
        metar = requests.get(f"https://aviationweather.gov/api/data/metar?ids={icao}").text
        metar = metar.replace("\n", "")
        metar = metar.replace(f"{icao} ", "")
        db_set_metar(icao=icao, metar=metar)
    return metar

def is_metar_valid(metar, METAR_gotOn):
    if metar is None: return False

    now = datetime.now(tz=timezone.utc)
    delta = now - METAR_gotOn

    condition = delta < timedelta(minutes=15) or (now.minute == 0 and delta < timedelta(minutes=1))

    print("Delta is", delta, "now", now, "result:", condition)

    return condition


class IcaoError(Exception):
    def __init__(self, message):
        super().__init__(message)

