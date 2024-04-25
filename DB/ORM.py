from os import environ
from sqlalchemy import PrimaryKeyConstraint, create_engine,\
    Column, Integer, String, ForeignKey, UniqueConstraint, DECIMAL
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session


Base = declarative_base()

class City(Base):
    __tablename__ = 'City'

    CityName = Column(String(50), primary_key=True)

class Aerodrome(Base):
    __tablename__ = 'Aerodrome'

    ICAO = Column(String(4), primary_key=True)
    AerodromeName = Column(String(50), nullable=False)
    City = Column(String(30), ForeignKey('City.CityName'), nullable=False)
    Latitude = Column(DECIMAL(9, 6), nullable=False)
    Longitude = Column(DECIMAL(9, 6), nullable=False)
    METAR = Column(String(100), nullable=True)
    __table_args__ = (
        UniqueConstraint('AerodromeName'),
    )

    runways = relationship("Runway", backref="aerodrome")
    ils = relationship("ILS", backref="aerodrome")
    vor = relationship("VOR", backref="aerodrome")
    communication = relationship("Communication", backref="aerodrome")

class PavementType(Base):
    __tablename__ = 'PavementType'

    Code = Column(String(3), primary_key=True)
    Material = Column(String(20), nullable=False)

class Runway(Base):
    __tablename__ = 'Runway'

    ICAO = Column(String(4), ForeignKey('Aerodrome.ICAO'), nullable=False)
    Head1 = Column(String(3), nullable=False)
    Head2 = Column(String(3), nullable=False)
    RunwayLength = Column(Integer, nullable=False)
    RunwayWidth = Column(Integer)
    PavementCode = Column(String(3), ForeignKey('PavementType.Code'))

    __table_args__ = (
        PrimaryKeyConstraint('ICAO', 'Head1'),
        UniqueConstraint('ICAO', 'Head1', 'Head2'),
    )

    pavement_type = relationship("PavementType")


class CommunicationType(Base):
    __tablename__ = 'CommunicationType'

    CommType = Column(String(20), primary_key=True)

class Communication(Base):
    __tablename__ = 'Communication'

    ICAO = Column(String(4), ForeignKey('Aerodrome.ICAO'), nullable=False)
    Frequency = Column(Integer, nullable=False)
    CommType = Column(String(20), ForeignKey('CommunicationType.CommType'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('ICAO', 'Frequency'),
    )

class ILSCategory(Base):
    __tablename__ = 'ILSCategory'

    Category = Column(String(10), primary_key=True)

class ILS(Base):
    __tablename__ = 'ILS'

    ICAO = Column(String(4), ForeignKey('Aerodrome.ICAO'), nullable=False)
    Ident = Column(String(3), nullable=False)
    RunwayHead = Column(String(3), nullable=False)
    Frequency = Column(Integer, nullable=False)
    Category = Column(String(10), ForeignKey('ILSCategory.Category'), nullable=False)
    CRS = Column(Integer, nullable=False)
    Minimum = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint('ICAO', 'Frequency'),
    )

class VOR(Base):
    __tablename__ = 'VOR'

    ICAO = Column(String(4), ForeignKey('Aerodrome.ICAO'), nullable=False)
    Ident = Column(String(3), nullable=False)
    Frequency = Column(Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('ICAO', 'Frequency'),
    )

# CREATE USER 'aero-user'@'localhost' IDENTIFIED BY '123';
# GRANT ALL PRIVILEGES ON aero.* TO 'aero-user'@'localhost';
# FLUSH PRIVILEGES;

DB_PASSWORD = None
with open(environ["MYSQL_PASSWORD_FILE"]) as fp:
    DB_PASSWORD = fp.read()

DB_USER = environ.get("MYSQL_USER")
DB_DATABASE = environ.get("MYSQL_DATABASE")

assert DB_PASSWORD is not None, "No db password supplied"
assert DB_USER is not None, "No MYSQL user supplied"
assert DB_DATABASE is not None, "No MYSQL database supplied"


db_url = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@aero-db:3306/{DB_DATABASE}'

engine = create_engine(db_url)
Base.metadata.create_all(engine)

