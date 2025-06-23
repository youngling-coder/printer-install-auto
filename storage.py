import os
import json
import re
from typing import Optional
import shutil

from colorama import Style, Fore

from models import Printer, Location
from custom_inputs import get_yn_confirmation


class Storage:
    def __init__(self):
        self.__locations: list[Location] = []

    def add_printer_to_location(self, printer: Printer, location: Location) -> None:

        print()
        print(printer.to_str(0))
        print(
            f'{Style.BRIGHT}Will be added to "{Fore.CYAN + location.name + Fore.RESET}"\n'
        )

        action_confirmed = get_yn_confirmation("Proceed? [Y/n]: ")

        if action_confirmed:
            location.add_printer(printer)
            self.write_dict_as_json()

            print(
                f"{Style.BRIGHT + Fore.GREEN}✅ Printer added successfully!{Style.RESET_ALL}\n"
            )

    def create_location(
        self,
        location_name,
        save: bool = True,
        output: bool = True,
        confirm: bool = False,
    ) -> Location:

        if self.get_location_by_name(location_name):
            if output:
                print(
                    f"{Style.BRIGHT + Fore.YELLOW}⚠️  Location '{location_name}' already exists!{Style.RESET_ALL}\n"
                )

        else:
            action_confirmed = True

            if confirm:
                action_confirmed = get_yn_confirmation("Proceed? [Y/n]: ")

            if action_confirmed:
                self.__locations.append(Location(location_name))
                if output:
                    print(
                        f"{Style.BRIGHT + Fore.GREEN}✅ Location is created!{Style.RESET_ALL}\n"
                    )

                if save:
                    self.write_dict_as_json()

                return self.__locations[-1]

    def remove_location(self, location_idx) -> None:

        location = self.get_location_by_index(location_idx)

        if location and location.get_printers():
            print(
                f"{Style.BRIGHT + Fore.YELLOW}⚠️  Location '{location.name}' contain printers!{Fore.RESET} Delete all the printers from this location first!{Style.RESET_ALL}\n"
            )

        else:
            try:
                action_confirmed = get_yn_confirmation("Proceed? [Y/n]: ")

                if action_confirmed:
                    self.__locations.remove(location)
                    self.write_dict_as_json()
                    print(
                        f"{Style.BRIGHT + Fore.GREEN}✅ '{location.name}' location is removed!\n{Style.RESET_ALL}"
                    )

            except ValueError as e:
                print(
                    f"{Style.BRIGHT + Fore.YELLOW}⚠️  Skipping '{location.name}' as it is not present in the list!\n{Style.RESET_ALL}"
                )

    def remove_printer_from_location(
        self, printer: Printer, location: Location
    ) -> None:

        print(
            f"{Fore.YELLOW + Style.BRIGHT}⚠️  All the info about this printer will be removed!\n"
        )
        print(printer.to_str(0))

        action_confirmed = get_yn_confirmation("Proceed? [Y/n]: ")

        if action_confirmed:

            location_printers = location.get_printers()

            for idx in range(len(location_printers)):
                if location_printers[idx].ip == printer.ip:
                    location.get_printers().pop(idx)

            self.write_dict_as_json()
            print(
                f"{Style.BRIGHT + Fore.GREEN}✅ Printer removed successfully!\n{Style.RESET_ALL}"
            )

    def get_location_by_index(self, location_idx: int) -> Location:
        return self.__locations[location_idx]

    def is_ip_unique(self, ip):
        for printer in self.get_printers():

            if printer.ip == ip:
                return False

        return True

    def is_ip_valid(self, ip: str):

        ip_regex = re.compile(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$")

        return bool(ip_regex.match(ip) and self.is_ip_unique(ip))

    def get_location_by_name(self, name: str) -> Optional[Location]:
        for location in self.__locations:

            if location.name == name:
                return location

        return

    def to_dict(self) -> dict:

        json = {}

        for location in self.__locations:
            json[location.name] = location.get_printers(as_dicts=True)

        return json

    def get_locations(self) -> list[Location]:
        return self.__locations

    def get_printers(self, as_dicts: bool = False) -> list[Printer]:

        printers = []

        for location in self.__locations:
            printers.extend(location.get_printers(as_dicts))

        return printers

    def __read_json(self, path: str = "printers.json") -> dict:

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"{Style.BRIGHT + Fore.RED}JSON file not found!\n{Style.RESET_ALL}"
            )

        druckers = {}

        with open(path, "r") as drucker_file:
            druckers = json.load(drucker_file)

        return druckers

    def load_from_json(self, output: bool = True):

        self.__locations = []

        printers_locations_json = self.__read_json()

        for location_name in printers_locations_json.keys():

            location = self.create_location(location_name, output=output, save=False)

            for printer in printers_locations_json[location_name]:
                new_printer = Printer.from_dict(printer)

                location.add_printer(new_printer)

    def __backup_current_state(self, path: str = "printers.json"):
        backup_path = path + ".bak"
        shutil.copy2(path, backup_path)

    def restore_from_backup(self):

        os.remove("printers.json")
        os.rename("printers.json.bak", "printers.json")

        self.load_from_json()

    def write_dict_as_json(self, path: str = "printers.json"):

        data = self.to_dict()

        self.__backup_current_state()

        with open(path, "w") as drucker_file:
            json.dump(data, drucker_file, indent=4)
