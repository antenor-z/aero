import re

# Fonte: https://ajuda.decea.mil.br/base-de-conhecimento/como-decodificar-o-metar-e-o-speci/


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
        
        elif item == "-RA":
            ret.append((item, f"Chuva leve."))
        
        elif item == "RA":
            ret.append((item, f"Chuva moderada."))
        
        elif item == "+RA":
            ret.append((item, f"Chuva forte."))

            
        elif item == "-DZ":
            ret.append((item, f"Chuvisco leve."))
        
        elif item == "DZ":
            ret.append((item, f"Chuvisco moderado."))
        
        elif item == "+DZ":
            ret.append((item, f"Chuvisco forte."))


        elif item == "-GR":
            ret.append((item, f"Granizo leve."))
        
        elif item == "GR":
            ret.append((item, f"Granizo moderado."))
        
        elif item == "+GR":
            ret.append((item, f"Granizo forte."))

        
        
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
    metar = "METAR SBMN 061300Z 31015G27KT 280V350 5000 1500W -RA BKN010 SCT020 FEW025TCU 25/24 Q1014 RERA WS RWY17 W12/H75="
    print(decode(metar))
