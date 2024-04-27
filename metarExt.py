from datetime import datetime, timezone, timedelta
from DB.Getter import get_metar as db_get_metar, set_metar as db_set_metar
import requests


def get_metar(icao: str) -> str | None:
    metar = db_get_metar(icao=icao)
    if not is_metar_valid(metar=metar):
        metar = requests.get(f"https://aviationweather.gov/api/data/metar?ids={icao}").text
        metar = metar.replace("\n", "")
        metar = metar.replace(f"{icao} ", "")
        db_set_metar(icao=icao, metar=metar)
    return metar

def is_metar_valid(metar):
    if metar is None: return False

    # Check if no more than 1 hour has passed
    metar = metar.split(" ")
    day = int(metar[0][0:2])
    hour = int(metar[0][2:4])
    minute = int(metar[0][4:6])
    now = datetime.now(tz=timezone.utc)
    ts_metar = datetime(day=day, month=now.month, year=now.year, hour=hour, minute=minute, tzinfo=timezone.utc)
    delta = now - ts_metar

    return delta < timedelta(hours=1)


class IcaoError(Exception):
    def __init__(self, message):
        super().__init__(message)

