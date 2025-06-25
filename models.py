import socket
from colorama import Fore, Style
from prettytable import PrettyTable

class Location:
    def __init__(self, name: str):
        self.name = name
        self.__printers: list["Printer"] = []

    def get_printer_by_idndex(self, printer_idx: int) -> "Printer":

        if self.__printers:
            return self.__printers[printer_idx]

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

    def to_str(self, idx: int) -> str:
        return f"{Style.BRIGHT}{idx+1}. {self.name}{Style.RESET_ALL}"
    
    def overview(self):
        printers = self.get_printers()

        table = Fore.LIGHTBLACK_EX + "  (Keine Drucker vorhanden)" + Style.RESET_ALL

        if printers:
            table = PrettyTable()
            table.field_names = ["#", "Name", "IP", "Modell", "Treiber", "Verfügbar"]
            for p_idx, printer in enumerate(printers):
                percent = (p_idx + 1) / len(printers)
                filled = int(20 * percent)
                print(
                    f"\r{Style.BRIGHT + Fore.CYAN}[ Availability check... ] {Fore.RESET}|{"█" * filled}{" " * (20 - filled)}| {(percent * 100):.2f}%{Style.RESET_ALL}",
                    end="",
                    flush=True,
                )
                status = printer.is_available()

                status_icon = (
                    Fore.GREEN + "✅ Ja" + Style.RESET_ALL
                    if status
                    else Fore.RED + "❌ Nein" + Style.RESET_ALL
                )

                table.add_row(
                    [
                        p_idx + 1,
                        printer.name,
                        printer.ip,
                        printer.model,
                        printer.driver_name,
                        status_icon,
                    ]
                )

        print(f"\n{table}")


class Printer:
    def __init__(
        self, ip: str, name: str, driver_inf_path: str, driver_name: str, model: str
    ):
        self.ip = ip
        self.name = name
        self.driver_inf_path = driver_inf_path
        self.driver_name = driver_name
        self.model = model

    def is_available(self, port: int = 80, timeout: float = 1.0) -> bool:
        try:
            with socket.create_connection((self.ip, port), timeout=timeout):
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False

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

    def to_str(self, idx: int) -> str:

        table = PrettyTable()
        table.field_names = ["#", "Name", "IP", "Modell", "Treiber", "Verfügbar"]


        status = self.is_available()

        status_icon = (
            Fore.GREEN + "✅ Ja" + Style.RESET_ALL
            if status
            else Fore.RED + "❌ Nein" + Style.RESET_ALL
        )

        table.add_row(
            [
                idx+1,
                self.name,
                self.ip,
                self.model,
                self.driver_name,
                status_icon,
            ]
        )

        return str(table)