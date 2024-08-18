from DB.ORM import *
from sqlalchemy import types, desc
from datetime import datetime, timezone
import re

from metarDecoder import parse_metar

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


def get_info(icao):
    with Session(engine) as session:
        aerodrome = session.get(Aerodrome, icao)
        if aerodrome is not None:
            aerodrome = model_to_dict(aerodrome)
            city = session.query(City.CityName).filter(City.CityCode == aerodrome["CityCode"]).first()
            aerodrome.pop("CityCode")
            aerodrome["City"] = city
            return aerodrome
        else:
            raise ValueError(f"Informações do ICAO '{icao}' não encontradas.")

def get_metar(icao: str) -> tuple[str, str]:
    with Session(engine) as session:
        latest_metar = session.query(METAR).filter(METAR.ICAO == icao).order_by(desc(METAR.ValidOn)).first()
        if latest_metar:
            return latest_metar.METAR, latest_metar.ValidOn.replace(tzinfo=timezone.utc)
        return None, None

def latest_n_metars(icao: str, n=10) -> list[tuple[str, str]]:
    with Session(engine) as session:
        metars = session.query(METAR).filter(METAR.ICAO == icao).order_by(METAR.ValidOn).limit(n).all()
        results = [('', '')] * n

        for i, metar in enumerate(reversed(metars)):
            results[-(i+1)] = (metar.METAR, metar.ValidOn.replace(tzinfo=timezone.utc))

        return results

def latest_n_metars_parsed(icao: str, n=10) -> list[dict]:
    metars = latest_n_metars(icao, n)
    result = []

    for metar_str, valid_on in metars:
        if metar_str:
            parsed_data = parse_metar(metar_str)
            parsed_data["timestamp"] = valid_on
            result.append(parsed_data)
        else:
            result.append(None)

    return result


def get_taf(icao: str) -> tuple[str, str]:
    with Session(engine) as session:
        latest_metar = session.query(TAF).filter(TAF.ICAO == icao).order_by(desc(TAF.ValidOn)).first()
        if latest_metar:
            return latest_metar.TAF, latest_metar.ValidOn.replace(tzinfo=timezone.utc)
        return None, None
    
def set_metar(icao: str, metar: str):
    with Session(engine) as session:
        now = datetime.now(tz=timezone.utc)
        try:
            metar_timestamp = metar.split(" ")[0]
            day = int(metar_timestamp[0:2])
            hour = int(metar_timestamp[2:4])
            minute = int(metar_timestamp[4:6])
            assert metar_timestamp[6] == "Z"
        except:
            # Fallback to not overload the API
            day = now.day
            hour = 0
            minute = 0
        
        try:
            valid_on = datetime(day=day, month=now.month, year=now.year, hour=hour, minute=minute)
            new_metar = METAR(ICAO=icao, ValidOn=valid_on, METAR=metar)
            session.add(new_metar)
            session.commit()
        except:
            pass

def set_taf(icao: str, taf: str):
    with Session(engine) as session:
        now = datetime.now(tz=timezone.utc)
        try:
            metar_timestamp = taf.split(" ")[0]
            day = int(metar_timestamp[0:2])
            hour = int(metar_timestamp[2:4])
            minute = int(metar_timestamp[4:6])
            assert metar_timestamp[6] == "Z"
        except:
            # Fallback to not overload the API
            day = now.day
            hour = 0
            minute = 0
        
        try:
            valid_on = datetime(day=day, month=now.month, year=now.year, hour=hour, minute=minute)
            new_taf = TAF(ICAO=icao, ValidOn=valid_on, TAF=taf)
            session.add(new_taf)
            session.commit()
        except:
            pass
        
def get_all_names():
    aerodromes = []
    with Session(engine) as session:
        for aerodrome in session.query(Aerodrome).all():
            city = session.query(City.CityName).filter(City.CityCode == aerodrome.CityCode).first()
            aerodromes.append((aerodrome.AerodromeName, aerodrome.ICAO, city[0]))

    return aerodromes

def get_all_icao():
    icao = []
    with Session(engine) as session:
        for aerodrome in session.query(Aerodrome).all():
            icao.append(aerodrome.ICAO)

    return icao
