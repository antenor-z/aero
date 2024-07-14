from DB.addUser import add_user
from DB.PortableDataLoad import insert_initial_data
while(True):
    print("0: Exit")
    print("1: Insert initial data")
    print("2: Insert user")
    option = input("Option: ")
    if option == "0": break
    options = {
        "1": insert_initial_data,
        "2": add_user
    }
    options.get(option, None)()