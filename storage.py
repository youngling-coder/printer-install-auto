import os
import json
import re
import shutil

from colorama import Style, Fore

from models import Printer, Location
import custom_inputs


class Storage:
    def __init__(self):
        self.__filename: str = "printers.json"
        self.__backup_file: str = f"{self.__filename}.bak"
        self.__locations: list[Location] = []

    def add_printer_to_location(self, printer: Printer, location: Location) -> None:

        print()
        print(printer.to_str(0))
        print(
            f'{Style.BRIGHT}Will be added to "{Fore.CYAN + location.name + Fore.RESET}"\n'
        )

        action_confirmed = custom_inputs.get_yn_confirmation("Proceed? [Y/n]: ")

        if action_confirmed:
            location.add_printer(printer)

            print(
                f"{Style.BRIGHT + Fore.GREEN}✅ Printer added successfully!{Style.RESET_ALL}"
            )

            self.write_dict_as_json()

    def create_location(
        self,
        location_name,
        save: bool = True,
        output: bool = True,
        confirm: bool = False,
    ) -> Location:

        if self.get_location_by_name(location_name)[1]:
            if output:
                print(
                    f"{Style.BRIGHT + Fore.YELLOW}⚠️  Location '{location_name}' already exists!{Style.RESET_ALL}"
                )

        else:
            action_confirmed = True

            if confirm:
                action_confirmed = custom_inputs.get_yn_confirmation("Proceed? [Y/n]: ")

            if action_confirmed:
                self.__locations.append(Location(location_name))
                if output:
                    print(
                        f"{Style.BRIGHT + Fore.GREEN}✅ Location '{location_name}' is created!{Style.RESET_ALL}"
                    )

                if save:
                    self.write_dict_as_json()

                return self.__locations[-1]

    def remove_location(self, location_idx) -> None:

        location = self.get_location_by_index(location_idx)

        if location and location.get_printers():
            print(
                f"{Style.BRIGHT + Fore.YELLOW}⚠️  Location '{location.name}' contain printers!{Fore.RESET} Delete all the printers from this location first!{Style.RESET_ALL}"
            )

        else:
            try:
                action_confirmed = custom_inputs.get_yn_confirmation("Proceed? [Y/n]: ")

                if action_confirmed:
                    self.__locations.remove(location)
                    print(
                        f"{Style.BRIGHT + Fore.GREEN}✅ '{location.name}' location is removed!\n{Style.RESET_ALL}"
                    )
                    self.write_dict_as_json()

            except ValueError as e:
                print(
                    f"{Style.BRIGHT + Fore.YELLOW}⚠️  Skipping '{location.name}' as it is not present in the list!\n{Style.RESET_ALL}"
                )

    def remove_printer_from_location(
        self, printer: Printer, location: Location
    ) -> None:

        print(
            f"{Fore.YELLOW + Style.BRIGHT}⚠️  All the info about this printer will be removed!"
        )
        print(printer.to_str(0))

        action_confirmed = custom_inputs.get_yn_confirmation("Proceed? [Y/n]: ")

        if action_confirmed:

            location_printers = location.get_printers()

            for idx in range(len(location_printers)):
                if location_printers[idx].ip == printer.ip:
                    location.get_printers().pop(idx)

            print(
                f"{Style.BRIGHT + Fore.GREEN}✅ Printer removed successfully!\n{Style.RESET_ALL}"
            )

            self.write_dict_as_json()

    def get_printer_by_ip(self, ip: str) -> Printer:

        for printer in self.get_printers():
            if printer.ip == ip:
                return printer

        return

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

    def get_location_by_name(self, name: str) -> tuple[int, Location]:
        for idx, location in enumerate(self.__locations):

            if location.name == name:
                return idx, location

        return None, None

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

    def __read_json(self, path: str) -> dict:

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

        printers_locations_json = self.__read_json(self.__filename)

        for location_name in printers_locations_json.keys():

            location = self.create_location(location_name, output=output, save=False)

            for printer in printers_locations_json[location_name]:
                new_printer = Printer.from_dict(printer)

                location.add_printer(new_printer)

    def create_backup(self, manual: bool = False, backup_path: str = None):

        if manual:
            backup_path = custom_inputs.get_generic_input(
                f"{Style.BRIGHT + Fore.CYAN}[Optional]{Style.RESET_ALL} Enter path or filename: "
            )

            if os.path.exists(backup_path):

                action_confirmed = custom_inputs.get_yn_confirmation(
                    f"{Style.BRIGHT + Fore.YELLOW}File already exists! Proceed? [Y/n]: "
                )

                if not action_confirmed:

                    print(
                        f"{Style.BRIGHT + Fore.YELLOW}⚠️  Backup creation canceled!\n{Style.RESET_ALL}"
                    )
                    return

        if not backup_path:
            backup_path = self.__backup_file

        if os.path.isdir(backup_path):
            backup_path = os.path.join(backup_path, self.__backup_file)

        shutil.copy2(self.__filename, backup_path)

        print(
            f"{Style.BRIGHT + Fore.GREEN}✅ {"[Auto]" if not manual else ""}{Fore.RESET} Backup created successfully!\n{Style.RESET_ALL}"
        )

    def restore_from_backup(self):

        backup_path = custom_inputs.get_generic_input(
            f"{Style.BRIGHT + Fore.CYAN}[Optional]{Style.RESET_ALL} Enter path or filename: "
        )

        if not backup_path:
            backup_path = self.__backup_file

        action_confirmed = custom_inputs.get_yn_confirmation(
            f"{Style.BRIGHT + Fore.YELLOW}⚠️  Current storage file will be overwritten!{Fore.RESET} Proceed? [Y/n]:{Style.RESET_ALL} "
        )

        if action_confirmed:

            shutil.copy2(backup_path, self.__filename)
            self.load_from_json()
            print(
                f"{Style.BRIGHT + Fore.GREEN}✅ Successfully restored from backup!\n{Style.RESET_ALL}"
            )

            return

        print(
            f"{Style.BRIGHT + Fore.YELLOW}⚠️  Backup restoration canceled!\n{Style.RESET_ALL}"
        )

    def write_dict_as_json(self, path: str = ""):

        file = os.path.join(path, self.__filename)

        data = self.to_dict()

        self.create_backup()

        with open(file, "w") as drucker_file:
            json.dump(data, drucker_file, indent=4)
