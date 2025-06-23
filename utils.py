from colorama import Style, Fore


actions = [
    "Add a printer with name, IP, and driver",
    "Remove a printer by place and IP",
    "Install a printer",
    "Create a location",
    "Remove a location",
    "Restore from backup",
]

total_actions_count = len(actions)


def help_():
    print(f"{Fore.CYAN + Style.BRIGHT}Commands: {Style.RESET_ALL}\n")

    for idx, action in enumerate(actions):
        print(f"{idx+1}  ::  {action}")

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

    return f"{Style.BRIGHT}{idx+1}  ::  {location.name}{Style.RESET_ALL}"


def prettified_locations_output(locations: list) -> str:

    locations = [
        prettified_location_output(idx, location)
        for idx, location in enumerate(locations)
    ]

    return f"{"\n".join(locations)}\n"
