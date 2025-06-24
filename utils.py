from colorama import Style, Fore
from prettytable import PrettyTable

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

    print(
        f"{Style.BRIGHT}{Fore.GREEN}🌐 Web Overview: {Fore.CYAN}http://localhost:8765/{Style.RESET_ALL}\n"
    )
    print(f"{Fore.CYAN + Style.BRIGHT}Commands: {Style.RESET_ALL}\n")

    for idx, action in enumerate(actions):
        print(f"{idx+1}  ::  {action}")

    print()


def show_overview_of_location(location):
    printers = location.get_printers()

    if not printers:
        print(Fore.LIGHTBLACK_EX + "  (Keine Drucker vorhanden)\n" + Style.RESET_ALL)
        return

    table = PrettyTable()
    table.field_names = ["#", "Name", "IP", "Modell", "Treiber", "Verfügbar"]

    for p_idx, printer in enumerate(printers):
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
