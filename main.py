import os
import sys
from colorama import Style, Fore

from argparser import build_arg_parser
from custom_inputs import (
    get_current_action,
    input_printer_data,
    select_printer_data,
    get_location_index_input,
    get_generic_input,
)
from installer import Installer
from models import Printer
import utils


def cli_main(args):
    storage = utils.get_storage()

    match args.action:
        case "overview":
            if args.location:
                _, location = utils.handle_location_check(storage, args.location)
                if location:
                    utils.show_overview_of_location(location)
            else:
                utils.show_overview_of_storage(storage)

        case "add":
            printer = Printer.from_dict(
                {
                    "ip": args.ip,
                    "name": args.name,
                    "driver_inf_path": args.driver_inf_path,
                    "model": args.model,
                    "driver_name": args.driver_name,
                }
            )
            _, location = utils.handle_location_check(storage, args.location_name)
            if location:
                storage.add_printer_to_location(printer, location)

        case "remove":
            printer = utils.handle_printer_check(storage, args.ip)
            _, location = utils.handle_location_check(storage, args.location_name)
            if printer and location:
                storage.remove_printer_from_location(printer, location)

        case "install":
            printer = utils.handle_printer_check(storage, args.ip)
            if printer:
                Installer(printer).run()

        case "create-location":
            storage.create_location(args.location_name, confirm=True)

        case "remove-location":
            idx, _ = utils.handle_location_check(storage, args.location_name)
            if idx is not None:
                storage.remove_location(idx)

        case "restore":
            storage.restore_from_backup()

        case "backup":
            storage.create_backup()


def interactive_main():
    os.system("cls")

    while True:
        storage = utils.get_storage()

        match get_current_action():
            case 1:
                name = get_generic_input(
                    f"{Style.BRIGHT + Fore.CYAN}[ Optional ]{Style.RESET_ALL} Enter location name: "
                )
                if name:
                    _, location = utils.handle_location_check(storage, name)
                    if location:
                        location.overview()
                else:
                    storage.overview()

            case 2:
                printer, location = input_printer_data(storage)
                storage.add_printer_to_location(printer, location)

            case 3:
                printer, location = select_printer_data(storage)
                if not printer:
                    utils.print_error("Printer not found!")

                else:
                    storage.remove_printer_from_location(printer, location)

            case 4:
                printer, _ = select_printer_data(storage)
                Installer(printer).run()

            case 5:
                name = get_generic_input("Enter new location's name: ", empty=False)
                storage.create_location(name, confirm=True)

            case 6:
                idx = get_location_index_input(storage.get_locations())
                storage.remove_location(idx)

            case 7:
                storage.restore_from_backup()

            case 8:
                storage.create_backup(manual=True)

        print()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = build_arg_parser().parse_args()
        cli_main(args)
    else:
        interactive_main()
