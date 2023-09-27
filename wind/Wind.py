import math

def sanity_check(heading):
    if heading < 0 or heading >= 360:
        raise Exception(f"Heading {heading} outside range.")

def get_components(runway_head: int, wind_dir:int, wind_speed: int):
    sanity_check(runway_head)
    sanity_check(wind_dir)
    # Dot product:
    # A.B = (Ax*Bx) + (Ay*By) = |A|*|B|*cos(x)

    alpha = math.radians(runway_head)
    (ax, ay) = (math.cos(alpha), math.sin(alpha))

    beta = math.radians(wind_dir)
    (bx, by) = (math.cos(beta), math.sin(beta))

    AB = (ax * bx) + (ay * by)

    angle_diff = math.acos(AB)

    sign = -1 
    if 0 <= (wind_dir - runway_head) % 360 <= 180:
        sign = 1

    return {"paral": math.cos(angle_diff) * wind_speed, 
            "cross": sign * math.sin(angle_diff) * wind_speed}

def get_runway_in_use(runway_names: list, wind_dir:int, wind_speed:int) -> list | None:
    if wind_speed == 0:
        return None

    runway_group = {}
    for runway in runway_names:
        if runway[-1] == "R" or runway[-1] == "L" or runway[-1] == "C":
            r = int(runway[:-1])
        else:
            r = int(runway)
        if runway_group.get(r) == None:
            runway_group[r] = [runway]
        else:
            runway_group[r].append(runway)

    highest_paral_wind = 0 # The highest head wind yet
    highest_runway = None # Runway group with the highest head wind

    for runway in runway_group.keys():
        runway_heading = int(runway) * 10
        paral_wind = get_components(runway_heading, wind_dir=wind_dir, wind_speed=wind_speed)["paral"]
        if paral_wind > highest_paral_wind:
            highest_paral_wind = paral_wind
            highest_runway = runway
    
    return runway_group[highest_runway]
