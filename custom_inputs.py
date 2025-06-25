from typing import Optional
from colorama import Style, Fore
import utils
import sys, os
from models import Printer, Location


printer_base_data = {
    "ip": "",
    "name": "",
    "driver_inf_path": "",
    "model": "",
    "driver": "",
}


def get_generic_input(prompt: str, empty: bool = True) -> str:

    while True:
        value = input(prompt)
        print()

        if value.lower() == "exit":
            sys.exit(0)

        if not empty and not value.strip():
            continue

        return value


def get_yn_confirmation(prompt: str) -> bool:

    confirmation = get_generic_input(Style.BRIGHT + prompt + Style.RESET_ALL)

    return confirmation.lower().startswith("y") or confirmation == ""


def get_ip_input(storage) -> str:

    while True:

        try:
            value = get_generic_input("Enter printer's IP address: ")

            if not storage.is_ip_valid(value):
                raise ValueError(
                    f"{Style.BRIGHT + Fore.RED}Entered IP is invalid!\n{Style.RESET_ALL}"
                )

            return value

        except ValueError as e:
            print(e)


def get_integer_input(prompt: str, range_: Optional[range] = None):

    while True:
        try:
            value = int(get_generic_input(prompt))

            if range_ and (value not in range_):
                raise IndexError(
                    f"Value is out of range!\n"
                )

            return value

        except ValueError:
            utils.print_error(f"Incompatible value!\n")

        except IndexError as e:
            utils.print_error(e)


def get_printer_index_input(location: Location):
    
    location.overview()

    printer_id = get_integer_input(
        f"Select printer: ", range_=range(1, len(location.get_printers()) + 1)
    )

    return printer_id - 1


def get_location_index_input(locations: Location) -> int:

    print(utils.prettified_locations_output(locations))

    location_id = get_integer_input(
        "Enter city number: ", range_=range(1, len(locations) + 1)
    )

    return location_id - 1


def get_current_action():
    utils.help_()

    current_action = get_integer_input(
        "Enter action you want to perform: ", range_=range(1, utils.total_actions_count + 1)
    )

    return current_action


def input_printer_data(storage) -> tuple[Printer, Location]:

    location = storage.get_location_by_index(
        get_location_index_input(storage.get_locations())
    )
    new_printer = printer_base_data.copy()

    new_printer["ip"] = get_ip_input(storage)
    new_printer["name"] = get_generic_input(f"Enter printer's name: ", empty=False)
    new_printer["model"] = get_generic_input(f"Enter printer's model: ", empty=False)
    new_printer["driver_name"] = get_generic_input(
        f"Enter printer's driver name: ", empty=False
    )
    new_printer["driver_inf_path"] = get_generic_input(
        f"Enter printer's driver path: ", empty=False
    )
    printer = Printer.from_dict(new_printer)

    return printer, location


def select_printer_data(storage) -> tuple[Printer, Location]:
    location_idx = get_location_index_input(storage.get_locations())
    location = storage.get_location_by_index(location_idx)

    printer_idx = get_printer_index_input(location)
    printer = location.get_printer_by_idndex(printer_idx)

    return printer, location
