import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from datetime import timedelta

from DB.Getter import get_all_icao, latest_n_metars_parsed

def plot_metar_data(icao: str, metar_data: list[dict], data_name, label_name: str, label_color: str):
    timestamps = [(data["timestamp"] - timedelta(hours=3)).strftime("%d/%m %H:%M") for data in metar_data if data]
    dat = [data[data_name] for data in metar_data if data]
    fig, ax1 = plt.subplots()

    fig.set_size_inches(12, 4)

    ax1.set_ylabel(label_name)
    ax1.plot(timestamps, dat, 'o-', color=f'tab:{label_color}', label=label_name)
    ax1.tick_params(axis='y', labelcolor=f'tab:{label_color}')

    fig.tight_layout()

    filename = f"static/plots/{icao}-{data_name}.png"
    plt.savefig(filename)
    plt.close(fig)
    print(f"Plot saved as {filename}")

def plot(icao, metar_data):
    plot_metar_data(icao, metar_data, "temperature", "Temperatura", "red")
    plot_metar_data(icao, metar_data, "wind_speed", "Velocidade do vento", "blue")
    plot_metar_data(icao, metar_data, "wind_direction", "Direção do vento", "green")

def update_images():
    for icao in get_all_icao():
        latest = latest_n_metars_parsed(icao=icao)
        plot(icao=icao, metar_data=latest)
        print(icao, latest)
