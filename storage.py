import os
import json
import re
from typing import Optional
import shutil

from colorama import Style, Fore

from utils import prettified_printer_output
import custom_inputs


class Storage:
    def __init__(self):
        self.__locations: list["Location"] = []

    def add_printer_to_location(self, printer: "Printer", location: "Location") -> None:

        print()
        print(prettified_printer_output(0, printer))
        print(
            f'{Style.BRIGHT}Will be added to "{Fore.CYAN + location.name.capitalize() + Fore.RESET}"'
        )

        check_data = custom_inputs.get_yn_confirmation("Proceed? [Y/n]: ")

        if check_data:
            location.add_printer(printer)
            self.write_dict_as_json()

            print(
                f"{Style.BRIGHT + Fore.GREEN}\n✅ Printer added successfully!{Style.RESET_ALL}"
            )

    def remove_printer_from_location(
        self, printer: "Printer", location: "Location"
    ) -> None:

        print(
            f"\n{Fore.YELLOW + Style.BRIGHT}⚠️ All the info about this printer will be removed!\n"
        )
        print(prettified_printer_output(0, printer))

        confirm_deletion = custom_inputs.get_yn_confirmation("\nProceed? [Y/n]: ")

        if confirm_deletion:

            location_printers = location.get_printers()

            for idx in range(len(location_printers)):
                if location_printers[idx].ip == printer.ip:
                    location.get_printers().pop(idx)

            self.write_dict_as_json()
            print(
                f"{Style.BRIGHT + Fore.GREEN}\n✅ Printer removed successfully!{Style.RESET_ALL}"
            )

    def get_location_by_id(self, location_id: int) -> "Location":
        return self.__locations[location_id]

    def is_ip_unique(self, ip):
        for printer in self.get_printers():

            if printer.ip == ip:
                return False

        return True

    def is_ip_valid(self, ip: str):

        ip_regex = re.compile(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$")

        return bool(ip_regex.match(ip) and self.is_ip_unique(ip))

    def get_location_by_name(self, name: str) -> Optional["Location"]:
        for location in self.__locations:

            if location.name == name:
                return location

        return

    def add_location(self, name: str) -> "Location":
        self.__locations.append(Location(name))

        return self.__locations[-1]

    def to_dict(self) -> dict:

        json = {}

        for location in self.__locations:
            json[location.name] = location.get_printers(as_dicts=True)

        return json

    def get_locations(self) -> list["Location"]:
        return self.__locations

    def get_printers(self, as_dicts: bool = False) -> list["Printer"]:

        printers = []

        for location in self.__locations:
            printers.extend(location.get_printers(as_dicts))

        return printers

    def __read_json(self, path: str = "printers.json"):

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"{Style.BRIGHT + Fore.RED}JSON file not found!{Style.RESET_ALL}"
            )

        druckers = {}

        with open(path, "r") as drucker_file:
            druckers = json.load(drucker_file)

        return druckers

    def load_from_json(self):

        printers_locations_json = self.__read_json()

        for location_name in printers_locations_json.keys():
            location = self.add_location(location_name)

            for printer in printers_locations_json[location_name]:
                new_printer = Printer.from_dict(printer)

                location.add_printer(new_printer)

    def __backup_current_state(self, path: str = "printers.json"):
        backup_path = path + ".bak"
        shutil.copy2(path, backup_path)

    def write_dict_as_json(self, path: str = "printers.json"):

        data = self.to_dict()

        self.__backup_current_state()

        with open(path, "w") as drucker_file:
            json.dump(data, drucker_file, indent=4)


class Location:
    def __init__(self, name: str):
        self.name = name
        self.__printers: list["Printer"] = []

    def get_printer_by_id(self, printer_id: int) -> "Printer":
        return self.__printers[printer_id]

    def get_printers(self, as_dicts: bool = False) -> list["Printer"]:

        printers = []

        if as_dicts:

            for printer in self.__printers:
                printers.append(printer.to_dict())

            return printers

        return self.__printers

    def __is_printer_unique(self, target: "Printer"):

        for printer in self.__printers:
            if target.ip == printer.ip:
                return False

        return True

    def add_printer(self, printer: "Printer"):

        if self.__is_printer_unique(printer):
            self.__printers.append(printer)


class Printer:
    def __init__(
        self, ip: str, name: str, driver_inf_path: str, driver_name: str, model: str
    ):
        self.ip = ip
        self.name = name
        self.driver_inf_path = driver_inf_path
        self.driver_name = driver_name
        self.model = model

    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict) -> "Printer":
        return cls(
            ip=data["ip"],
            name=data["name"],
            driver_inf_path=data["driver_inf_path"],
            driver_name=data["driver_name"],
            model=data["model"],
        )
