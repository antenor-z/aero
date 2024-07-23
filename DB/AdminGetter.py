from DB.ORM import *
from sqlalchemy import types, desc
from datetime import datetime, timezone

engine = create_engine(db_url, pool_pre_ping=True)


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
