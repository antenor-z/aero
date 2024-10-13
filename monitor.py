from DB.Getter import get_all_icao
from DB.UserCtl import add_user, edit_user, remove_user
from DB.PortableDataLoad import insert_initial_data
from ext import update_metars, update_tafs
from historyPlot import update_images
import asyncio

loop = asyncio.get_event_loop()
def update_all_metars(): loop.run_until_complete(update_metars())
def update_all_tafs(): loop.run_until_complete(update_tafs())
def update_all_images(): loop.run_until_complete(update_images())
def exit_now(): exit()

print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
print("ADMIN")
print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

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