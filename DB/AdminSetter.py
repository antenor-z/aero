from DB.ORM import *
from sqlalchemy import types, desc
from datetime import datetime, timezone

from red import trash_it

engine = create_engine(db_url, pool_pre_ping=True)

def create_city(city_code, city_name, state_code):
    with Session(engine) as session:
        try:
            city: City = City(CityCode=city_code, CityName=city_name, StateCode=state_code)
            session.add(city)
            session.commit()
            city: City = session.get_one(City, city_code)
            return city
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao criar a cidade, verifique se o nome correto foi digitado.", e)

def create_aerodrome(icao: str, aerodrome_name: str, latitude: float, longitude: float, city_code: int, user: User):
    with Session(engine) as session:
        try:
            aerodrome: Aerodrome = Aerodrome(
                ICAO=icao,
                AerodromeName=aerodrome_name,
                Latitude=latitude,
                Longitude=longitude,
                CityCode=city_code,
            )
            session.add(aerodrome)
            session.commit()
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao criar o aeródromo. Provavelmente existe um aeródromo com mesmo ICAO", e)
        
def publish_aerodrome(icao):
    with Session(engine) as session:
        try:
            aerodrome: Aerodrome = session.get_one(Aerodrome, icao)
            aerodrome.IsPublished = True
            session.commit()
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao publicar o aeródromo", e)
        
def unpublish_aerodrome(icao):
    with Session(engine) as session:
        try:
            aerodrome: Aerodrome = session.get_one(Aerodrome, icao)
            aerodrome.IsPublished = False
            session.commit()
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao ocultar o aeróromo", e)

        
def patch_aerodrome(icao: str, aerodrome_name: str, latitude: float, longitude: float, city_code: int):
    with Session(engine) as session:
        try:
            aerodrome: Aerodrome = session.get_one(Aerodrome, icao)
            aerodrome.AerodromeName = aerodrome_name
            aerodrome.Latitude = latitude
            aerodrome.Longitude = longitude
            aerodrome.CityCode = city_code
            session.commit()
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao editar o aeródromo.", e)
  
def del_aerodrome(icao: str):
    with Session(engine) as session:
        try:
            runways = session.query(Runway).filter(Runway.ICAO == icao).all()
            for runway in runways:
                session.delete(runway)

            communications = session.query(Communication).filter(Communication.ICAO == icao).all()
            for communication in communications:
                session.delete(communication)

            ils_systems = session.query(ILS).filter(ILS.ICAO == icao).all()
            for ils in ils_systems:
                session.delete(ils)

            vors = session.query(VOR).filter(VOR.ICAO == icao).all()
            for vor in vors:
                session.delete(vor)

            metars = session.query(METAR).filter(METAR.ICAO == icao).all()
            for metar in metars:
                session.delete(metar)

            tafs = session.query(TAF).filter(TAF.ICAO == icao).all()
            for taf in tafs:
                session.delete(taf)

            aerodrome: Aerodrome = session.get_one(Aerodrome, icao)
            session.delete(aerodrome)
            session.commit()
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao apagar o aeródromo", e)

def create_runway(icao: str, head1: str, head2: str, runway_length: int, runway_width: int, pavement_code: str):
    with Session(engine) as session:
        try:
            runway: Runway = Runway(ICAO=icao, Head1=head1, Head2=head2, RunwayLength=runway_length, RunwayWidth=runway_width, PavementCode=pavement_code)
            session.add(runway)
            session.commit()
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao inserir a pista. Provavelmente uma pista com mesma cabeceira já existe.", e)

def patch_runway(icao: str, head1_old: str, head1: str, head2: str, runway_length: int, runway_width: int, pavement_code: str):
    with Session(engine) as session:
        try:
            runway: Runway = session.get_one(Runway, (icao, head1_old))
            runway.Head1 = head1
            runway.Head2 = head2
            runway.RunwayLength = runway_length
            runway.RunwayWidth = runway_width
            runway.PavementCode = pavement_code
            session.commit()
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao editar a pista.", e)

def del_runway(icao: str, runway_head: str):
    with Session(engine) as session:
        try:
            runway: Runway = session.get_one(Runway, (icao, runway_head))
            session.delete(runway)
            session.commit()
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao apagar a pista.", e)

def create_comm(icao: str, frequency: str, comm_type: str):
    with Session(engine) as session:
        try:
            communication: Communication = Communication(ICAO=icao, Frequency=float(frequency), CommType=comm_type)
            session.add(communication)
            session.commit()
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao inserir frequência. Veja se a frequência não está sendo usada no mesmo aeródromo.", e)

def patch_comm(icao: str, frequency_old, frequency, comm_type):
    with Session(engine) as session:
        try:
            communication: Communication = session.get_one(Communication, (icao, frequency_old))
            if frequency is not None:
                communication.Frequency = float(frequency)
            if comm_type is not None:
                communication.CommType = comm_type
            session.commit()
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao editar frequência. Veja se a frequência não está sendo usada no mesmo aeródromo.", e)
  
def del_comm(icao: str, frequency):
    with Session(engine) as session:
        try:
            communication: Communication = session.get_one(Communication, (icao, frequency))
            session.delete(communication)
            session.commit()
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao apagar frequência.", e)

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
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao adicionar o ILS. Verifique se já não existe um com mesmo IDENT e frequência", e)

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
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao editar o ILS. Verifique se já não existe um com mesmo IDENT e frequência", e)
        
def del_ils(icao: str, frequency):
    with Session(engine) as session:
        try:
            ils: ILS = session.get_one(ILS, (icao, frequency))
            session.delete(ils)
            session.commit()
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao apagar o ILS.", e)
        
def create_vor(icao, ident, frequency):
    with Session(engine) as session:
        vor: VOR =  VOR(ICAO=icao, 
                        Ident=ident, 
                        Frequency=frequency)
        try:
            session.add(vor)
            session.commit()
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao criar o VOR", e)
        
def patch_vor(icao, frequency_old, ident, frequency):
    with Session(engine) as session:
        try:
            vor: VOR = session.get_one(VOR, (icao, frequency_old))
            vor.Ident = ident
            vor.Frequency = frequency
            session.commit()
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao editar o VOR", e)

def del_vor(icao: str, frequency):
    with Session(engine) as session:
        try:
            vor: VOR = session.get_one(VOR, (icao, frequency))
            session.delete(vor)
            session.commit()
            trash_it(icao)
        except Exception as e:
            session.rollback()
            raise ValueError("Erro ao apagar o VOR", e)