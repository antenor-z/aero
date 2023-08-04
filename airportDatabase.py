from airportDataModel import *

_airport_data = {
"SBFZ": Airport(
    nome="Pinto Martins",
    icao="SBFZ", 
    comunication=Comunication(
        twr=["121.500", "129.000"], 
        gnd=["121.950"], 
        ops=["122.500"],
        atis=["127.700"]),
    ils=[Ils(rwy="13", ident="IFO", freq="110.3")],
    vor=[Vor(ident="FLZ", freq="114.1")],
    ),
"SBGR": Airport(
    nome="Guarulhos - Governador André Franco Montoro",
    icao="SBGR", 
    comunication=Comunication(
        twr=["118.400", "121.500", "132.750", "135.200"], 
        gnd=["121.700", "126.900"], 
        ops=["122.500"],
        traf=["121.000"],
        atis=["127.750"]),
    ils=[Ils(rwy="28L", ident="IBC", freq="111.1"),
        Ils(rwy="10R", ident="IGH", freq="111.7"),
        Ils(rwy="28R", ident="IGS", freq="111.9"),
        Ils(rwy="10L", ident="IUC", freq="110.7")], 
    ),
"SBRJ": Airport(
    nome="Santos Dumont",
    icao="SBRJ", 
    comunication=Comunication(
        twr=["118.700", "121.500"], 
        gnd=["121.700"], 
        traf=["121.050"],
        atis=["132.650"]),
    ),
"SBTE": Airport(
    nome="Viracopos",
    icao="SBKP", 
    comunication=Comunication(
        twr=["118.250"],
        gnd=["121.900"],
        traf=["121.100"],
        atis=["127.800"]),
    ils=[Ils(rwy="15", ident="IKP", freq="110.3",)]
    ),
"SBTE": Airport(
    nome="Senador Petrônio Portella",
    icao="SBTE", 
    comunication=Comunication(
        twr=["118.800"], 
        atis=["127.800"]),
    vor=[Vor(ident="TNA", freq="127.8")],
    ),
"SBCT": Airport(
    nome="Afonso Pena",
    icao="SBCT", 
    comunication=Comunication(
        twr=["118.150", "121.500"],
        gnd=["121.900"],
        traf=["119.300"],
        atis=["127.800"]),
    ils=[Ils(rwy="33", ident="ITA", freq="110.3"),
         Ils(rwy="15", ident="CTB", freq="109.3"),],
    vor=[Vor(ident="CTB", freq="116.5")],
    ),
}

def get_info(icao):
    return _airport_data[icao].model_dump()

if __name__ == "__main__":
    print(_airport_data)