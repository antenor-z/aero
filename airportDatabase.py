from airportDataModel import *

_airport_data = [
Airport(
    nome="Pinto Martins",
    icao="SBFZ", 
    comunication=Comunication(
        twr=["121.500", "129.000"], 
        gnd=["121.950"], 
        ops=["122.500"],
        atis=["127.700"]),
    nav=Nav(
        ils=[Ils(rwy="13", ident="IFO", freq="110.3")],
        vor=[Vor(ident="FLZ", freq="114.1")],
    )),
Airport(
    nome="Guarulhos - Governador André Franco Montoro",
    icao="SBGR", 
    comunication=Comunication(
        twr=["118.400", "121.500", "132.750", "135.200"], 
        gnd=["121.700", "126.900"], 
        ops=["122.500"],
        traf=["121.000"],
        atis=["127.750"]),
    nav=Nav(
        ils=[Ils(rwy="28L", ident="IBC", freq="111.1"),
            Ils(rwy="10R", ident="IGH", freq="111.7"),
            Ils(rwy="28R", ident="IGS", freq="111.9"),
            Ils(rwy="10L", ident="IUC", freq="110.7")], 
    )),
Airport(
    nome="Santos Dumont",
    icao="SBRJ", 
    comunication=Comunication(
        twr=["118.700", "121.500"], 
        gnd=["121.700"], 
        traf=["121.050"],
        atis=["132.650"]),
    ),
Airport(
    nome="Aeroporto Senador Petrônio Portella",
    icao="SBTE", 
    comunication=Comunication(
        twr=["118.800"], 
        atis=["127.800"]),
    nav=Nav(
        vor=[Vor(ident="TNA", freq="127.8")],
    )),
]

print(_airport_data)