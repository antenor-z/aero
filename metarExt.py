from datetime import datetime, timezone, timedelta
from DB.Getter import get_metar as db_get_metar, set_metar as db_set_metar
import requests


def get_metar(icao: str) -> str | None:
    metar, METAR_valid_on = db_get_metar(icao=icao)
    print("get_metar() called")
    if not is_metar_valid(metar=metar, METAR_valid_on=METAR_valid_on):
        print("METAR was not valid. Updating...")
        metar = requests.get(f"https://aviationweather.gov/api/data/metar?ids={icao}").text
        metar = metar.replace("\n", "")
        metar = metar.replace(f"{icao} ", "")
        db_set_metar(icao=icao, metar=metar)
    return metar

def is_metar_valid(metar, METAR_valid_on):
    if metar is None: return False

    now = datetime.now(tz=timezone.utc)
    delta = now - METAR_valid_on

    condition = delta < timedelta(minutes=30)

    print(f"Now: {now}")
    print(f"ValidOn: {METAR_valid_on}")
    print(f"Delta: {delta}")
    print(f"Result: {condition}")

    return condition


class IcaoError(Exception):
    def __init__(self, message):
        super().__init__(message)

