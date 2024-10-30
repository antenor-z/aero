import re

def parse_metar(metar_str: str) -> dict:
    wind_regex = re.compile(r'(\d{3})(\d{2})KT')
    temp_regex = re.compile(r'M?(\d{2})/(M?\d{2})')
    qnh_regex = re.compile(r'Q(\d{4})')
    vis_regex = re.compile(r'(\d{4}) ')
    cloud_regex = re.compile(r'(FEW|SCT|BKN|OVC)(\d{3})')

    wind_match = wind_regex.search(metar_str)
    temp_match = temp_regex.search(metar_str)
    qnh_match = qnh_regex.search(metar_str)
    vis_match = vis_regex.search(metar_str)
    cloud_matches = cloud_regex.findall(metar_str)

    wind_direction = int(wind_match.group(1)) if wind_match else None
    wind_speed = int(wind_match.group(2)) if wind_match else None
    visibility = int(vis_match.group(1)) if vis_match else None

    if "CAVOK" in metar_str:
        visibility = 9999

    if temp_match:
        temp_str = temp_match.group(1)
        temperature = -int(temp_str[1:]) if temp_str.startswith('M') else int(temp_str)
        dew_str = temp_match.group(2)
        dew_point = -int(dew_str[1:]) if dew_str.startswith('M') else int(dew_str)
    else:
        temperature = None
        dew_point = None

    qnh = int(qnh_match.group(1)) if qnh_match else None

    clouds_few = []
    clouds_scattered = []
    clouds_broken = []
    clouds_overcast = []

    for match in cloud_matches:
        coverage = match[0] 
        altitude = int(match[1]) * 100

        if coverage == 'FEW':
            clouds_few.append(altitude)
        elif coverage == 'SCT':
            clouds_scattered.append(altitude)
        elif coverage == 'BKN':
            clouds_broken.append(altitude)
        elif coverage == 'OVC':
            clouds_overcast.append(altitude)

    return {
        "wind_direction": wind_direction,
        "wind_speed": wind_speed,
        "temperature": temperature,
        "dew_point": dew_point,
        "qnh": qnh,
        "visibility": visibility,
        "clouds_few": ",".join(map(str, clouds_few)), 
        "clouds_scattered": ",".join(map(str, clouds_scattered)),
        "clouds_broken": ",".join(map(str, clouds_broken)),
        "clouds_overcast": ",".join(map(str, clouds_overcast))
    }


print(parse_metar("301100Z 03006KT 350V060 9999 BKN018 BKN040 23/20 Q1016"))
