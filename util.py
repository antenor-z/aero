import re

import requests
def is_icao_valid(icao: str) -> bool:
    if len(re.findall("^[A-Z]{4}$", icao)) == 1 and icao.startswith("SB"):
        return True
    else:
        return False


accent_map = {
        'ã': 'a', 'á': 'a', 'â': 'a', 'à': 'a', 'ä': 'a', 'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i', 'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u', 'ç': 'c', 'ñ': 'n'
    }


def replace_accents(text):
    return ''.join(accent_map.get(char, char) for char in text)


def get_city_name_for_IBGE_API(city):
    return replace_accents(city.strip()).lower().replace(" ", "-")


def get_city_and_code_from_IGBE(city, state_code):
    formatted_city = get_city_name_for_IBGE_API(city)
    print(city)
    res = requests.get(f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{formatted_city}")
    if res.status_code != 200:
        return None

    city_data = res.json()

    if isinstance(city_data, list):
        for city in city_data:
            if str(city["microrregiao"]["mesorregiao"]["UF"]["id"]) == str(state_code):
                return city["id"], city["nome"]
    elif "id" in city_data and "nome" in city_data:
        if city_data["microrregiao"]["mesorregiao"]["UF"]["id"] == state_code:
            return city_data["id"], city_data["nome"]

    return None


def windhead_filter(speed):
    if speed > 0:
        return f"{speed} kt (vindo de frente)"
    elif speed < 0:
        return f"{-speed} kt (vindo de trás)"
    else:
        return "zero"
    
def windcross_filter(speed):
    if speed > 0:
        return f"{speed} kt (vindo da direita)"
    elif speed < 0:
        return f"{-speed} kt (vindo da esquerda)"
    else:
        return "zero"