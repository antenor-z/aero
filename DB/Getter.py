from DB.ORM import *
from sqlalchemy import types
from datetime import datetime, timezone

engine = create_engine(db_url, pool_pre_ping=True)

def model_to_dict(instance, include_relationships=True):
    instance_dict = {}
    for column in instance.__table__.columns:
        value = getattr(instance, column.key)
        if isinstance(column.type, types.DECIMAL):
            value = float(value) if value is not None else None
        if column.key != "ICAO":
            instance_dict[column.key] = value
    
    if include_relationships:
        for name in instance.__mapper__.relationships.keys():
            related_instance = getattr(instance, name)
            if related_instance is not None:
                instance_dict[name] = [model_to_dict(related, include_relationships=False) for related in related_instance]
            else:
                instance_dict[name] = None

    return instance_dict

def adjust_frequencies(model):
    for communication in model["communication"]:
        f = communication["Frequency"]
        communication["Frequency"] = f"{f / 1000:.3f}"

    for ils in model["ils"]:
        f = ils["Frequency"]
        ils["Frequency"] = f"{f / 10:.1f}"

    for vor in model["vor"]:
        f = vor["Frequency"]
        vor["Frequency"] = f"{f / 10:.1f}"

    return model

def get_info(icao):
    with Session(engine) as session:
        aerodrome = session.get(Aerodrome, icao)
        if aerodrome is not None:
            return adjust_frequencies(model_to_dict(aerodrome))
        else:
            raise ValueError(f"Informações do ICAO '{icao}' não encontradas.")
        
def get_metar(icao: str) -> tuple[str, str]:
    with Session(engine) as session:
        aerodrome: Aerodrome = session.get(Aerodrome, icao)
        if aerodrome.METAR is None: return None, None
        METAR_gotOn = aerodrome.METAR_gotOn.replace(tzinfo=timezone.utc)
        return aerodrome.METAR, METAR_gotOn
    
def set_metar(icao: str, metar: str):
    now_utc = datetime.now(tz=timezone.utc)
    with Session(engine) as session:
        aerodrome: Aerodrome = session.get(Aerodrome, icao)
        aerodrome.METAR = metar
        try:
            metar = metar.split(" ")
            day = int(metar[0][0:2])
            hour = int(metar[0][2:4])
            minute = int(metar[0][4:6])
        except ValueError:
            day = now_utc.day
            hour = now_utc.hour
            minute = now_utc.minute

    ret = []

    ts_utc = datetime(day=day, month=now_utc.month, year=now_utc.year, hour=hour, minute=minute, tzinfo=timezone.utc)
    aerodrome.METAR_gotOn = ts_utc
    session.commit()
        
def get_all_names():
    aerodromes = []
    with Session(engine) as session:
        for aerodrome in session.query(Aerodrome).all():
            aerodromes.append((aerodrome.AerodromeName, aerodrome.ICAO, aerodrome.City))

    return aerodromes


print(get_all_names())
