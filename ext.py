from datetime import datetime
from DB.Getter import get_metar as db_get_metar, \
                      get_taf as db_get_taf, \
                      set_metar as db_set_metar, \
                      set_taf as db_set_taf
import requests


def update_metars(icao_list):
    print("METAR update started at", datetime.now())
    icao_list_str = ",".join(icao_list)
    metars = requests.get(f"https://aviationweather.gov/api/data/metar?ids={icao_list_str}").text.split("\n")
    for metar in metars:
        if len(metar) < 5:
            continue
        icao = metar[0:4]
        metar = metar[5:]
        db_set_metar(icao=icao, metar=metar)
        print(f"{icao}: {metar}")
    print("METAR update ended at", datetime.now())

def update_tafs(icao_list):
    print("TAF update started at", datetime.now())
    icao_list_str = ",".join(icao_list)
    tafs = requests.get(f"https://aviationweather.gov/api/data/taf?ids={icao_list_str}").text.split("TAF ")
    for taf in tafs:
        if len(taf) < 9:
            continue
        icao = taf[0:4]
        taf = taf[5:]
        if taf[-1] == "\n": taf = taf[:-1]
        db_set_taf(icao=icao, taf=taf)
        print(f"{icao}: {taf}")
    print("TAF update ended at", datetime.now())


def get_metar(icao: str) -> str | None:
    metar, _ = db_get_metar(icao=icao)
    return metar

def get_taf(icao: str) -> str | None:
    metar, _ = db_get_taf(icao=icao)
    return metar


class IcaoError(Exception):
    def __init__(self, message):
        super().__init__(message)

