from DB.ORM import *
import re
from security import TOTP, password
from sqlalchemy.exc import NoResultFound

def add_user():
    Session = sessionmaker(bind=engine)
    session = Session()

    name = input("Username: ")
    if not re.match("^[a-zA-Z0-9_]{3,30}$", name):
        exit("Invalid username format")

    passwd = input("Password: ")

    isSuper = input("Can create/delete airports (superuser)? (y/N)") in ["y", "Y"]

    CanEditAirportsList = None
    if not isSuper:
        CanEditAirportsList = input("Comma separated values of ICAOs this user can edit: ")
        for icao in CanEditAirportsList.split(","):
            if not re.match("^[A-Z]{4}$", icao):
                exit("Invalid ICAO code:", icao)


    TwoFactorKey = None
    if input("Generate TOTP? (y/N)") in ["y", "Y"]:
        TwoFactorKey = TOTP.gen2fa(name)
        token = input("Type TOTP token: ")
        while not TOTP.check2fa(TwoFactorKey, token):
            token = input("Type TOTP token: ")

    password_hash = password.hash_password(passwd)
    session.add(User(Name=name, 
                    PasswordHash=password_hash,
                    CanEditAirportsList=CanEditAirportsList,
                    IsSuper=isSuper,
                    TwoFactorKey=TwoFactorKey))

    session.commit()

def edit_user():
    Session = sessionmaker(bind=engine)
    session = Session()

    print(session.query(User.Name).all())

    try:
        name = input("Enter username to edit: ")
        user = session.query(User).filter_by(Name=name).one()

        choice = input("Do you want to change the password or TOTP? (password/TOTP): ").strip().lower()

        if choice == "password":
            passwd = input("Enter new password: ")
            user.PasswordHash = password.hash_password(passwd)

        elif choice == "totp":
            if input("Regenerate TOTP key? (y/N)") in ["y", "Y"]:
                user.TwoFactorKey = TOTP.gen2fa(user.Name)
                token = input("Type new TOTP token: ")
                while not TOTP.check2fa(user.TwoFactorKey, token):
                    token = input("Type TOTP token again: ")

        session.commit()
        print(f"User '{user.Name}' updated successfully!")

    except NoResultFound:
        print(f"User '{name}' not found.")
    finally:
        session.close()


def remove_user():
    Session = sessionmaker(bind=engine)
    session = Session()

    print(session.query(User.Name).all())

    try:
        name = input("Enter username to remove: ")
        user = session.query(User).filter_by(Name=name).one()

        confirm = input(f"Are you sure you want to delete user '{user.Name}'? (y/N): ")
        if confirm in ["y", "Y"]:
            session.delete(user)
            session.commit()
            print(f"User '{user.Name}' removed successfully!")
        else:
            print("Operation canceled.")

    except NoResultFound:
        print(f"User '{name}' not found.")
    finally:
        session.close()
