from DB.ORM import *
from sqlalchemy import types, desc
from datetime import datetime, timezone

engine = create_engine(db_url, pool_pre_ping=True)

def get_aerodrome(icao: str):
    with Session(engine) as session:
        aerodrome: Aerodrome = session.get_one(Aerodrome, icao)
        city: City = session.get_one(City, aerodrome.CityCode)
        return {
           "ICAO": aerodrome.ICAO,
           "AerodromeName": aerodrome.AerodromeName,
           "CityCode": aerodrome.CityCode,
           "CityName": city.CityName,
           "StateCode": city.StateCode, 
           "Latitude": aerodrome.Latitude,
           "Longitude": aerodrome.Longitude,
        }
    
def get_cities():
    with Session(engine) as session:
        cities: list[City] = session.query(City).all()
        return [{"City": city.CityName, "CityCode": city.CityCode} for city in cities]

def get_runway(icao: str, runway_head: str):
    with Session(engine) as session:
        runway: Runway = session.get_one(Runway, (icao, runway_head))
        return {
           "ICAO": runway.ICAO,
           "Head1": runway.Head1,
           "Head2": runway.Head2,
           "RunwayLength": runway.RunwayLength,
           "RunwayWidth": runway.RunwayWidth,
           "PavementCode": runway.PavementCode
        }

def get_communication(icao: str, frequency: int):
    with Session(engine) as session:
        communication: Communication = session.get_one(Communication, (icao, frequency))
        return {
            "Frequency": communication.Frequency,
            "CommType": communication.CommType
        }

def get_ils(icao: str, frequency: int):
    with Session(engine) as session:
        ils: ILS = session.get_one(ILS, (icao, frequency))
        return {
            "ICAO": ils.ICAO,
            "Ident": ils.Ident,
            "RunwayHead": ils.RunwayHead,
            "Frequency": ils.Frequency,
            "Category": ils.Category,
            "CRS": ils.CRS,
            "Minimum": ils.Minimum
        }
    
def get_vor(icao: str, frequency: int):
    with Session(engine) as session:
        ils: VOR = session.get_one(VOR, (icao, frequency))
        return {
            "ICAO": ils.ICAO,
            "Ident": ils.Ident,
            "Frequency": ils.Frequency
        }

def get_pavement_codes():
    with Session(engine) as session:
        pavs: list[PavementType] = session.query(PavementType).all()
        return [{"Code": pav.Code, "Material": pav.Material} for pav in pavs]
    
def get_comm_types():
    with Session(engine) as session:
        comms: list[CommunicationType] = session.query(CommunicationType).all()
        return [{"CommType": comm.CommType} for comm in comms]

def get_ils_categories():
    with Session(engine) as session:
        ils_cats: list[ILSCategory] = session.query(ILSCategory).all()
        return [cat.Category for cat in ils_cats]
    
def get_user(username):
    with Session(engine) as session:
        user: User = session.query(User).filter(User.Name == username).one_or_none()
        return user
    
def get_states():
    states = []
    with Session(engine) as session:
        for state in session.query(State).all():
            states.append({
                "StateCode": state.StateCode,
                "StateName": state.StateName,
                "StateAbbreviation": state.StateAbbreviation})

    return states

def get_city(state_code, city_name):
    with Session(engine) as session:
        return session.query(City).filter(City.CityName == city_name).\
        filter(City.StateCode == state_code).first()

