from datetime import datetime, timezone, timedelta
from DB.Getter import get_metar as db_get_metar, set_metar as db_set_metar
import requests


def get_metar(icao: str) -> str | None:
    metar, METAR_gotOn = db_get_metar(icao=icao)
    if not is_metar_valid(metar=metar, METAR_gotOn=METAR_gotOn):
        metar = requests.get(f"https://aviationweather.gov/api/data/metar?ids={icao}").text
        metar = metar.replace("\n", "")
        metar = metar.replace(f"{icao} ", "")
        db_set_metar(icao=icao, metar=metar)
    return metar

def is_metar_valid(metar, METAR_gotOn):
    if metar is None: return False

    # Check if no more than 1 hour has passed
    now = datetime.now(tz=timezone.utc)
    delta = now - METAR_gotOn
    print("Delta is", delta, "result:", delta < timedelta(hours=1) and now.hour == METAR_gotOn.hour)

    return delta < timedelta(hours=1) and now.hour == METAR_gotOn.hour


class IcaoError(Exception):
    def __init__(self, message):
        super().__init__(message)

