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
                printer, _ = select_printer_data(storage)
                install_printer(printer)

            case 6:
                storage.restore_from_backup()

        input(
            f"\n{Style.BRIGHT + Fore.CYAN}Press ENTER to continue...\n{Style.RESET_ALL}"
        )


main()
