import math
import re

from airportDatabase import get_info

def get_wind(metar):
    try:
        [(wind_dir, wind_speed)] = re.findall("(\d{3})(\d{2})KT", metar)
    except ValueError:
        wind_dir, wind_speed = 0, 0

    return wind_dir, wind_speed

def get_components(icao: str, metar: str):
    #metar = "171800Z 28010KT 260V320 9999 SCT035 FEW040TCU 33/19 Q1012"
    wind_dir, wind_speed = get_wind(metar)
    r = {}
    for (rwy_name, rwy_direction) in get_runways(icao):
        print(rwy_direction)
        r[rwy_name] = get_components_one_runway(rwy_direction, int(wind_dir), int(wind_speed))
    print(r)
    return r

def get_components_one_runway(runway_head: int, wind_dir:int, wind_speed: int):
    """
    For a runway heading (0 to 360 degrees) and the direction where the
    wind is comming from, compute the component paralel to the direction
    of the runway (head wind or tail wind) and the perpendicular component.

    For the paralel component:
        if > 0: Head wind, the wind is comming towards the plane
        if < 0: Tail wind, the wind is comming from behind the plane.
    For the perpendicular component (cross wind):
        if > 0: Cross wind comming from the right
        if < 0: Cross wind comming from the left
    """
    assert 0 < runway_head <= 360
    assert 0 <= wind_dir < 360
    assert 0 <= wind_speed

    angle = math.radians((wind_dir - runway_head) % 360)
    angle_deg = abs(math.degrees(angle))

    head = wind_speed * math.cos(angle)
    cross = wind_speed * math.sin(angle)

    return {
        "cross": round(cross, 2),
        "head": round(head, 2),
        "angle": round(angle_deg, 2),
    }

def get_runways(icao: str):
    """
    Returns the runway 'name' (including R, L or C) and the runway heading in degrees.
    For example if the airport has runways 17L, 17R, 35L and 35R, the following will
    be returned:
    [('17R', 170), ('35L', 350), ('17L', 170), ('35R', 350)]
    """
    r = []
    for runway in get_info(icao)["rwy"]:
        rwy_without_letter = runway["head"][0].replace("L", "").replace("C", "").replace("R", "")
        r.append((runway["head"][0], int(rwy_without_letter) * 10))
        rwy_without_letter = runway["head"][1].replace("L", "").replace("C", "").replace("R", "")
        r.append((runway["head"][1], int(rwy_without_letter) * 10))
    return r