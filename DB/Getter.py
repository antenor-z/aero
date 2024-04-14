from DB.ORM import *
from sqlalchemy import types

Session = sessionmaker(bind=engine)
session = Session()

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
    aerodrome = session.get(Aerodrome, icao)
    if aerodrome is not None:
        return model_to_dict(aerodrome) 
    else:
        raise ValueError(f"Informações do ICAO '{icao}' não encontradas.")
    
def get_all_names():
    aerodromes = []
    for aerodrome in session.query(Aerodrome).all():
        aerodromes.append((aerodrome.AerodromeName, aerodrome.ICAO, aerodrome.City))

    return aerodromes


print(get_all_names())