from DB.ORM import *
from sqlalchemy import types, desc
from datetime import datetime, timezone

engine = create_engine(db_url, pool_pre_ping=True)


def patch_aerodrome(icao: str, aerodrome_name=None, latitude=None, longitude=None, city_code=None):
    with Session(engine) as session:
        aerodrome: Aerodrome = session.get_one(Aerodrome, icao)
        if aerodrome_name is not None:
            aerodrome.AerodromeName = aerodrome_name
        if latitude is not None:
            aerodrome.Latitude = latitude
        if longitude is not None:
            aerodrome.Latitude = longitude
        if city_code is not None:
            aerodrome.CityCode = city_code
        session.commit()

def create_runway(icao: str, head1, head2, runway_length, runway_width=None, pavement_code=None):
    with Session(engine) as session:
        runway: Runway = Runway(ICAO=icao, Head1=head1, Head2=head2, RunwayLength=runway_length, RunwayWidth=runway_width, PavementCode=pavement_code)
        try:
            session.add(runway)
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)

def patch_runway(icao: str, head1_pk, head1, head2, runway_length, runway_width=None, pavement_code=None):
    with Session(engine) as session:
        runway: Runway = session.get_one(Runway, (icao, head1_pk))
        try:
            if head1 is not None:
                runway.Head1 = head1
            if head2 is not None:
                runway.Head2 = head2
            if runway_length is not None:
                runway.RunwayLength = runway_length
            if runway_width is not None:
                runway.RunwayWidth = runway_width
            if pavement_code is not None:
                runway.PavementCode = pavement_code
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)
        
        



