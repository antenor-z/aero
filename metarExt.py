import pandas
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def load_now():
    df = pandas.read_csv("https://aviationweather.gov/data/cache/metars.cache.csv.gz", 
                     compression='infer',
                     header=5)
    df = df[["station_id", "raw_text"]]

    for airport in df.iloc:
        BRAZIL_PREFIX = "SB"
        if airport['station_id'].startswith(BRAZIL_PREFIX):
            r.set(f"metar:{airport['station_id']}", airport["raw_text"], ex=1800)

def get_metar(icao: str) -> str | None:
    return r.get(f"metar:{icao.upper()}")

