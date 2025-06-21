from colorama import Style, Fore


total_actions_count = 5


actions = {
    1: "Add a printer with name, IP, and driver",
    2: "Remove a printer by place and IP",
    3: "Install a printer",
    4: "Add a location",
    5: "Remove a location",
    6: "Restore last state",
}


def help_():
    print(f"{Fore.CYAN + Style.BRIGHT}Commands {Style.RESET_ALL}\n")

    for idx, action in actions.items():

        print(f"{idx}. {action}")

    print()


def prettified_printer_output(idx: int, printer) -> str:

    output = (
        f"{idx+1}. {Style.BRIGHT + Fore.CYAN}{printer.name}\n"
        f"  {Fore.YELLOW}Model  : {Fore.RESET}{printer.model}\n"
        f"  {Fore.YELLOW}IP     : {Fore.RESET}{printer.ip}\n"
        f"  {Fore.YELLOW}Driver name : {Fore.RESET}{printer.driver_name or '—'}\n"
        f"  {Fore.YELLOW}Driver .inf path : {Fore.RESET}{printer.driver_inf_path or '—'}\n"
    )

    return output


def prettified_location_output(idx: int, location) -> str:

    return f"{Style.BRIGHT}{idx+1}. {location.capitalize()}{Style.RESET_ALL}"


def prettified_locations_output(locations: list) -> str:

    locations = [
        prettified_location_output(idx, location.name)
        for idx, location in enumerate(locations)
    ]

    return f"{"\n".join(locations)}\n"
