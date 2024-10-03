import redis, json

client = redis.Redis(host='redis', port=6379, decode_responses=True)

def cache_it(func):
    def wrapper(*args, **kargs):
        icao = kargs.get("icao") or args[0: 1] or "default"
        key = f'{icao}:{func.__name__}'
        cached = json.loads(client.get(key) or "null")
        if not cached:
            cached = func(*args, **kargs)
            client.set(key, json.dumps(cached))
        return cached            
    return wrapper

def trash_it(icao):
    for k in client.scan_iter(f"{icao}:*"):
        client.delete(k)