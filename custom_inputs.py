from typing import Optional
from colorama import Style, Fore
import utils
import sys
from models import Printer, Location


def get_generic_input(prompt: str, empty: bool = True) -> str:
    """
    Fragt eine generische Benutzereingabe ab.
    Beendet das Programm, wenn 'exit' eingegeben wird.
    Bei empty=False werden leere Eingaben wiederholt.
    """
    while True:
        value = input(prompt)
        print()

        if value.lower() == "exit":
            sys.exit(0)

        if not empty and not value.strip():
            continue

        return value


def get_yn_confirmation(prompt: str) -> bool:
    """
    Fragt eine Ja/Nein-Bestätigung ab.
    Rückgabe ist True bei Eingabe mit 'y' beginnend oder leerer Eingabe.
    """
    confirmation = get_generic_input(Style.BRIGHT + prompt + Style.RESET_ALL)
    return confirmation.lower().startswith("y") or confirmation == ""


def get_ip_input(storage) -> str:
    """
    Fordert die Eingabe einer IP-Adresse vom Benutzer an
    und überprüft deren Gültigkeit mithilfe des Storage-Objekts.
    """
    while True:
        try:
            value = get_generic_input("IP-Addresse des Druckers eingeben: ")

            if not storage.is_ip_valid(value):
                raise ValueError(
                    f"{Style.BRIGHT + Fore.RED}Ungültiger Wert!\n{Style.RESET_ALL}"
                )

            return value

        except ValueError as e:
            print(e)


def get_integer_input(
    prompt: str, range_: Optional[range] = None, optional: bool = False
) -> int:
    """
    Fragt eine Ganzzahl vom Benutzer ab.
    Optional kann ein gültiger Wertebereich angegeben werden.
    """
    while True:
        try:
            value = int(get_generic_input(prompt, optional))

            if range_ and (value not in range_):
                raise IndexError("Wert liegt außerhalb des gültigen Bereichs!\n")

            return value

        except ValueError:
            if optional:
                return ""

            utils.print_error("Ungültiger Wert!\n")

        except IndexError as e:
            utils.print_error(e)


def get_printer_index_input(location: Location) -> int:
    """
    Zeigt Übersicht der Drucker in einem Standort an
    und fragt den Index eines Druckers vom Benutzer ab.
    """
    location.overview()

    printer_id = get_integer_input(
        "Drucker auswählen: ", range_=range(1, len(location.get_printers()) + 1)
    )

    return printer_id - 1


def get_location_index_input(locations: list[Location], optional: bool = False) -> int:
    """
    Zeigt alle Standorte an und fragt den Index eines Standorts vom Benutzer ab.
    """
    print(utils.prettified_locations_output(locations))

    location_id = get_integer_input(
        "Nummer des Standorts eingeben: ",
        range_=range(1, len(locations) + 1),
        optional=optional,
    )

    if optional and not location_id:
        return

    return location_id - 1


def get_current_action() -> int:
    """
    Zeigt verfügbaren Aktionen an und fragt gewünschte Aktion vom Benutzer ab.
    """
    utils.help_()

    current_action = get_integer_input(
        "Wählen Sie die gewünschte Aktion: ",
        range_=range(1, utils.total_actions_count + 1),
    )

    return current_action


def input_printer_data(storage) -> tuple[Printer, Location]:
    """
    Fragt vom Benutzer alle Daten für einen neuen Drucker ab.
    Gibt ein Printer-Objekt und den zugehörigen Standort zurück.
    """
    location = storage.get_location_by_index(
        get_location_index_input(storage.get_locations())
    )
    new_printer = {}

    new_printer["ip"] = get_ip_input(storage)
    new_printer["name"] = get_generic_input("Enter printer's name: ", empty=False)
    new_printer["model"] = get_generic_input("Enter printer's model: ", empty=False)

    action_confirmed = False
    for printer in storage.get_printers():
        if printer.model.lower() == new_printer["model"].lower():
            new_printer["driver_name"] = printer.driver_name
            new_printer["driver_inf_path"] = printer.driver_inf_path
            action_confirmed = get_yn_confirmation(
                "Ein Drucker dieses Modells existiert bereits! Möchten Sie die Treibereinstellungen übernehmen? [Y/n]: "
            )
            break

    if not action_confirmed:
        new_printer["driver_name"] = get_generic_input(
            "Name des Druckertreibers eingeben: ", empty=False
        )
        new_printer["driver_inf_path"] = get_generic_input(
            "Pfad des Druckertreibers eingeben: ", empty=False
        )

    printer = Printer.from_dict(new_printer)

    return printer, location


def select_printer_data(storage) -> tuple[Printer, Location]:
    """
    Lässt den Benutzer einen Standort und Drucker auswählen.
    Gibt das ausgewählte Printer-Objekt und den zugehörigen Standort zurück.
    """
    location_idx = get_location_index_input(storage.get_locations())
    location = storage.get_location_by_index(location_idx)

    printer_idx = get_printer_index_input(location)
    printer = location.get_printer_by_idndex(printer_idx)

    return printer, location
