from sqlalchemy import PrimaryKeyConstraint, create_engine,\
    Column, Integer, String, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from dotenv import dotenv_values

CONFIG: dict = dotenv_values()

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
    Frequency = Column(DECIMAL(6, 3), nullable=False)
    CommType = Column(String(20), ForeignKey('CommunicationType.CommType'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('ICAO', 'Frequency'),
        UniqueConstraint('ICAO', 'Frequency'),
    )

class ILSCategory(Base):
    __tablename__ = 'ILSCategory'

    Category = Column(String(10), primary_key=True)

class ILS(Base):
    __tablename__ = 'ILS'

    ICAO = Column(String(4), ForeignKey('Aerodrome.ICAO'), nullable=False)
    Ident = Column(String(3), nullable=False)
    RunwayHead = Column(String(3), nullable=False)
    Frequency = Column(DECIMAL(6, 3), nullable=False)
    Category = Column(String(10), ForeignKey('ILSCategory.Category'), nullable=False)
    CRS = Column(Integer, nullable=False)
    Minimum = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint('ICAO', 'Ident'),
        UniqueConstraint('ICAO', 'Frequency'),
    )

class VOR(Base):
    __tablename__ = 'VOR'

    ICAO = Column(String(4), ForeignKey('Aerodrome.ICAO'), nullable=False)
    Ident = Column(String(3), nullable=False)
    Frequency = Column(DECIMAL(6, 3), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('ICAO', 'Ident'),
        UniqueConstraint('ICAO', 'Frequency'),
    )

# CREATE USER 'aero-user'@'localhost' IDENTIFIED BY '123';
# GRANT ALL PRIVILEGES ON aero.* TO 'aero-user'@'localhost';
# FLUSH PRIVILEGES;

db_url = f'mysql+pymysql://aero-user:{CONFIG["DB_PASSWORD"]}@localhost:3306/aero'

engine = create_engine(db_url)
Base.metadata.create_all(engine)

