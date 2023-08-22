from Wind import get_components
def test_get_wind():
    a = get_components(runway_head=30, wind_dir=60, wind_speed=12)
    assert(round(a["paral"], 2) == 10.39 and round(a["cross"], 2) == 6)

    a = get_components(runway_head=30, wind_dir=215, wind_speed=12)
    assert(round(a["paral"], 2) == -11.95 and round(a["cross"], 2) == -1.05)

    a = get_components(runway_head=160, wind_dir=12, wind_speed=6)
    assert(round(a["paral"], 2) == -5.09 and round(a["cross"], 2) == -3.18)

    a = get_components(runway_head=160, wind_dir=240, wind_speed=6)
    assert(round(a["paral"], 2) == 1.04 and round(a["cross"], 2) == 5.91)
    
