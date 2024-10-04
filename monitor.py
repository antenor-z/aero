from DB.Getter import get_all_icao
from DB.UserCtl import add_user, edit_user, remove_user
from DB.PortableDataLoad import insert_initial_data
from ext import update_metars, update_tafs
from historyPlot import update_images
from asyncio import run

def update_all_metars(): run(update_metars(get_all_icao()))
def update_all_tafs(): run(update_tafs(get_all_icao()))
def update_all_images(): run(update_images())
def exit_now(): exit()

while(True):
    options = {
        "0": exit_now,
        "1": insert_initial_data,
        "2": add_user,
        "3": edit_user,
        "4": remove_user,
        "5": update_all_metars,
        "6": update_all_tafs,
        "7": update_all_images
    }
    for num, func in options.items():
        print(f"{num}: {func.__name__}")

    option = input("Option: ")
    options.get(option, None)()