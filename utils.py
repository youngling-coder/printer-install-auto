from colorama import Style, Fore
from storage import Storage

# Liste aller möglichen Aktionen, die der Benutzer im interaktiven Modus auswählen kann.
actions = [
    "Druckerübersicht anzeigen",
    "Einen Drucker hinzufügen",
    "Einen Drucker entfernen",
    "Einen Drucker installieren",
    "Einen neuen Standort erstellen",
    "Einen Standort entfernen",
    "Aus Backup wiederherstellen",
    "Create Backup erstellen",
]

# Anzahl aller Aktionen (wird für Bereichsprüfung verwendet)
total_actions_count = len(actions)


def help_() -> None:
    """
    Gibt dem Benutzer eine Liste aller verfügbaren Aktionen aus.
    """
    print(f'Geben Sie {Style.BRIGHT}"exit"{Style.RESET_ALL} ein, um das Programm zu beenden\n')

    for idx, action in enumerate(actions):
        print(f"{idx+1}. {action}")

    print()


def get_storage() -> Storage:
    """
    Erstellt eine Storage-Instanz und lädt darin die JSON-Daten.
    Gibt die geladene Instanz zurück.
    """
    s = Storage()
    s.load_from_json(output=False)
    return s


def print_error(msg: str) -> None:
    """
    Gibt eine formatiere Fehlermeldung aus.
    """
    print(f"{Style.BRIGHT + Fore.RED}❌ {msg} {Style.RESET_ALL}")


def handle_location_check(storage: Storage, name: str) -> tuple[int, "Location"]:
    """
    Prüft, ob ein Standort mit dem gegebenen Namen existiert.
    Gibt (Index, Standort) zurück. Gibt Fehler aus, wenn nicht vorhanden.
    """
    idx, loc = storage.get_location_by_name(name)
    if not loc:
        print_error("Standort nicht gefunden!")
    return idx, loc


def handle_printer_check(storage: Storage, ip: str) -> "Printer":
    """
    Sucht einen Drucker anhand seiner IP im Storage.
    Gibt Fehler aus, wenn kein Drucker mit dieser IP existiert.
    """
    printer = storage.get_printer_by_ip(ip)
    if not printer:
        print_error("Drucker nicht gefunden!")
    return printer


def prettified_locations_output(locations: list) -> str:
    """
    Gibt eine formatierte, durchnummerierte Übersicht über alle Standorte zurück.
    """
    locations = [location.to_str(idx) for idx, location in enumerate(locations)]
    return f"{"\n".join(locations)}\n"
