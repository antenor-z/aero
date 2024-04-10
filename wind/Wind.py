import math
import re

from airportDatabase import get_info

def get_wind(metar):
    ret = None
    try:
        wind_m = re.search(r"(\d{3}|VRB)(\d{2})(G\d{2,3})?KT", metar)
        variable_direction_m = re.search(r"(\d{3})V(\d{3})", metar)
        if wind_m:
            wind_dir = wind_m.group(1)
            wind_speed = wind_m.group(2)
            gust_match = wind_m.group(3)

            ret = [wind_dir, wind_speed, None, None, None]
            if gust_match:
                ret[2] = gust_match.replace("G", "")

            if variable_direction_m:
                ret[3] = variable_direction_m[1]
                ret[4] = variable_direction_m[2]
    except ValueError:
        pass

    return ret

def get_components(icao: str, metar: str):
    metar = "171800Z 28010KT 9999 SCT035 FEW040TCU 33/19 Q1012"
    wind_dir, wind_speed, gust_speed, wind_dir_min, wind_dir_max = get_wind(metar)
    r = {}
    for (rwy_name, rwy_direction) in get_runways(icao):
        r[rwy_name] = get_components_one_runway(rwy_direction, int(wind_dir), int(wind_speed))
        
        if gust_speed is not None:
            r[rwy_name]["gust"] = get_components_one_runway(rwy_direction, int(wind_dir), int(gust_speed))
        else:
            r[rwy_name]["gust"] = None

        if wind_dir_min is not None and wind_dir_max is not None :
            r[rwy_name]["wind_var_min"] = get_components_one_runway(rwy_direction, int(wind_dir_min), int(wind_speed))
            r[rwy_name]["wind_var_max"] = get_components_one_runway(rwy_direction, int(wind_dir_max), int(wind_speed))

            if gust_speed is not None:
                r[rwy_name]["wind_var_min"]["gust"] = get_components_one_runway(rwy_direction, int(wind_dir_min), int(gust_speed))
                r[rwy_name]["wind_var_max"]["gust"] = get_components_one_runway(rwy_direction, int(wind_dir_max), int(gust_speed))
            else:
                r[rwy_name]["wind_var_min"]["gust"] = None
                r[rwy_name]["wind_var_max"]["gust"] = None
        else:
            r[rwy_name]["wind_var_min"] = None
            r[rwy_name]["wind_var_max"] = None


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