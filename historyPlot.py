import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from datetime import timedelta

from DB.Getter import get_all_icao, latest_n_metars_parsed


def plot_metar_data(icao: str,
                    metar_data: list[dict],
                    data_name1: str,
                    label_name1: str,
                    label_color1: str,
                    data_name2: str,
                    label_name2: str,
                    label_color2: str):

    timestamps = [(data["timestamp"] - timedelta(hours=3)).strftime("%d/%m %H:%M") for data in metar_data if data]
    data1 = [data[data_name1] for data in metar_data if data]
    data2 = [data[data_name2] for data in metar_data if data]

    fig, ax1 = plt.subplots()
    fig.set_size_inches(12, 4)

    ax1.set_ylabel(label_name1, color=f'tab:{label_color1}')
    ax1.plot(timestamps, data1, 'o-', color=f'tab:{label_color1}', label=label_name1)
    ax1.tick_params(axis='y', labelcolor=f'tab:{label_color1}')

    ax2 = ax1.twinx()
    ax2.set_ylabel(label_name2, color=f'tab:{label_color2}')
    ax2.plot(timestamps, data2, 's-', color=f'tab:{label_color2}', label=label_name2)
    ax2.tick_params(axis='y', labelcolor=f'tab:{label_color2}')

    fig.tight_layout()
    filename = f"static/plots/{icao}-{data_name1}-{data_name2}.png"
    plt.savefig(filename)
    plt.close(fig)
    print(f"Plot saved as {filename}")


def plot(icao, metar_data):
    plot_metar_data(icao, metar_data, "temperature", "Temperatura", "red", "dew_point", "Ponto de orvalho", "green")
    plot_metar_data(icao, metar_data, "wind_speed", "Velocidade do vento", "blue", "wind_direction", "Direção do vento", "green")
    plot_metar_data(icao, metar_data, "qnh", "Ajuste altímetro", "blue", "visibility", "Visibilidade", "green")


def update_images():
    for icao in get_all_icao():
        latest = latest_n_metars_parsed(icao=icao)
        plot(icao=icao, metar_data=latest)
        print(icao, latest)
