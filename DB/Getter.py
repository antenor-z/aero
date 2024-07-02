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
    with Session(engine) as session:
        aerodrome: Aerodrome = session.get(Aerodrome, icao)
        ts_utc = datetime.now(tz=timezone.utc)
        aerodrome.METAR = metar
        aerodrome.METAR_gotOn = ts_utc
        session.commit()
        print(f"setting METAR '{metar}' for {icao}. Received on {ts_utc}")
        
def get_all_names():
    aerodromes = []
    with Session(engine) as session:
        for aerodrome in session.query(Aerodrome).all():
            aerodromes.append((aerodrome.AerodromeName, aerodrome.ICAO, aerodrome.City))

    return aerodromes


print(get_all_names())
