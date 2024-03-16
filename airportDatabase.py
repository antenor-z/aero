from airportDataModel import *

_airport_data = {
"SBSP": Airport(
    nome="Congonhas",
    cidade="São Paulo",
    icao="SBSP", 
    comm=[
        Comm(freq="118.050", type="torre"),
        Comm(freq="127.150", type="torre"),
        Comm(freq="121.900", type="solo"),
        Comm(freq="120.600", type="tráfego"),
        Comm(freq="127.650", type="atis"),
    ],
    ils=[Ils(rwy="17R", ident="ISP", freq="109.3", crs="169", cat="I", minimus="200"),
         Ils(rwy="35L", ident="ISO", freq="109.7", crs="349", cat="I", minimus="200")],
    vor=[Vor(ident="CGO", freq="116.9")],
    rwy=[Rwy(head=("17R", "35L"), length=1940), Rwy(head=("17L", "35R"), length=1495)]
    ),
"SBMT": Airport(
    nome="Campo de Marte",
    cidade="São Paulo",
    icao="SBMT", 
    comm=[
        Comm(freq="133.350", type="torre"),
        Comm(freq="121.600", type="solo"),
        Comm(freq="118.700", type="tráfego"),
        Comm(freq="127.725", type="atis"),
    ],
    rwy=[Rwy(head=("12", "30"), length=1600)],
    ),
"SBGR": Airport(
    nome="Guarulhos",
    cidade="São Paulo",
    icao="SBGR", 
    comm=[
        Comm(freq="118.400", type="torre"),
        Comm(freq="121.500", type="torre"),
        Comm(freq="132.750", type="torre"),
        Comm(freq="135.200", type="torre"),
        Comm(freq="121.700", type="solo"),
        Comm(freq="126.900", type="solo"),
        Comm(freq="122.500", type="operações"),
        Comm(freq="121.000", type="tráfego"),
        Comm(freq="127.750", type="atis"),
    ],
    ils=[Ils(rwy="28L", ident="IBC", freq="111.1", cat="I", crs="275", minimus="200"),
        Ils(rwy="10R", ident="IGH", freq="111.7", cat="III", crs="095", minimus="0"),
        Ils(rwy="28R", ident="IGS", freq="111.9", cat="I", crs="275", minimus="200"),
        Ils(rwy="10L", ident="IUC", freq="110.7", cat="II", crs="095", minimus="100")], 
    rwy=[Rwy(head=("28L", "10R"), length=3000), Rwy(head=("28R", "10L"), length=3700)],
    ),
"SBRJ": Airport(
    nome="Santos Dumont",
    cidade="Rio de Janeiro",
    icao="SBRJ",
    comm=[
        Comm(freq="118.700", type="torre"),
        Comm(freq="121.500", type="torre"),
        Comm(freq="121.700", type="solo"),
        Comm(freq="121.050", type="tráfego"),
        Comm(freq="132.650", type="atis"),
    ],
    rwy=[Rwy(head=("20L", "02R"), length=1323), Rwy(head=("20R", "02L"), length=1260)],
    ),
"SBGL": Airport(
    nome="Antônio Carlos Jobim",
    cidade="Rio de Janeiro",
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
    rwy=[Rwy(head=("10", "28"), length=4000), Rwy(head=("15", "33"), length=3180)],
    ils=[Ils(rwy="15", ident="IJB", freq="110.5", cat="I", crs="149", minimus="217"),
         Ils(rwy="10", ident="ITB", freq="109.3", cat="II", crs="097", minimus="100"), 
         Ils(rwy="28", ident="ILM", freq="111.5", cat="I", crs="278", minimus="500"), 
        ],
    ),
"SBKP": Airport(
    nome="Viracopos",
    cidade="Campinas",
    icao="SBKP", 
    comm=[
        Comm(freq="118.250", type="torre"),
        Comm(freq="121.900", type="solo"),
        Comm(freq="121.100", type="tráfego"),
        Comm(freq="127.825", type="atis"),
    ],
    ils=[Ils(rwy="15", ident="IKP", freq="110.3", cat="I", crs="149", minimus="200")],
    rwy=[Rwy(head=("15", "33"), length=3240)],
    ),
"SBFZ": Airport(
    nome="Pinto Martins",
    cidade="Fortaleza",
    icao="SBFZ", 
    comm=[
        Comm(freq="121.500", type="torre"),
        Comm(freq="129.000", type="torre"),
        Comm(freq="121.950", type="solo"),
        Comm(freq="122.500", type="operações"),
        Comm(freq="127.700", type="atis"),
    ],
    ils=[Ils(rwy="13", ident="IFO", freq="110.3", crs="126", cat="I", minimus="200")],
    vor=[Vor(ident="FLZ", freq="114.1")],
    rwy=[Rwy(head=("13", "31"), length=2755)]
    ),
"SBTE": Airport(
    nome="Senador Petrônio Portella",
    cidade="Teresina",
    icao="SBTE", 
    comm=[
        Comm(freq="118.800", type="torre"),
        Comm(freq="127.800", type="atis"),
    ],
    vor=[Vor(ident="TNA", freq="112.9")],
    rwy=[Rwy(head=("20", "02"), length=2200)],
    ),
"SBCT": Airport(
    nome="Afonso Pena",
    cidade="Curitiba",
    icao="SBCT", 
    comm=[
        Comm(freq="118.150", type="torre"),
        Comm(freq="121.500", type="torre"),
        Comm(freq="121.900", type="solo"),
        Comm(freq="119.300", type="tráfego"),
        Comm(freq="127.800", type="atis"),
    ],
    ils=[Ils(rwy="33", ident="ITA", freq="110.3", cat="I", crs="334", minimus="200"),
         Ils(rwy="15", ident="ICT", freq="109.3", cat="II", crs="154", minimus="110"),],
    vor=[Vor(ident="CTB", freq="116.5")],
    rwy=[Rwy(head=("15", "33"), length=2218), Rwy(head=("11", "29"), length=1798)],
    ),

    "SBCF": Airport(
    nome="Tancredo Neves",
    cidade="Belo Horizonte",
    icao="SBCF", 
    comm=[
        Comm(freq="118.200", type="torre"),
        Comm(freq="121.500", type="torre"),
        Comm(freq="121.900", type="solo"),
        Comm(freq="121.000", type="tráfego"),
        Comm(freq="127.850", type="atis"),
    ],
    ils=[Ils(rwy="34", ident="ITN", freq="110.3", cat="I", crs="342", minimus="200"),
         Ils(rwy="16", ident="ICF", freq="109.7", cat="I", crs="162", minimus="200"),],
    vor=[Vor(ident="CNF", freq="114.4")],
    rwy=[Rwy(head=("16", "34"), length=3600)],
    ),

    "SBSG": Airport(
    nome="São Gonçalo do Amarante",
    cidade="Natal",
    icao="SBSG", 
    comm=[
        Comm(freq="118.200", type="torre"),
        Comm(freq="118.850", type="torre"),
        Comm(freq="121.700", type="solo"),
        Comm(freq="121.000", type="tráfego"),
        Comm(freq="127.600", type="atis"),
    ],
    ils=[Ils(rwy="12", ident="ISG", freq="109.7", cat="I", crs="121", minimus="203")],
    vor=[Vor(ident="SGA", freq="115.9")],
    rwy=[Rwy(head=("12", "30"), length=3000)],
    ),

    "SBBR": Airport(
    nome="Presidente Juscelino Kubitschek",
    cidade="Brasília",
    icao="SBBR", 
    comm=[
        Comm(freq="118.100", type="torre"),
        Comm(freq="118.450", type="torre"),
        Comm(freq="118.750", type="torre"),
        Comm(freq="121.500", type="torre"),
        Comm(freq="121.800", type="solo"),
        Comm(freq="121.950", type="solo"),
        Comm(freq="122.500", type="operações"),
        Comm(freq="135.850", type="operações"),
        Comm(freq="121.000", type="tráfego"),
        Comm(freq="127.800", type="atis"),
    ],
    ils=[
        Ils(rwy="11L", ident="IBR", freq="110.3", cat="I", crs="108", minimus="264"),
        Ils(rwy="29L", ident="IJK", freq="110.9", cat="I", crs="288", minimus="498"),
        Ils(rwy="11R", ident="IDF", freq="109.9", cat="I", crs="108", minimus="250"),],
    vor=[Vor(ident="FSA", freq="112.7"),
         Vor(ident="VJK", freq="117.5")],
    rwy=[Rwy(head=("11L", "29R"), length=3200), Rwy(head=("11R", "29L"), length=3300)],
    ),

    "SBRF": Airport(
    nome="Guararapes - Gilberto Freyre",
    cidade="Recife",
    icao="SBRF", 
    comm=[
        Comm(freq="118.350", type="torre"),
        Comm(freq="121.500", type="torre"),
        Comm(freq="122.800", type="torre"),
        Comm(freq="125.250", type="torre"),
        Comm(freq="121.850", type="solo"),
        Comm(freq="122.500", type="operações"),
        Comm(freq="118.900", type="tráfego"),
        Comm(freq="127.650", type="atis"),
    ],
    ils=[
        Ils(rwy="18", ident="IRF", freq="110.3", cat="I", crs="183", minimus="200"),],
    vor=[Vor(ident="REC", freq="116.9")],
    rwy=[Rwy(head=("18", "36"), length=2751)],
    ),

    "SBSV": Airport(
    nome="Deputado Luís Eduardo Magalhães",
    cidade="Salvador",
    icao="SBSV", 
    comm=[
        Comm(freq="118.300", type="torre"),
        Comm(freq="118.600", type="torre"),
        Comm(freq="118.950", type="torre"),
        Comm(freq="121.100", type="torre"),
        Comm(freq="121.500", type="torre"),
        Comm(freq="121.900", type="solo"),
        Comm(freq="122.500", type="operações"),
        Comm(freq="121.100", type="tráfego"),
        Comm(freq="122.500", type="tráfego"),
        Comm(freq="127.750", type="atis"),
    ],
    ils=[
        Ils(rwy="28", ident="ILD", freq="110.9", cat="I", crs="282", minimus="200"),
        Ils(rwy="10", ident="ISA", freq="111.9", cat="I", crs="102", minimus="200"),],
    vor=[Vor(ident="SVD", freq="116.5")],
    rwy=[Rwy(head=("17", "35"), length=1518), Rwy(head=("10", "28"), length=3003)],
    ),

    "SBPA": Airport(
    nome="Salgado Filho",
    cidade="Porto Alegre",
    icao="SBSV", 
    comm=[
        Comm(freq="118.100", type="torre"),
        Comm(freq="121.100", type="torre"),
        Comm(freq="121.900", type="solo"),
        Comm(freq="122.150", type="trafego"),
        Comm(freq="132.350", type="atis"),
    ],
    ils=[
        Ils(rwy="11", ident="IPA", freq="110.3", cat="I", crs="110", minimus="200")],
    vor=[Vor(ident="FIG", freq="114.7")],
    rwy=[Rwy(head=("11", "29"), length=3200)],
    ),
}

def get_info(icao):
    ret = _airport_data.get(icao)
    if ret is None:
        raise InfoError(f"Informações do ICAO '{icao}' não encontradas.")
    return _airport_data[icao].model_dump()

def get_all_names():
    return [(a.nome, a.icao, a.cidade) for a in _airport_data.values()]

class InfoError(Exception):
    def __init__(self, message):
        super().__init__(message)

if __name__ == "__main__":
    print(_airport_data)
