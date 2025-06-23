import os
import logging
import threading
from colorama import Style, Fore
from custom_inputs import (
    get_current_action,
    input_printer_data,
    select_printer_data,
    get_location_index_input,
    get_generic_input,
)
from storage import Storage
from installer import Installer
import web_ui


def run_web_ui():
    # Suppress Flask output
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    web_ui.app.logger.disabled = True

    web_ui.app.run(port=8765, use_reloader=False, debug=False)


def main():

    threading.Thread(target=run_web_ui, daemon=True).start()

    while True:
        storage = Storage()
        storage.load_from_json()

        os.system("cls")

        print(f'Type {Style.BRIGHT}"exit"{Style.RESET_ALL} to quit the program\n')

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
                installer = Installer(printer)
                installer.run()

            case 4:
                location_name = get_generic_input(
                    "Enter new location's name: ", empty=False
                )
                storage.create_location(location_name, confirm=True)

            case 5:
                location_idx = get_location_index_input(storage.get_locations())
                storage.remove_location(location_idx)

            case 6:
                storage.restore_from_backup()

        input(
            f"{Style.BRIGHT + Fore.CYAN}Press ENTER to continue...\n{Style.RESET_ALL}"
        )


if __name__ == "__main__":
    main()
