import os
from colorama import Style, Fore
from custom_inputs import (
    get_current_action,
    input_printer_data,
    get_location_id_input,
    get_printer_id_input,
    select_printer_data,
)
from actions import install_printer
from storage import Storage

# TODO: Add/Remove Location functionality
# TODO: Restore from backup functionality
# TODO: Maybe export as HTML for better overview
# TODO: GUI - ???

def main():

    while True:
        storage = Storage()
        storage.load_from_json()
        locations = storage.get_locations()

        os.system("cls")
        print(
            f'Type {Style.BRIGHT}"exit"{Style.RESET_ALL} to quit the program, ', end=""
        )
        print(f'{Style.BRIGHT}"help_"{Style.RESET_ALL} to show help.\n')

        current_action = get_current_action()

        match current_action:
            case 1:
                printer, location = input_printer_data(storage)
                storage.add_printer_to_location(printer, location)

            case 2:
                printer, location = select_printer_data(storage)
                storage.remove_printer_from_location(printer, location)

            case 3:

                location_id = get_location_id_input(locations)
                location = storage.get_location_by_id(location_id)

                printer_id = get_printer_id_input(location)
                printer = location.get_printer_by_id(printer_id)

                install_printer(
                    printer.ip,
                    printer.name,
                    printer.driver_inf_path,
                    printer.driver_name,
                )

        input(
            f"\n{Style.BRIGHT + Fore.CYAN}Press any key to continue...\n{Style.RESET_ALL}"
        )


main()
