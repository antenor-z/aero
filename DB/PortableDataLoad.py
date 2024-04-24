from ORM import *

Session = sessionmaker(bind=engine)
session = Session()

session.add_all([
    CommunicationType(CommType="Torre"),
    CommunicationType(CommType="Solo"),
    CommunicationType(CommType="Tráfego"),
    CommunicationType(CommType="ATIS"),
    CommunicationType(CommType="Operações"),
    CommunicationType(CommType="Rampa")])

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

session.add_all([
    City(CityName="São Paulo"),
    City(CityName="Rio de Janeiro"),
    City(CityName="Campinas"),
    City(CityName="Fortaleza"),
    City(CityName="Teresina"),
    City(CityName="Curitiba"),
    City(CityName="Belo Horizonte"),
    City(CityName="Natal"),
    City(CityName="Brasília"),
    City(CityName="Recife"),
    City(CityName="Salvador"),
    City(CityName="Porto Alegre"),
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
    Runway(ICAO="SBSP", Head1="17L", Head2="35R", RunwayLength=1495, RunwayWidth=45, PavementCode="ASP"),
    Runway(ICAO="SBSP", Head1="17R", Head2="35L", RunwayLength=1883, RunwayWidth=45, PavementCode="ASP"),
])
session.add_all([
    ILS(ICAO="SBSP", Ident="ISP", RunwayHead="17R", Frequency=109.3, Category="I", CRS=169, Minimum=200),
    ILS(ICAO="SBSP", Ident="ISO", RunwayHead="35L", Frequency=109.7, Category="I", CRS=349, Minimum=200),
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


session.add(Aerodrome(ICAO='SBGR', AerodromeName='Guarulhos', City='São Paulo', Latitude=-23.430181, Longitude=-46.466770))
session.add_all([
    Communication(ICAO="SBGR", Frequency=118.400, CommType="Torre"),
    Communication(ICAO="SBGR", Frequency=121.500, CommType="Torre"),
    Communication(ICAO="SBGR", Frequency=132.750, CommType="Torre"),
    Communication(ICAO="SBGR", Frequency=135.200, CommType="Torre"),
    Communication(ICAO="SBGR", Frequency=121.700, CommType="Solo"),
    Communication(ICAO="SBGR", Frequency=126.900, CommType="Solo"),
    Communication(ICAO="SBGR", Frequency=122.500, CommType="Operações"),
    Communication(ICAO="SBGR", Frequency=121.000, CommType="Tráfego"),
    Communication(ICAO="SBGR", Frequency=127.750, CommType="ATIS")])
session.add_all([
    Runway(ICAO="SBGR", Head1="10R", Head2="28L", RunwayLength=3000, RunwayWidth=45, PavementCode="ASP"),
    Runway(ICAO="SBGR", Head1="10L", Head2="28R", RunwayLength=3700, RunwayWidth=30, PavementCode="ASP"),
])
session.add_all([
    ILS(ICAO="SBGR", Ident="IBC", RunwayHead="28L", Frequency=111.1, Category="I", CRS=275, Minimum=200),
    ILS(ICAO="SBGR", Ident="IGH", RunwayHead="10R", Frequency=111.7, Category="IIIC", CRS=95, Minimum=0),
    ILS(ICAO="SBGR", Ident="IGS", RunwayHead="28R", Frequency=111.9, Category="I", CRS=275, Minimum=200),
    ILS(ICAO="SBGR", Ident="IUC", RunwayHead="10L", Frequency=110.7, Category="II", CRS=95, Minimum=100),
])


session.add(Aerodrome(ICAO='SBRJ', AerodromeName='Santos Dumont', City='Rio de Janeiro', Latitude=-22.910500, Longitude=-43.163236))
session.add_all([
    Communication(ICAO="SBRJ", Frequency=118.700, CommType="Torre"),
    Communication(ICAO="SBRJ", Frequency=121.500, CommType="Torre"),
    Communication(ICAO="SBRJ", Frequency=121.700, CommType="Solo"),
    Communication(ICAO="SBRJ", Frequency=121.050, CommType="Tráfego"),
    Communication(ICAO="SBRJ", Frequency=132.650, CommType="ATIS")])
session.add_all([
    Runway(ICAO="SBRJ", Head1="02L", Head2="20R", RunwayLength=1260, RunwayWidth=30, PavementCode="ASP"),
    Runway(ICAO="SBRJ", Head1="02R", Head2="20L", RunwayLength=1323, RunwayWidth=42, PavementCode="ASP"),
])

session.add(Aerodrome(ICAO='SBGL', AerodromeName='Antônio Carlos Jobim', City='Rio de Janeiro', Latitude=-22.806812, Longitude=-43.236409))
session.add_all([
    Communication(ICAO="SBGL", Frequency=118.000, CommType="Torre"),
    Communication(ICAO="SBGL", Frequency=118.200, CommType="Torre"),
    Communication(ICAO="SBGL", Frequency=121.500, CommType="Torre"),
    Communication(ICAO="SBGL", Frequency=121.650, CommType="Solo"),
    Communication(ICAO="SBGL", Frequency=128.350, CommType="Solo"),
    Communication(ICAO="SBGL", Frequency=121.000, CommType="Tráfego"),
    Communication(ICAO="SBGL", Frequency=135.100, CommType="Tráfego"),
    Communication(ICAO="SBGL", Frequency=127.600, CommType="ATIS"),
    Communication(ICAO="SBGL", Frequency=121.950, CommType="Rampa"),
    Communication(ICAO="SBGL", Frequency=130.675, CommType="Rampa"),
    Communication(ICAO="SBGL", Frequency=131.050, CommType="Rampa"),
    ])
session.add_all([
    Runway(ICAO="SBGL", Head1="10", Head2="28", RunwayLength=4000, RunwayWidth=45, PavementCode="ASP"),
    Runway(ICAO="SBGL", Head1="15", Head2="33", RunwayLength=3180, RunwayWidth=47, PavementCode="ASP"),
])
session.add_all([
    VOR(ICAO='SBGL', Ident='PCX', Frequency=114.6),
    VOR(ICAO='SBGL', Ident='CXI', Frequency=112.3),
])
session.add_all([
    ILS(ICAO="SBGL", Ident="IJB", RunwayHead="15", Frequency=110.5, Category="I", CRS=149, Minimum=217),
    ILS(ICAO="SBGL", Ident="ITB", RunwayHead="10", Frequency=109.3, Category="II", CRS=97, Minimum=100),
    ILS(ICAO="SBGL", Ident="ILM", RunwayHead="28", Frequency=111.5, Category="I", CRS=278, Minimum=500),
])

session.add(Aerodrome(ICAO='SBKP', AerodromeName='Viracopos', City='Campinas', Latitude=-23.006848, Longitude=-47.136147))
session.add_all([
    Communication(ICAO="SBKP", Frequency=118.250, CommType="Torre"),
    Communication(ICAO="SBKP", Frequency=121.900, CommType="Solo"),
    Communication(ICAO="SBKP", Frequency=121.100, CommType="Tráfego"),
    Communication(ICAO="SBKP", Frequency=127.825, CommType="Atis"),
    ])
session.add_all([
    Runway(ICAO="SBKP", Head1="15", Head2="33", RunwayLength=3240, RunwayWidth=45, PavementCode="ASP"),
])
session.add_all([
    ILS(ICAO="SBKP", Ident="IKP", RunwayHead="15", Frequency=110.3, Category="I", CRS=149, Minimum=200),
])

session.add_all([
    Aerodrome(ICAO='SBFZ', AerodromeName='Pinto Martins', City='Fortaleza', Latitude=-3.7764, Longitude=-38.532041),
    Communication(ICAO='SBFZ', Frequency=121.5, CommType='Torre'),
    Communication(ICAO='SBFZ', Frequency=129.0, CommType='Torre'),
    Communication(ICAO='SBFZ', Frequency=121.95, CommType='Solo'),
    Communication(ICAO='SBFZ', Frequency=122.5, CommType='Operações'),
    Communication(ICAO='SBFZ', Frequency=127.7, CommType='ATIS'),
    ILS(ICAO='SBFZ', Ident='IFO', RunwayHead='13', Frequency=110.3, CRS='126', Category='I', Minimum=200),
    VOR(ICAO='SBFZ', Ident='FLZ', Frequency=114.1),
    Runway(ICAO='SBFZ', Head1='13', Head2='31', RunwayLength=2755, RunwayWidth=45, PavementCode="ASP"),
])

session.add_all([
    Aerodrome(ICAO='SBTE', AerodromeName='Senador Petrônio Portella', City='Teresina', Latitude=-5.059275, Longitude=-42.823784),
    Communication(ICAO='SBTE', Frequency=118.8, CommType='Torre'),
    Communication(ICAO='SBTE', Frequency=127.8, CommType='ATIS'),
    VOR(ICAO='SBTE', Ident='TNA', Frequency=112.9),
    Runway(ICAO='SBTE', Head1='20', Head2='02', RunwayLength=2200, RunwayWidth=45, PavementCode="ASP"),
])

session.add_all([
    Aerodrome(ICAO='SBCT', AerodromeName='Afonso Pena', City='Curitiba', Latitude=-25.527896, Longitude=-49.175797),
    Communication(ICAO='SBCT', Frequency=118.150, CommType='Torre'),
    Communication(ICAO='SBCT', Frequency=121.500, CommType='Torre'),
    Communication(ICAO='SBCT', Frequency=121.900, CommType='Solo'),
    Communication(ICAO='SBCT', Frequency=119.300, CommType='Tráfego'),
    Communication(ICAO='SBCT', Frequency=127.800, CommType='ATIS'),
    ILS(ICAO='SBCT', Ident='ITA', RunwayHead='33', Frequency=110.3, CRS='334', Category='I', Minimum=200),
    ILS(ICAO='SBCT', Ident='ICT', RunwayHead='15', Frequency=109.3, CRS='154', Category='II', Minimum=110),
    VOR(ICAO='SBCT', Ident='CTB', Frequency=116.5),
    Runway(ICAO='SBCT', Head1='15', Head2='33', RunwayLength=2218, RunwayWidth=45, PavementCode="ASP"),
    Runway(ICAO='SBCT', Head1='11', Head2='29', RunwayLength=1798, RunwayWidth=45, PavementCode="ASP"),
])

session.add_all([
    Aerodrome(ICAO='SBCF', AerodromeName='Tancredo Neves', City='Belo Horizonte', Latitude=-19.633220, Longitude=-43.969015),
    Communication(ICAO='SBCF', Frequency=118.200, CommType='Torre'),
    Communication(ICAO='SBCF', Frequency=121.500, CommType='Torre'),
    Communication(ICAO='SBCF', Frequency=121.900, CommType='Solo'),
    Communication(ICAO='SBCF', Frequency=121.000, CommType='Tráfego'),
    Communication(ICAO='SBCF', Frequency=127.850, CommType='ATIS'),
    ILS(ICAO='SBCF', Ident='ITN', RunwayHead='34', Frequency=110.3, CRS='342', Category='I', Minimum=200),
    ILS(ICAO='SBCF', Ident='ICF', RunwayHead='16', Frequency=109.7, CRS='162', Category='I', Minimum=200),
    VOR(ICAO='SBCF', Ident='CNF', Frequency=114.4),
    Runway(ICAO='SBCF', Head1='16', Head2='34', RunwayLength=3600, RunwayWidth=45, PavementCode="ASP"),
])

session.add_all([
    Aerodrome(ICAO='SBSG', AerodromeName='São Gonçalo do Amarante', City='Natal', Latitude=-5.768855, Longitude=-35.366448),
    Communication(ICAO='SBSG', Frequency=118.200, CommType='Torre'),
    Communication(ICAO='SBSG', Frequency=118.850, CommType='Torre'),
    Communication(ICAO='SBSG', Frequency=121.700, CommType='Solo'),
    Communication(ICAO='SBSG', Frequency=121.000, CommType='Tráfego'),
    Communication(ICAO='SBSG', Frequency=127.600, CommType='ATIS'),
    ILS(ICAO='SBSG', Ident='ISG', RunwayHead='12', Frequency=109.7, CRS='121', Category='I', Minimum=203),
    VOR(ICAO='SBSG', Ident='SGA', Frequency=115.9),
    Runway(ICAO='SBSG', Head1='12', Head2='30', RunwayLength=3000, RunwayWidth=60, PavementCode="ASP"),
])

session.add_all([
    Aerodrome(ICAO='SBBR', AerodromeName='Presidente Juscelino Kubitschek', City='Brasília', Latitude=-15.870264, Longitude=-47.918460),
    Communication(ICAO='SBBR', Frequency=118.100, CommType='Torre'),
    Communication(ICAO='SBBR', Frequency=118.450, CommType='Torre'),
    Communication(ICAO='SBBR', Frequency=118.750, CommType='Torre'),
    Communication(ICAO='SBBR', Frequency=121.500, CommType='Torre'),
    Communication(ICAO='SBBR', Frequency=121.800, CommType='Solo'),
    Communication(ICAO='SBBR', Frequency=121.950, CommType='Solo'),
    Communication(ICAO='SBBR', Frequency=122.500, CommType='Operações'),
    Communication(ICAO='SBBR', Frequency=135.850, CommType='Operações'),
    Communication(ICAO='SBBR', Frequency=121.000, CommType='Tráfego'),
    Communication(ICAO='SBBR', Frequency=127.800, CommType='ATIS'),
    ILS(ICAO='SBBR', Ident='IBR', RunwayHead='11L', Frequency=110.3, CRS='108', Category='I', Minimum=264),
    ILS(ICAO='SBBR', Ident='IJK', RunwayHead='29L', Frequency=110.9, CRS='288', Category='I', Minimum=498),
    ILS(ICAO='SBBR', Ident='IDF', RunwayHead='11R', Frequency=109.9, CRS='108', Category='I', Minimum=250),
    VOR(ICAO='SBBR', Ident='FSA', Frequency=112.7),
    VOR(ICAO='SBBR', Ident='VJK', Frequency=117.5),
    Runway(ICAO='SBBR', Head1='11L', Head2='29R', RunwayLength=3200, RunwayWidth=45, PavementCode="ASP"),
    Runway(ICAO='SBBR', Head1='11R', Head2='29L', RunwayLength=3300, RunwayWidth=45, PavementCode="ASP"),
])

session.add_all([
    Aerodrome(ICAO='SBRF', AerodromeName='Guararapes - Gilberto Freyre', City='Recife', Latitude=-8.123593, Longitude=-34.924340),
    Communication(ICAO='SBRF', Frequency=118.350, CommType='Torre'),
    Communication(ICAO='SBRF', Frequency=121.500, CommType='Torre'),
    Communication(ICAO='SBRF', Frequency=122.800, CommType='Torre'),
    Communication(ICAO='SBRF', Frequency=125.250, CommType='Torre'),
    Communication(ICAO='SBRF', Frequency=121.850, CommType='Solo'),
    Communication(ICAO='SBRF', Frequency=122.500, CommType='Operações'),
    Communication(ICAO='SBRF', Frequency=118.900, CommType='Tráfego'),
    Communication(ICAO='SBRF', Frequency=127.650, CommType='ATIS'),
    ILS(ICAO='SBRF', Ident='IRF', RunwayHead='18', Frequency=110.3, CRS='183', Category='I', Minimum=200),
    VOR(ICAO='SBRF', Ident='REC', Frequency=116.9),
    Runway(ICAO='SBRF', Head1='18', Head2='36', RunwayLength=2751, RunwayWidth=45, PavementCode="ASP"),
])

session.add_all([
    Aerodrome(ICAO='SBSV', AerodromeName='Deputado Luís Eduardo Magalhães', City='Salvador', Latitude=-12.910444, Longitude=-38.332605),
    Communication(ICAO='SBSV', Frequency=118.300, CommType='Torre'),
    Communication(ICAO='SBSV', Frequency=118.600, CommType='Torre'),
    Communication(ICAO='SBSV', Frequency=118.950, CommType='Torre'),
    Communication(ICAO='SBSV', Frequency=121.500, CommType='Torre'),
    Communication(ICAO='SBSV', Frequency=121.900, CommType='Solo'),
    Communication(ICAO='SBSV', Frequency=121.100, CommType='Tráfego'),
    Communication(ICAO='SBSV', Frequency=122.500, CommType='Tráfego'),
    Communication(ICAO='SBSV', Frequency=127.750, CommType='ATIS'),
    ILS(ICAO='SBSV', Ident='ILD', RunwayHead='28', Frequency=110.9, CRS='282', Category='I', Minimum=200),
    ILS(ICAO='SBSV', Ident='ISA', RunwayHead='10', Frequency=111.9, CRS='102', Category='I', Minimum=200),
    VOR(ICAO='SBSV', Ident='SVD', Frequency=116.5),
    Runway(ICAO='SBSV', Head1='17', Head2='35', RunwayLength=1518, RunwayWidth=45, PavementCode="ASP"),
    Runway(ICAO='SBSV', Head1='10', Head2='28', RunwayLength=3003, RunwayWidth=45, PavementCode="ASP"),
])

session.add_all([
    Aerodrome(ICAO='SBPA', AerodromeName='Salgado Filho', City='Porto Alegre', Latitude=29.993515, Longitude=-51.172375),
    Communication(ICAO='SBPA', Frequency=118.100, CommType='Torre'),
    Communication(ICAO='SBPA', Frequency=121.100, CommType='Torre'),
    Communication(ICAO='SBPA', Frequency=121.900, CommType='Solo'),
    Communication(ICAO='SBPA', Frequency=122.150, CommType='Tráfego'),
    Communication(ICAO='SBPA', Frequency=132.350, CommType='ATIS'),
    ILS(ICAO='SBPA', Ident='IPA', RunwayHead='11', Frequency=110.3, CRS='110', Category='I', Minimum=200),
    VOR(ICAO='SBPA', Ident='FIG', Frequency=114.7),
    Runway(ICAO='SBPA', Head1='11', Head2='29', RunwayLength=3200, RunwayWidth=45, PavementCode="ASP"),
])


session.commit()
session.close()