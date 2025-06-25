from colorama import Style, Fore
from prettytable import PrettyTable
from storage import Storage

actions = [
    "Printer overview",
    "Add a printer with name, IP, and driver",
    "Remove a printer by place and IP",
    "Install a printer",
    "Create a location",
    "Remove a location",
    "Restore from backup",
    "Create backup",
]

total_actions_count = len(actions)


def help_():

    print(f'Type {Style.BRIGHT}"exit"{Style.RESET_ALL} to quit the program\n')

    for idx, action in enumerate(actions):
        print(f"{idx+1}. {action}")

    print()


def get_storage():
    s = Storage()
    s.load_from_json(output=False)
    return s


def print_error(msg):
    print(f"{Style.BRIGHT + Fore.RED}❌ {msg} {Style.RESET_ALL}")


def handle_location_check(storage, name):
    idx, loc = storage.get_location_by_name(name)
    if not loc:
        print_error("Location not found!")
    return idx, loc


def handle_printer_check(storage, ip):
    printer = storage.get_printer_by_ip(ip)
    if not printer:
        print_error("Printer not found!")
    return printer

def prettified_locations_output(locations: list) -> str:

    locations = [location.to_str(idx) for idx, location in enumerate(locations)]

    return f"{"\n".join(locations)}\n"
