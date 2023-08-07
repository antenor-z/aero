from airportDataModel import *

_airport_data = {
"SBFZ": Airport(
    nome="Pinto Martins",
    icao="SBFZ", 
    comm=[
        Comm(freq="121.500", type="torre"),
        Comm(freq="129.000", type="torre"),
        Comm(freq="121.950", type="solo"),
        Comm(freq="122.500", type="operações"),
        Comm(freq="127.700", type="atis"),
        Comm(freq="129.000", type="torre"),
    ],
    ils=[Ils(rwy="13", ident="IFO", freq="110.3")],
    vor=[Vor(ident="FLZ", freq="114.1")],
    rwy=[Rwy(head=("13", "31"), length=2755)]
    ),
# "SBGR": Airport(
#     nome="Guarulhos - Governador André Franco Montoro",
#     icao="SBGR", 
#     comm=Comunication(
#         twr=["118.400", "121.500", "132.750", "135.200"], 
#         gnd=["121.700", "126.900"], 
#         ops=["122.500"],
#         traf=["121.000"],
#         atis=["127.750"]),
#     ils=[Ils(rwy="28L", ident="IBC", freq="111.1"),
#         Ils(rwy="10R", ident="IGH", freq="111.7"),
#         Ils(rwy="28R", ident="IGS", freq="111.9"),
#         Ils(rwy="10L", ident="IUC", freq="110.7")], 
#     rwy=[Rwy(head=("28L", "10R"), length=3000), Rwy(head=("28R", "10L"), length=3700)],
#     ),
# "SBRJ": Airport(
#     nome="Santos Dumont",
#     icao="SBRJ", 
#     comunication=Comunication(
#         twr=["118.700", "121.500"], 
#         gnd=["121.700"], 
#         traf=["121.050"],
#         atis=["132.650"]),
#     rwy=[Rwy(head=("20L", "02R"), length=1323), Rwy(head=("20R", "02L"), length=1260)],
#     ),
"SBGL": Airport(
    nome="Antônio Carlos Jobim",
    icao="SBGL", 
    comm=[
        Comm(freq="118.000", type="torre"),
        Comm(freq="118.200", type="torre"),
        Comm(freq="121.500", type="torre"),
        Comm(freq="121.000", type="torre"),
        Comm(freq="121.650", type="torre"),
        Comm(freq="121.650", type="solo"),
        Comm(freq="128.350", type="solo"),
        Comm(freq="121.000", type="tráfego"),
        Comm(freq="135.100", type="tráfego"),
        Comm(freq="127.600", type="atis"),
        Comm(freq="121.950", type="rampa"),
        Comm(freq="130.675", type="rampa"),
        Comm(freq="131.050", type="rampa"),],
    rwy=[Rwy(head=("20L", "02R"), length=1323), Rwy(head=("20R", "02L"), length=1260)],
    ils=[Ils(rwy="15", ident="IJB", freq="110.5"),
         Ils(rwy="10", ident="ITB", freq="109.3", cat="II"), 
         Ils(rwy="28", ident="ILM", freq="111.5"), 
        ],
    ),
"SBKP": Airport(
    nome="Viracopos",
    icao="SBKP", 
    comm=[
        Comm(freq="118.250", type="torre"),
        Comm(freq="121.900", type="solo"),
        Comm(freq="121.100", type="tráfego"),
        Comm(freq="127.800", type="atis"),
    ],
    ils=[Ils(rwy="15", ident="IKP", freq="110.3",)],
    rwy=[Rwy(head=("15", "33"), length=3240)],
    ),
"SBTE": Airport(
    nome="Senador Petrônio Portella",
    icao="SBTE", 
    comm=[
        Comm(freq="118.800", type="torre"),
        Comm(freq="127.800", type="atis"),
    ],
    vor=[Vor(ident="TNA", freq="127.8")],
    rwy=[Rwy(head=("20", "02"), length=2200)],
    ),
"SBCT": Airport(
    nome="Afonso Pena",
    icao="SBCT", 
    comm=[
        Comm(freq="118.150", type="torre"),
        Comm(freq="121.500", type="torre"),
        Comm(freq="121.900", type="solo"),
        Comm(freq="119.300", type="tráfego"),
        Comm(freq="127.800", type="atis"),
    ],
    ils=[Ils(rwy="33", ident="ITA", freq="110.3"),
         Ils(rwy="15", ident="CTB", freq="109.3"),],
    vor=[Vor(ident="CTB", freq="116.5")],
    rwy=[Rwy(head=("15", "33"), length=2218), Rwy(head=("11", "29"), length=1798)],
    ),
}

def get_info(icao):
    return _airport_data[icao].model_dump()

def get_all_names():
    return [(a.nome, a.icao) for a in _airport_data.values()]

if __name__ == "__main__":
    print(_airport_data)
