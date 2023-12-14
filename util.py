import re
def is_icao_valid(icao: str) -> bool:
    if len(re.findall("^[A-Z]{4}$", icao)) == 1 and icao.startswith("SB"):
        return True
    else:
        return False