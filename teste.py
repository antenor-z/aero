import re

item = "M03/06"  # Example input with negative temperature and dew point

if (temp := re.findall("(M?\d+)/(M?\d+)", item)) != []:
    [(temperature, dew_point)] = temp
    temperature = temperature.replace("M", "-")
    dew_point = dew_point.replace("M", "-")
    print((item, f"Temperatura <b>{temperature}</b>°C e ponto de orvalho <b>{dew_point}</b>°C."))

