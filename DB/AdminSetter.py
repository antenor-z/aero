from DB.ORM import *
from sqlalchemy import types, desc
from datetime import datetime, timezone

engine = create_engine(db_url, pool_pre_ping=True)

def create_city(city_code, city_name):
    with Session(engine) as session:
        try:
            city: City = City(CityCode=city_code, CityName=city_name)
            session.add(city)
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)

def create_aerodrome(icao: str, aerodrome_name=None, latitude=None, longitude=None, city_code=None):
    with Session(engine) as session:
        try:
            aerodrome: Aerodrome = Aerodrome(
                AerodromeName=aerodrome_name,
                Latitude=latitude,
                Longitude=longitude,
                CityCode=city_code,
            )
            session.add(aerodrome)
        except Exception as e:
            session.rollback()
            return str(e)
        
def patch_aerodrome(icao: str, aerodrome_name=None, latitude=None, longitude=None, city_code=None):
    with Session(engine) as session:
        try:
            aerodrome: Aerodrome = session.get_one(Aerodrome, icao)
            aerodrome.AerodromeName = aerodrome_name
            aerodrome.Latitude = latitude
            aerodrome.Longitude = longitude
            aerodrome.CityCode = city_code
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)

def create_runway(icao: str, head1, head2, runway_length, runway_width=None, pavement_code=None):
    with Session(engine) as session:
        try:
            runway: Runway = Runway(ICAO=icao, Head1=head1, Head2=head2, RunwayLength=runway_length, RunwayWidth=runway_width, PavementCode=pavement_code)
            session.add(runway)
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)

def patch_runway(icao: str, head1_old, head1, head2, runway_length, runway_width=None, pavement_code=None):
    with Session(engine) as session:
        try:
            runway: Runway = session.get_one(Runway, (icao, head1_old))
            runway.Head1 = head1
            runway.Head2 = head2
            runway.RunwayLength = runway_length
            runway.RunwayWidth = runway_width
            runway.PavementCode = pavement_code
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)

def del_runway(icao: str, runway_head):
    with Session(engine) as session:
        try:
            runway: Runway = session.get_one(Runway, (icao, runway_head))
            session.delete(runway)
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)

def create_comm(icao, frequency, comm_type):
    with Session(engine) as session:
        try:
            communication: Communication = Communication(ICAO=icao, Frequency=float(frequency), CommType=comm_type)
            session.add(communication)
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)

def patch_comm(icao: str, frequency_old, frequency, comm_type):
    with Session(engine) as session:
        try:
            communication: Communication = session.get_one(Communication, (icao, frequency_old))
            if frequency is not None:
                communication.Frequency = float(frequency)
            if comm_type is not None:
                communication.CommType = comm_type
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)
  
def del_comm(icao: str, frequency):
    with Session(engine) as session:
        try:
            communication: Communication = session.get_one(Communication, (icao, frequency))
            session.delete(communication)
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)

def create_ils(icao, ident, runway_head, frequency, category, crs, minimum):
    with Session(engine) as session:
        ils: ILS =  ILS(ICAO=icao, 
                        Ident=ident, 
                        RunwayHead=runway_head, 
                        Frequency=frequency, 
                        Category=category, 
                        CRS=crs, 
                        Minimum=minimum)
        try:
            session.add(ils)
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)

def patch_ils(icao, frequency_old, ident, runway_head, frequency, category, crs, minimum):
    with Session(engine) as session:
        try:
            ils: ILS = session.get_one(ILS, (icao, frequency_old))
            ils.Ident = ident
            ils.RunwayHead = runway_head
            ils.Frequency = frequency
            ils.Category = category
            ils.CRS = crs
            ils.Minimum = minimum
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)
        
def del_ils(icao: str, frequency):
    with Session(engine) as session:
        try:
            ils: ILS = session.get_one(ILS, (icao, frequency))
            session.delete(ils)
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)
        
def create_vor(icao, ident, frequency):
    with Session(engine) as session:
        vor: VOR =  VOR(ICAO=icao, 
                        Ident=ident, 
                        Frequency=frequency)
        try:
            session.add(vor)
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)  
        
def patch_vor(icao, frequency_old, ident, frequency):
    with Session(engine) as session:
        try:
            vor: VOR = session.get_one(VOR, (icao, frequency_old))
            vor.Ident = ident
            vor.Frequency = frequency
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)

def del_vor(icao: str, frequency):
    with Session(engine) as session:
        try:
            vor: VOR = session.get_one(VOR, (icao, frequency))
            session.delete(vor)
            session.commit()
        except Exception as e:
            session.rollback()
            return str(e)