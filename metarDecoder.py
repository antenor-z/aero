import re
from metar import get_metar

# Fonte: https://ajuda.decea.mil.br/base-de-conhecimento/como-decodificar-o-metar-e-o-speci/

"""
Return:
{
    "icao": "XXXX",
    "day": "01",
    "timeZ": "0300",
    "wind": {
        "direction": "10",
        "speed": "06",
    },
    "visibility": "9999",
    "clouds": {
        "broken": "017",
        "scatered": "027",
        "few": "037",
        "overcast": "047",
    },
    "temperature": 17,
    "dew_point": 15,
    "altimeter": "1024",
}
"""
def decode(icao: str) -> dict:
    metar, is_cache = get_metar(icao)
    #metar = "METAR SBSP 290400Z AUTO 19008KT 160V220 9999 FEW006 SCT008 BKN010 16/14 Q1025="
    #metar = "METAR SBSP 290400Z AUTO VRB08KT 160V220 9999 FEW006 SCT008 BKN010 16/14 Q1025="
    #metar = "METAR SBMN 061300Z 31015G27KT 280V350 5000 1500W -RA BKN010 SCT020 FEW025TCU 25/24 Q1014 RERA WS RWY17 W12/H75="
    print(metar)
    [returned_icao] = re.findall("METAR ([A-Z]{4})", metar)
    assert icao.upper() == returned_icao
    assert metar[0:5] == "METAR"
    assert metar[-1] == "="

    [(day, timeZ)] = re.findall(r" (\d{2})(\d{4})Z ", metar)
    [(temperature, dew_point)] = re.findall(r" (\d{2})/(\d{2}) ", metar)
    [altimeter] = re.findall(r" Q(\d{4})", metar)
    _clouds = re.findall(r" ([A-Z]{3})(\d{3}) ", metar)

    auto = False if len(re.findall("AUTO", metar)) == 0 else True
    correction = False if len(re.findall("COR", metar)) == 0 else True

    if len(re.findall(r" CAVOK ", metar)) == 1:
        visibility = "CAVOK"
        minimum_visibility = None
    else:
        [visibility] = re.findall(r" (\d{4}) ", metar)
        try:
            [(minimum_vis, min_vis_direction)] = re.findall(r" (\d{4})([[N|S|E|W]+) ", metar)
            minimum_visibility = {
            "distance": minimum_vis,
            "direction": min_vis_direction,}
        except ValueError:
            minimum_visibility = None

    try:
        [(wind_direction, wind_speed)] = re.findall(r" (.{3})(\d{2})KT ", metar)
        wind_gusts = 0
    except ValueError:
        [(wind_direction, wind_speed, wind_gusts)] = re.findall(r" (.{3})(\d{2})G(\d{2})KT ", metar)
    
    if wind_direction == "VRB":
        wind_direction = "variable"

    try:
        [big_variation] = re.findall(r" (\d{3})V(\d{3}) ", metar)
    except ValueError:
        big_variation = ()

    clouds_types = {
        "BKN": "broken",
        "SCT": "scatered",
        "FEW": "few",
        "OVC": "overcast",
    }

    clouds = [(clouds_types[type], altitude) for (type, altitude) in _clouds]

    return {
        "is_cache": is_cache,
        "icao": returned_icao,
        "isAutomatic": auto,
        "isCorrection": correction,
        "day": day, 
        "timeZ": timeZ,
        "wind": {
            "direction": wind_direction,
            "speed": wind_speed,
            "gust": wind_gusts,
            "big_variation": big_variation,
        },
        "visibility": visibility,
        "min_visibility": minimum_visibility,
        "clouds": clouds,
        "temperature": temperature,
        "dewPoint": dew_point,
        "altimeter": altimeter,
    }

if __name__ == "__main__":
    print(decode("SBMN"))