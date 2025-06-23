import platform
import subprocess
from colorama import Fore, Style


class Location:
    def __init__(self, name: str):
        self.name = name
        self.__printers: list["Printer"] = []

    def get_printer_by_idndex(self, printer_idx: int) -> "Printer":
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


class Printer:
    def __init__(
        self, ip: str, name: str, driver_inf_path: str, driver_name: str, model: str
    ):
        self.ip = ip
        self.name = name
        self.driver_inf_path = driver_inf_path
        self.driver_name = driver_name
        self.model = model

    def is_available(self, timeout: int = 5) -> bool:

        param = "-n" if platform.system().lower() == "windows" else "-c"

        try:
            result = subprocess.run(
                ["ping", param, "1", "-w", str(timeout), self.ip],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return result.returncode == 0
        except Exception:
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

    def to_str(self, idx: int, tab_level: int = 0) -> str:

        output = (
            f"{"  " * tab_level}{idx+1}. {Style.BRIGHT + Fore.CYAN}{self.name}\n"
            f"  {"  " * tab_level}{Fore.YELLOW}Model  : {Fore.RESET}{self.model}\n"
            f"  {"  " * tab_level}{Fore.YELLOW}IP     : {Fore.RESET}{self.ip}\n"
            f"  {"  " * tab_level}{Fore.YELLOW}Driver name : {Fore.RESET}{self.driver_name or '—'}\n"
            f"  {"  " * tab_level}{Fore.YELLOW}Driver .inf path : {Fore.RESET}{self.driver_inf_path or '—'}\n"
        )

        return output
