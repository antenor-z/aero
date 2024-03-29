import re

# Fonte: https://ajuda.decea.mil.br/base-de-conhecimento/como-decodificar-o-metar-e-o-speci/

other_items = {
    "SH": "Pancada(s) moderada.",
    "+SH": "Pancada(s) forte.",
    "-FZ": "Congelante leve.",
    "FZ": "Congelante moderado.",
    "+FZ": "Congelante forte.",
    "-DZ": "Chuvisco leve.",
    "DZ": "Chuvisco moderado.",
    "+DZ": "Chuvisco forte.",
    "-RA": "Chuva leve.",
    "RA": "Chuva moderada.",
    "+RA": "Chuva forte.",
    "-SN": "Neve leve.",
    "SN": "Neve moderada.",
    "+SN": "Neve forte.",
    "-SG": "Grãos de neve leve.",
    "SG": "Grãos de neve moderado.",
    "+SG": "Grãos de neve forte.",
    "-PL": "Pelotas de gelo leve.",
    "PL": "Pelotas de gelo moderado.",
    "+PL": "Pelotas de gelo forte.",
    "-GR": "Granizo leve.",
    "GR": "Granizo moderado.",
    "+GR": "Granizo forte.",
    "-GS": "Granizo pequeno e/ou grãos de neve leve.",
    "GS": "Granizo pequeno e/ou grãos de neve moderado.",
    "+GS": "Granizo pequeno e/ou grãos de neve forte.",
    "-BR": "Névoa úmida leve.",
    "BR": "Névoa úmida moderada.",
    "+BR": "Névoa úmida densa.",
    "-FG": "Nevoeiro leve.",
    "FG": "Nevoeiro moderado.",
    "+FG": "Nevoeiro denso.",
    "-FU": "Fumaça leve.",
    "FU": "Fumaça moderada.",
    "+FU": "Fumaça densa.",
    "-VA": "Cinzas vulcânicas leve.",
    "VA": "Cinzas vulcânicas moderada.",
    "+VA": "Cinzas vulcânicas densa.",
    "-DU": "Poeira extensa leve.",
    "DU": "Poeira extensa moderada.",
    "+DU": "Poeira extensa densa.",
    "-SA": "Areia leve.",
    "SA": "Areia moderada.",
    "+SA": "Areia densa.",
    "-HZ": "Névoa seca leve.",
    "HZ": "Névoa seca moderada.",
    "+HZ": "Névoa seca densa.",
    "-PO": "Poeira/areia em redemoinhos leve.",
    "PO": "Poeira/areia em redemoinhos moderada.",
    "+PO": "Poeira/areia em redemoinhos densa.",
    "-SQ": "Tempestade leve.",
    "SQ": "Tempestade moderada.",
    "+SQ": "Tempestade forte.",
    "-FC": "Nuvem(ns) funil (tornado ou tromba d’água) leve.",
    "FC": "Nuvem(ns) funil (tornado ou tromba d’água) moderada.",
    "+FC": "Nuvem(ns) funil (tornado ou tromba d’água) densa.",
    "-SS": "Tempestade de areia leve.",
    "SS": "Tempestade de areia moderada.",
    "+SS": "Tempestade de areia densa.",
    "-DS": "Tempestade de poeira leve.",
    "DS": "Tempestade de poeira moderada.",
    "+DS": "Tempestade de poeira densa.",
    "-TS": "Trovoada, Raios e Relâmpagos leve.",
    "TS": "Trovoada, Raios e Relâmpagos moderada.",
    "+TS": "Trovoada, Raios e Relâmpagos densa.",
    "RERA": "Fenômenos meteorológicos recentes.",
    "WS": "Tesoura de vento (windshear)",
    "NSC": "No Significant Cloud, podem haver algumas nuvens, mas nenhuma está abaixo de 5000 pés ou dentro de 10 quilômetros.",
}

