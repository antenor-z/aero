import re

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

# Test the function
metar = "METAR SBGL 131000Z 280V350 31015G12KT 4000 1800N R10/P2000 +TSRA FEW005 FEW010CB SCT018 BKN025 10/03 Q0995 REDZ WS R10 W12/H75= "
print(get_wind(metar))
