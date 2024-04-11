from ORM import *

Session = sessionmaker(bind=engine)
session = Session()

session.add_all([
    CommunicationType(CommType="Torre"),
    CommunicationType(CommType="Solo"),
    CommunicationType(CommType="Tráfego"),
    CommunicationType(CommType="ATIS"),
    CommunicationType(CommType="Operações")])

session.add_all([
    ILSCategory(Category="I"),
    ILSCategory(Category="II"),
    ILSCategory(Category="III"),
    ILSCategory(Category="IIIA"),
    ILSCategory(Category="IIIB"),
    ILSCategory(Category="IIIC"),
])

session.add_all([
    PavementType(Code="ASP", Material="Asfalto"),
    PavementType(Code="CON", Material="Concreto"),    
])

session.commit()

session.add(Aerodrome(ICAO='SBSP', AerodromeName='Congonhas', City='São Paulo', Latitude=-23.626243, Longitude=-46.655417))
session.add_all([
    Communication(ICAO="SBSP", Frequency=118.050, CommType="Torre"),
    Communication(ICAO="SBSP", Frequency=127.150, CommType="Torre"),
    Communication(ICAO="SBSP", Frequency=121.900, CommType="Solo"),
    Communication(ICAO="SBSP", Frequency=120.600, CommType="Tráfego"),
    Communication(ICAO="SBSP", Frequency=127.650, CommType="ATIS")])
session.add_all([
    Runway(ICAO="SBSP", Head1="17R", Head2="35L", RunwayLength=1940, RunwayWidth=45, PavementCode="ASP"),
    Runway(ICAO="SBSP", Head1="17L", Head2="35R", RunwayLength=1495, RunwayWidth=30, PavementCode="ASP"),
])
session.add_all([
    ILS(ICAO="SBSP", Ident="ISP", RunwayHead="17R", Frequency=109.3, Category="I", CRS="169", Minimum=200),
    ILS(ICAO="SBSP", Ident="ISO", RunwayHead="35L", Frequency=109.7, Category="I", CRS="349", Minimum=200),
])
session.add_all([
    VOR(ICAO="SBSP", Ident="CGO", Frequency=116.9),
])

session.add(Aerodrome(ICAO='SBMT', AerodromeName='Campo de Marte', City='São Paulo', Latitude=-23.508810, Longitude=-46.637816))
session.add_all([
    Communication(ICAO="SBMT", Frequency=133.350, CommType="Torre"),
    Communication(ICAO="SBMT", Frequency=121.600, CommType="Solo"),
    Communication(ICAO="SBMT", Frequency=118.700, CommType="Tráfego"),
    Communication(ICAO="SBMT", Frequency=127.725, CommType="ATIS")])
session.add_all([
    Runway(ICAO="SBMT", Head1="12", Head2="30", RunwayLength=1600, RunwayWidth=45, PavementCode="ASP"),
])





session.commit()
session.close()