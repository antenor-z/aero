import time
import pandas
import redis
from datetime import datetime

try:
    r = redis.Redis(host='redis', port=6379, decode_responses=True)
    r.keys("a")
except redis.exceptions.ConnectionError:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def download_ext():
    while True:
        minute = datetime.now().minute
        second = datetime.now().second
        if (minute % 10 == 0) and second == 0:
            try:
                load_now()
            except:
                # If any problem occours, ignore and download nothing
                pass
        time.sleep(40)
        
def load_now():
    print("Downloading METARs", datetime.now())
    df = pandas.read_csv("https://aviationweather.gov/data/cache/metars.cache.csv.gz", 
                     compression='infer',
                     header=5)
    df = df[["station_id", "raw_text"]]

    for airport in df.iloc:
        BRAZIL_PREFIX = "SB"
        if airport['station_id'].startswith(BRAZIL_PREFIX):
            metar = airport["raw_text"].replace(airport['station_id'] + " ", "")
            print(metar)
            r.set(f"metar:{airport['station_id']}", metar)
    print("Done")

def get_metar(icao: str) -> str | None:
    metar = r.get(f"metar:{icao.upper()}")
    if metar is None:
        raise IcaoError("Aeroporto não encontrado.")
    return metar

class IcaoError(Exception):
    def __init__(self, message):
        super().__init__(message)

