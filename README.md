# Druckerverwaltungssystem - Dokumentation

## Einführung
Dieses Python-basiertes System verwaltet Drucker in verschiedenen Standorten. Es bietet:
- Kommandozeilenoberfläche (CLI) für Verwaltung
- Web-Oberfläche zur Übersicht (http://localhost:8765)
- Automatisierte Druckerinstallation
- JSON-basierte Datenspeicherung

### Voraussetzungen
- Python 3.10+
- Abhängigkeiten: `pip install -r requirements.txt`

## Hauptfunktionen

### 1. Standortverwaltung
- **Standort hinzufügen**:  
  `Create a location` im Hauptmenü
- **Standort entfernen**:  
  Voraussetzung: Keine Drucker im Standort  
  `Remove a location` im Hauptmenü

### 2. Druckerverwaltung
- **Drucker hinzufügen**:  
  Erfordert IP, Name, Modell, Treiberpfad
- **Drucker entfernen**:  
  `Remove a printer by place and IP` im Menü

### 3. Druckerinstallation
- Führt drei Schritte aus:
  1. TCP/IP-Port erstellen
  2. Treiber installieren
  3. Drucker im System einrichten

### 4. Datenpersistenz
- Automatische Backups bei Änderungen
- Manuelle Backup-Wiederherstellung möglich

### 5. Web-Oberfläche
- Startet automatisch mit Hauptprogramm
- Zeigt pro Standort:
  - Drucker-IPs und Namen
  - Treiberinformationen
  - Verfügbarkeit (✅/❌ via Ping)
- Erreichbar unter: http://localhost:8765

## Bedienungshandbuch

### Hauptmenü-Optionen:
1. **Printer overview**  
   Zeigt alle Standorte und Drucker
2. **Add a printer**  
   Fügt neuen Drucker hinzu (erfordert alle Daten)
3. **Remove a printer**  
   Entfernt Drucker aus Standort
4. **Install a printer**  
   Startet Installationsroutine
5. **Create a location**  
   Erstellt neuen Standort
6. **Remove a location**  
   Löscht leeren Standort
7. **Restore from backup**  
   Stellt Backup wieder her
8. **Create backup**  
   Manuelles Backup erstellen

### Tastaturbefehle:
- `exit`: Programm beenden
- `ENTER`: Bestätigen/Weiter
- `Y/n`: Ja/Nein-Antworten (Ja als Standardauswahl)

## Datenmodell (printers.json)
```json
{
  "Standortname": [
    {
      "ip": "10.97.207.86",
      "name": "Druckername",
      "driver_inf_path": "/pfad/zur/datei.inf",
      "driver_name": "Treibername",
      "model": "Druckermodell"
    }
  ]
}
```

### Sicherheitshinweise
- IP-Adressen müssen eindeutig sein
- Treiber-Pfade müssen valide sein
- Standorte müssen leer sein zum Löschen
- Backups werden automatisch erstellt

### Fehlerbehandlung
- Ungültige IPs werden abgefangen
- Falsche Menüeingaben werden erneut abgefragt
- Fehlermeldungen in Rot mit Symbolen:
  - ❌: Kritischer Fehler
  - ⚠️: Warnung

### Startanleitung
1. Abhängigkeiten installieren:
   `pip install -r requirements.txt`
2. Hauptprogramm starten:
   `python main.py`
3. Build-Prozess:
   `pyinstaller --onefile main.py --name druckautoinstall.exe`
4. Webinterface öffnen:
   http://localhost:8765

**Autor:** Dmytro Shyrokov 