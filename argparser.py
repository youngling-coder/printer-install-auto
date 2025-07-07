import argparse


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Erstellt und konfiguriert den Argumentparser für die Kommandozeilensteuerung.
    Gibt den konfigurierten Parser zurück.
    """

    # Basisparser mit Beschreibung
    parser = argparse.ArgumentParser(description="Druckerverwaltung über CLI")

    # Subparser für Aktionen (z. B. add, remove, install)
    subparsers = parser.add_subparsers(dest="action", help="Aktionen")
    subparsers.required = True  # Aktion ist Pflicht

    # Übersicht anzeigen, optional mit Standortfilter
    overview = subparsers.add_parser("overview", help="Druckerübersicht anzeigen")
    overview.add_argument("--location", required=False)

    # Drucker hinzufügen
    add = subparsers.add_parser("add", help="Einen Drucker hinzufügen")
    add.add_argument("location_name")
    add.add_argument("ip")
    add.add_argument("name")
    add.add_argument("model")
    add.add_argument("driver_name")
    add.add_argument("driver_inf_path")

    # Drucker entfernen (per IP und Standort)
    rem = subparsers.add_parser("remove", help="Einen Drucker entfernen")
    rem.add_argument("ip")
    rem.add_argument("location_name")

    # Drucker installieren
    install = subparsers.add_parser("install", help="Einen Drucker installieren")
    install.add_argument("ip")

    # Standort erstellen
    create_loc = subparsers.add_parser(
        "create-location", help="Einen neuen Standort erstellen"
    )
    create_loc.add_argument("location_name")

    # Standort entfernen
    remove_loc = subparsers.add_parser(
        "remove-location", help="Einen Standort entfernen"
    )
    remove_loc.add_argument("location_name")

    # Backup wiederherstellen
    subparsers.add_parser("restore", help="Aus Backup wiederherstellen")

    # Backup erstellen
    subparsers.add_parser("backup", help="Backup erstellen")

    return parser