def decode(metar: str) -> dict:
    #metar = "METAR SBSP 290400Z AUTO 19008KT 160V220 9999 FEW006 SCT008 BKN010 16/14 Q1025="
    #metar = "METAR SBSP 290400Z AUTO VRB08KT 160V220 9999 FEW006 SCT008 BKN010 16/14 Q1025="
    #metar = "METAR SBMN 061300Z 31015G27KT 280V350 5000 1500W -RA BKN010 SCT020 FEW025TCU 25/24 Q1014 RERA WS RWY17 W12/H75="

    metar = metar.split(" ")
    day = metar[0][0:2]
    timeZ = metar[0][2:6]
    ret = []
    ret.append((metar[0], f"Dia {day[0:3]}. Horário {timeZ[0:2]}:{timeZ[2:4]} zulu (UTC)."))

    metar = metar[1:]

    for item in metar:
        if item == "AUTO":
            ret.append((item, "Informação obtida automaticamente."))
        
        elif item == "9999":
            ret.append((item, "Visibilidade ilimitada"))
        
        elif (vis := re.findall("^(\d{4})$", item)) != [] and vis != "9999":
            [vis] = vis
            ret.append((item, f"Visibilidade {vis} metros."))
        
        elif (vis := re.findall("^(\d{4})([A-Z]+)$", item)) != []:
            [(vis, sector)] = vis
            if sector == "N": sector = "norte"
            elif sector == "S": sector = "sul"
            elif sector == "W": sector = "oeste"
            elif sector == "E": sector = "leste"
            elif sector == "NE": sector = "nordeste"
            elif sector == "NW": sector = "noroeste"
            elif sector == "SE": sector = "sudeste"
            elif sector == "SW": sector = "sudoeste"
        
            ret.append((item, f"No setor {sector} do aerodromo, visibilidade {vis}m."))
        
        elif (wind := re.findall("(\d{3})(\d{2})KT", item)) != []:
            [(direction, speed)] = wind
            ret.append((item, f"Vento proa {direction}° com velocidade {speed} nós (kt)."))
        
        elif (wind := re.findall("VRB(\d{2})KT", item)) != []:
            [speed] = wind
            ret.append((item, f"Vento com direção variável e velocidade {speed} nós (kt)."))
        
        elif (wind := re.findall("(\d{3})(\d+)G(\d+)KT", item)) != []:
            [(direction, speed, gust)] = wind
            ret.append((item, f"Vento proa {direction}° com velocidade {speed} nós (kt) e rajadas de {gust} nós."))
        
        elif (wind := re.findall("(\d{3})V(\d{3})", item)) != []:
            [(wind1, wind2)] = wind
            ret.append((item, f"Vento variável de proa {wind1}° até {wind2}°."))
        
        elif (cloud := re.findall("([A-Z]{3})(\d{3})", item)) != []:
            [(cloud_type, cloud_altitude)] = cloud
            cloud_altitude = int(cloud_altitude) * 100

            if cloud_type == "OVC": cloud_type = "Totalmente encoberto"
            elif cloud_type == "BKN": cloud_type = "Nuvens quebradas (5/8 a 7/8 do céu com nuvens)"
            elif cloud_type == "SCT": cloud_type = "Nuvens espalhadas (3/8 a 4/8 do céu com nuvens)"
            elif cloud_type == "FEW": cloud_type = "Poucas nuvens (1/8 a 2/8 do céu com nuvens)"
            ret.append((item, f"{cloud_type} em {cloud_altitude} pés de altitude."))

        elif (temp := re.findall("(\d+)/(\d+)", item)) != []:
            [(temperature, dew_point)] = temp
            if (int(temperature) - int(dew_point) < 4):
                ret.append((item, f"Temperatura {temperature}°C e ponto de orvalho {dew_point}°C. Existe chance de chuva, pois as duas temperaturas estão próximas."))
            else:
                ret.append((item, f"Temperatura {temperature}°C e ponto de orvalho {dew_point}°C. Provavelmente não choverá, pois as duas temperaturas estão distantes."))
        
        elif (qnh := re.findall("Q(\d{4})", item)) != []:
            [qnh] = qnh
            ret.append((item, f"O altímetro deve ser ajustado para a pressão {qnh} hPa"))
        
        elif item == "CAVOK":
            ret.append((item, "Ceiling and Visibility OK. Sem nuvens e visibilidade OK."))
        
        elif (runway := re.findall("RWY(\d{2}[RLC]*)", item)) != []:
            [runway] = runway
            ret.append((item, f"Informação anterior se refere a pista {runway}"))
        
        elif item in other_items:
            ret.append((item, other_items[item]))
        
        else:
            ret.append((item, ""))

    return ret

def get_wind_info(metar: str) -> dict:
    if (wind := re.findall("(\d{3})(\d{2})KT", metar)) != []:
        [(direction, speed)] = wind
        return {"direction": int(direction), "speed": int(speed)}
    else:
        raise DecodeError("Could not find wind information.")

class DecodeError(Exception):
    def __init__(self, message):
        super().__init__(message)

if __name__ == "__main__":
    metar = "METAR SBMN 061300Z 31015G27KT 280V350 5000 1500W -RA -DU BKN010 SCT020 FEW025TCU 25/24 Q1014 RERA WS RWY17 W12/H75="
    print(decode(metar))
