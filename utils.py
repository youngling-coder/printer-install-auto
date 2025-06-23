from colorama import Style, Fore


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


def prettified_locations_output(locations: list) -> str:

    locations = [location.to_str(idx) for idx, location in enumerate(locations)]

    return f"{"\n".join(locations)}\n"
