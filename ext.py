from datetime import datetime
from DB.Getter import get_all_icao, get_metar as db_get_metar, \
                      get_taf as db_get_taf, \
                      set_metar as db_set_metar, \
                      set_taf as db_set_taf
import requests

from red import trash_it


async def update_metars():
    print("METAR update started at", datetime.now())
    icao_list = get_all_icao()
    icao_list_str = ",".join(icao_list)
    metars = requests.get(f"https://aviationweather.gov/api/data/metar?ids={icao_list_str}").text.split("\n")
    for metar in metars:
        if len(metar) < 5:
            continue
        icao = metar[0:4]
        metar = metar[5:]
        db_set_metar(icao=icao, metar=metar)
        await trash_it(icao)
        print(f"{icao}: {metar}")
    print("METAR update ended at", datetime.now())

async def update_tafs():
    print("TAF update started at", datetime.now())
    icao_list = get_all_icao()
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
        await trash_it(icao)
    print("TAF update ended at", datetime.now())


async def get_metar(icao: str) -> str | None:
    metar, _ = await db_get_metar(icao=icao)
    return metar

async def get_taf(icao: str) -> str | None:
    metar, _ = await db_get_taf(icao=icao)
    return metar


class IcaoError(Exception):
    def __init__(self, message):
        super().__init__(message)

