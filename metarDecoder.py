import re
from metar import get_metar

# Fonte: https://ajuda.decea.mil.br/base-de-conhecimento/como-decodificar-o-metar-e-o-speci/


def decode(icao: str) -> dict:
    metar, is_cache = get_metar(icao)
    #metar = "METAR SBSP 290400Z AUTO 19008KT 160V220 9999 FEW006 SCT008 BKN010 16/14 Q1025="
    #metar = "METAR SBSP 290400Z AUTO VRB08KT 160V220 9999 FEW006 SCT008 BKN010 16/14 Q1025="
    #metar = "METAR SBMN 061300Z 31015G27KT 280V350 5000 1500W -RA BKN010 SCT020 FEW025TCU 25/24 Q1014 RERA WS RWY17 W12/H75="

    metar = metar.split(" ")
    assert(metar[0] == "METAR" and metar[1] == icao.upper())

    metar = metar[2:]

    day = metar[0][0:2]
    timeZ = metar[0][2:6]
    ret = []
    ret.append((metar[0], f"Dia {day[0:3]}. Horário {timeZ[0:2]}:{timeZ[2:4]} zulu (UTC)."))

    metar = metar[1:]

    for item in metar:
        if item == "AUTO":
            ret.append((item, "Informação obtida automaticamente."))
        elif (wind := re.findall("(\d{3})(\d{2})KT", item)) != []:
            [(direction, speed)] = wind
            ret.append((item, f"Vento proa {direction}° com velocidade de {speed} nós (kt)."))
        elif (temp := re.findall("(\d+)/(\d+)", item)) != []:
            [(temperature, dew_point)] = temp
            ret.append((item, f"Temperatura {temperature}°C e ponto de orvalho {dew_point}°C. Quanto mais próximo os dois estiverem, maior a chance de chuva."))
        elif (qnh := re.findall("Q(\d{4})", item)) != []:
            [qnh] = qnh
            ret.append((item, f"O altímetro deve ser ajustado para a pressão {qnh} kPa"))
        elif item == "CAVOK":
            ret.append((item, "Ceiling and Visibility OK. Teto e visibilidade OK."))
        else:
            ret.append((item, ""))

    return ret

if __name__ == "__main__":
    print(decode("SBMN"))