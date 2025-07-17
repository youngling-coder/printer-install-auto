import os
import sys
from colorama import Style, Fore
from argparser import build_arg_parser

from custom_inputs import (
    get_current_action,
    input_printer_data,
    select_printer_data,
    get_location_index_input,
    get_generic_input,
)
from installer import Installer
from models import Printer
import utils


def cli_main(args):
    # Holt das aktuelle Speicherobjekt (z. B. Drucker- und Standortdaten)
    storage = utils.get_storage()

    # Führt Aktionen basierend auf dem Kommandozeilenargument `args.action` aus
    match args.action:
        case "overview":
            # Zeigt entweder Übersicht eines bestimmten Standorts oder aller Standorte
            if args.location:
                _, location = utils.handle_location_check(storage, args.location)
                if location:
                    location.overview()
            else:
                storage.overview()

        case "add":
            # Erstellt ein Printer-Objekt aus den Argumenten
            printer = Printer.from_dict(
                {
                    "dns": args.dns,
                    "name": args.name,
                    "driver_inf_path": args.driver_inf_path,
                    "model": args.model,
                    "driver_name": args.driver_name,
                }
            )
            # Prüft und holt den zugehörigen Standort
            _, location = utils.handle_location_check(storage, args.location_name)
            if location:
                # Fügt Drucker dem Standort hinzu
                storage.add_printer_to_location(printer, location)

        case "remove":
            # Holt Drucker- und Standortdaten aus den Argumenten
            printer = utils.handle_printer_check(storage, args.dns)
            _, location = utils.handle_location_check(storage, args.location_name)
            if printer and location:
                # Entfernt Drucker vom Standort
                storage.remove_printer_from_location(printer, location)

        case "install":
            # Holt Drucker anhand der DNS und startet Installation
            printer = utils.handle_printer_check(storage, args.dns)
            if printer:
                Installer(printer).run()

        case "create-location":
            # Erstellt neuen Standort mit Bestätigung
            storage.create_location(args.location_name, confirm=True)

        case "remove-location":
            # Entfernt bestehenden Standort, wenn Index gefunden
            idx, _ = utils.handle_location_check(storage, args.location_name)
            if idx is not None:
                storage.remove_location(idx)

        case "restore":
            # Stellt Daten aus Backup wieder her
            storage.restore_from_backup()

        case "backup":
            # Erstellt Backup der aktuellen Daten
            storage.create_backup()


def interactive_main():
    # Löscht die Konsole (nur unter Windows wirksam)
    os.system("cls")

    # Startet interaktives Menü
    while True:
        storage = utils.get_storage()

        # Führt Benutzeraktion basierend auf Auswahl aus
        match get_current_action():
            case 1:
                # Zeigt Übersicht für spezifischen oder alle Standorte
                location_idx = get_location_index_input(storage.get_locations(), True)

                if location_idx is None:
                    storage.overview()
                else:
                    location = storage.get_location_by_index(location_idx)
                    location.overview()

            case 2:
                # Neue Druckerdaten eingeben und zu Standort hinzufügen
                printer, location = input_printer_data(storage)
                storage.add_printer_to_location(printer, location)

            case 3:
                # Drucker auswählen und entfernen
                printer, location = select_printer_data(storage)
                if not printer:
                    utils.print_error("Drucker nicht gefunden!")
                else:
                    storage.remove_printer_from_location(printer, location)

            case 4:
                # Drucker auswählen und Installation ausführen
                printer, _ = select_printer_data(storage)
                Installer(printer).run()

            case 5:
                # Neuen Standort anlegen
                name = get_generic_input(
                    "Name des neuen Standorts eingeben: ", empty=False
                )
                storage.create_location(name, confirm=True)

            case 6:
                # Standort per Index auswählen und entfernen
                idx = get_location_index_input(storage.get_locations())
                storage.remove_location(idx)

            case 7:
                # Backup wiederherstellen
                storage.restore_from_backup()

            case 8:
                # Manuelles Backup erstellen
                storage.create_backup(manual=True)

        print()


if __name__ == "__main__":
    # Entscheidet zwischen CLI- und interaktivem Modus basierend auf Argumentanzahl
    if len(sys.argv) > 1:
        args = build_arg_parser().parse_args()
        cli_main(args)
    else:
        interactive_main()
