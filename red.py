from datetime import datetime
import redis, json

client = redis.Redis(host='redis', port=6379, decode_responses=True)

def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def datetime_parser(dct):
    for key, value in dct.items():
        try:
            dct[key] = datetime.fromisoformat(value)
        except (ValueError, TypeError):
            pass
    return dct

def cache_it(func):
    def wrapper(*args, **kargs):
        try:
            icao = kargs.get("icao") or args[0]
        except IndexError:
            icao = "default"
        key = f'{icao}:{func.__name__}'
        print(key, end=" :: ")
        cached = json.loads(client.get(key) or "null", object_hook=datetime_parser)
        if not cached:
            cached = func(*args, **kargs)
            client.set(key, json.dumps(cached, default=datetime_serializer), ex=3600)
            print("miss", cached)
        else:
            print("hit", cached)
        return cached            
    return wrapper

def trash_it(icao):
    for k in client.scan_iter(f"{icao}:*"):
        client.delete(k)