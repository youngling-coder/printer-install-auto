from colorama import Style, Fore
from storage import Location, Printer

total_actions_count = 3

def help_():
    print(f"{Fore.CYAN}{Style.BRIGHT}Commands\n")
    
    print(f"1. {Style.RESET_ALL}Add a printer with name, IP, and driver")
    print(f"{Style.BRIGHT}2. {Style.RESET_ALL}Remove a printer by place and IP")
    print(f"{Style.BRIGHT}3. {Style.RESET_ALL}Install a printer\n")


def prettified_printer_output(idx: int, printer: Printer) -> str:

    output = (
        f"{idx+1}. {Style.BRIGHT + Fore.CYAN}{printer.name}\n"
        f"  {Fore.YELLOW}Model  : {Fore.RESET}{printer.model}\n"
        f"  {Fore.YELLOW}IP     : {Fore.RESET}{printer.ip}\n"
        f"  {Fore.YELLOW}Driver name : {Fore.RESET}{printer.driver_name or '—'}\n"
        f"  {Fore.YELLOW}Driver .inf path : {Fore.RESET}{printer.driver_inf_path or '—'}\n"
    )

    return output


def prettified_location_output(idx: int, location: dict) -> str:
     
    return f"{Style.BRIGHT}{idx+1}. {location.capitalize()}{Style.RESET_ALL}"


def prettified_locations_output(locations: list[Location]) -> str:

    locations = [
        prettified_location_output(idx, location.name) for idx, location in enumerate(locations)
    ]

    return f"{"\n".join(locations)}\n"


def get_location_by_ip(ip: str, locations: list[Location]):
    pass