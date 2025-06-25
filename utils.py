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

    print(f"{Fore.CYAN + Style.BRIGHT}Commands: {Style.RESET_ALL}\n")

    for idx, action in enumerate(actions):
        print(f"{idx+1}  ::  {action}")

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


def show_overview_of_location(location):
    printers = location.get_printers()

    if not printers:
        print(Fore.LIGHTBLACK_EX + "  (Keine Drucker vorhanden)" + Style.RESET_ALL)
        return

    table = PrettyTable()
    table.field_names = ["#", "Name", "IP", "Modell", "Treiber", "Verfügbar"]

    for p_idx, printer in enumerate(printers):
        percent = (p_idx + 1) / len(printers)
        filled = int(20 * percent)
        print(
            f"\r{Style.BRIGHT + Fore.CYAN}[Availability check... ] {Fore.RESET}|{"█" * filled}{" " * (20 - filled)}| {(percent * 100):.2f}%{Style.RESET_ALL}",
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

    print()
    print(table)


def show_overview_of_storage(storage):
    locations = storage.get_locations()

    if not locations:
        print(Fore.YELLOW + "Keine Standorte vorhanden." + Style.RESET_ALL)
        return

    for l_idx, location in enumerate(locations):
        print(
            f"{"\n" if l_idx else ""}{Style.BRIGHT}Standort {l_idx+1}: {location.name}{Style.RESET_ALL}"
        )

        show_overview_of_location(location)


def prettified_locations_output(locations: list) -> str:

    locations = [location.to_str(idx) for idx, location in enumerate(locations)]

    return f"{"\n".join(locations)}\n"
