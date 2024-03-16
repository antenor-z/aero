import pandas
import redis

r = redis.Redis(host='redis', port=6379, decode_responses=True)

def load_now():
    df = pandas.read_csv("https://aviationweather.gov/data/cache/metars.cache.csv.gz", 
                     compression='infer',
                     header=5)
    df = df[["station_id", "raw_text"]]

    for airport in df.iloc:
        BRAZIL_PREFIX = "SB"
        if airport['station_id'].startswith(BRAZIL_PREFIX):
            metar = airport["raw_text"].replace(airport['station_id'] + " ", "")
            r.set(f"metar:{airport['station_id']}", metar, ex=1800)

def get_metar(icao: str) -> str | None:
    metar = r.get(f"metar:{icao.upper()}")
    if metar is None:
        raise IcaoError("Aeroporto não encontrado.")
    return metar

class IcaoError(Exception):
    def __init__(self, message):
        super().__init__(message)

