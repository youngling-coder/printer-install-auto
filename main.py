import os
import sys
import logging
import threading

from colorama import Style, Fore

from argparser import build_arg_parser
from custom_inputs import (
    get_current_action,
    input_printer_data,
    select_printer_data,
    get_location_index_input,
    get_generic_input,
)
from storage import Storage
from models import Printer, Location
from utils import show_overview_of_storage
from installer import Installer
import web_ui


def run_web_ui():
    # Suppress Flask output
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    web_ui.app.logger.disabled = True
    web_ui.app.run(port=8765, use_reloader=False, debug=False)


def cli_main(args):
    storage = Storage()
    storage.load_from_json(output=False)

    printer = Printer.from_dict(
        {
            "ip": "",
            "name": "",
            "driver_inf_path": "",
            "model": "",
            "driver_name": "",
        }
    )

    match args.action:
        case "overview":
            show_overview_of_storage(storage)

        case "add":
            printer.ip = args.ip
            printer.name = args.name
            printer.driver_name = args.driver_name
            printer.driver_inf_path = args.driver_inf_path
            printer.model = args.model

            _, location = storage.get_location_by_name(args.location_name)

            if not location:
                print(
                    f"{Style.BRIGHT + Fore.RED}❌ Location not found! {Style.RESET_ALL}"
                )
                return

            storage.add_printer_to_location(printer, location)

        case "remove":

            printer = storage.get_printer_by_ip(args.ip)

            if not printer:
                print(
                    f"{Style.BRIGHT + Fore.RED}❌ Printer not found! {Style.RESET_ALL}"
                )
                return

            _, location = storage.get_location_by_name(args.location_name)

            if not location:
                print(
                    f"{Style.BRIGHT + Fore.RED}❌ Location not found! {Style.RESET_ALL}"
                )
                return

            storage.remove_printer_from_location(printer, location)

        case "install":
            printer = storage.get_printer_by_ip(args.ip)

            if not printer:
                print(
                    f"{Style.BRIGHT + Fore.RED}❌ Printer not found! {Style.RESET_ALL}"
                )
                return

            installer = Installer(printer)
            installer.run()

        case "create-location":
            storage.create_location(args.location_name, confirm=True)

        case "remove-location":
            location_idx, _ = storage.get_location_by_name(args.location_name)

            if not location_idx:
                print(
                    f"{Style.BRIGHT + Fore.RED}❌ Location not found! {Style.RESET_ALL}"
                )
                return

            storage.remove_location(location_idx)

        case "restore":
            storage.restore_from_backup()

        case "backup":
            storage.create_backup()


def interactive_main():
    threading.Thread(target=run_web_ui, daemon=True).start()

    while True:
        storage = Storage()
        storage.load_from_json(output=False)

        os.system("cls" if os.name == "nt" else "clear")

        print(f'Type {Style.BRIGHT}"exit"{Style.RESET_ALL} to quit the program\n')

        current_action = get_current_action()

        match current_action:
            case 1:
                show_overview_of_storage(storage)
            case 2:
                printer, location = input_printer_data(storage)
                storage.add_printer_to_location(printer, location)
            case 3:
                printer, location = select_printer_data(storage)
                storage.remove_printer_from_location(printer, location)
            case 4:
                printer, _ = select_printer_data(storage)
                installer = Installer(printer)
                installer.run()
            case 5:
                location_name = get_generic_input(
                    "Enter new location's name: ", empty=False
                )
                storage.create_location(location_name, confirm=True)
            case 6:
                location_idx = get_location_index_input(storage.get_locations())
                storage.remove_location(location_idx)
            case 7:
                storage.restore_from_backup()
            case 8:
                storage.create_backup(manual=True)

        input(
            f"{Style.BRIGHT + Fore.CYAN}Press ENTER to continue...\n{Style.RESET_ALL}"
        )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = build_arg_parser()
        args = parser.parse_args()
        cli_main(args)
    else:
        interactive_main()
