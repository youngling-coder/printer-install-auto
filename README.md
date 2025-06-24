
# 🖨️ Druckerverwaltungssystem – Dokumentation

## 📌 Einführung

Dieses Python-basierte System dient zur Verwaltung von Druckern an verschiedenen Standorten. Es bietet:

* **Kommandozeilen-Interface (CLI)** zur Verwaltung
* **Web-Oberfläche** zur Übersicht unter [http://localhost:8765](http://localhost:8765)
* **Automatisierte Druckerinstallation**
* **JSON-basierte Datenspeicherung und automatische Backups**


## ⚙️ Voraussetzungen

* Python **3.10+**
* Abhängigkeiten installieren via:

  ```bash
  pip install -r requirements.txt
  ```

## 🧰 Hauptfunktionen

### 1. Standortverwaltung

* 🏢 **Standort hinzufügen**
  → Über `Create a location` im Hauptmenü

* ❌ **Standort entfernen**
  → Nur möglich, wenn der Standort **keine Drucker** enthält
  → Über `Remove a location` im Hauptmenü

---

### 2. Druckerverwaltung

* ➕ **Drucker hinzufügen**
  → Erfordert: IP-Adresse, Name, Modell, Treibername & Pfad

* ➖ **Drucker entfernen**
  → Über `Remove a printer by place and IP`

---

### 3. Druckerinstallation

Führt folgende Schritte automatisch aus:

1. Erstellen des TCP/IP-Ports
2. Treiberinstallation (.inf-Datei)
3. Einrichtung im System

---

### 4. Datenpersistenz

* 💾 **Automatische Backups** bei jeder Änderung
* 🔄 **Manuelle Wiederherstellung** über das Menü möglich

---

### 5. Web-Oberfläche

* Startet automatisch beim Programmstart
* Darstellung je Standort:

  * Drucker-IPs & Namen
  * Treiberinformationen
  * Verfügbarkeit (✅ verfügbar / ❌ offline via Ping)
* Aufrufbar unter: [http://localhost:8765](http://localhost:8765)

---

## 🖥️ Bedienungshandbuch (CLI)

```bash
python main.py <command> [Argumente]
```

### 📜 Verfügbare Befehle

#### 1. `overview`

Zeigt Übersicht aller Standorte und Drucker.

```bash
python main.py overview
```

---

#### 2. `add`

Fügt einen neuen Drucker zu einem Standort hinzu.

```bash
python main.py add <location_name> <ip> <name> <model> <driver_name> <driver_inf_path>
```

| Argument          | Beschreibung            |
| ----------------- | ----------------------- |
| `location_name`   | Name des Standorts      |
| `ip`              | IP-Adresse des Druckers |
| `name`            | Anzeigename             |
| `model`           | Modellbezeichnung       |
| `driver_name`     | Name des Treibers       |
| `driver_inf_path` | Pfad zur `.inf`-Datei   |

---

#### 3. `remove`

Entfernt einen Drucker anhand von IP und Standort.

```bash
python main.py remove <ip> <location_name>
```

---

#### 4. `install`

Installiert einen Drucker anhand seiner IP-Adresse.

```bash
python main.py install <ip>
```

---

#### 5. `create-location`

Erstellt einen neuen Standort.

```bash
python main.py create-location <location_name>
```

---

#### 6. `remove-location`

Entfernt einen bestehenden Standort (nur wenn leer).

```bash
python main.py remove-location <location_name>
```

---

#### 7. `restore`

Stellt den letzten Backup-Zustand wieder her.

```bash
python main.py restore
```

---

#### 8. `backup`

Erstellt ein manuelles Backup.

```bash
python main.py backup
```

---

## 🧭 Menüfunktionen im Interaktiven Modus

1. **Printer overview** – Zeigt alle Standorte & Drucker
2. **Add a printer** – Drucker hinzufügen (alle Daten notwendig)
3. **Remove a printer** – Drucker entfernen
4. **Install a printer** – Installationsroutine starten
5. **Create a location** – Neuen Standort anlegen
6. **Remove a location** – Leeren Standort löschen
7. **Restore from backup** – Backup wiederherstellen
8. **Create backup** – Manuelles Backup erstellen

---

## ⌨️ Tastaturbefehle

| Eingabe | Funktion                           |
| ------- | ---------------------------------- |
| `exit`  | Beendet das Programm               |
| `ENTER` | Bestätigt Eingabe / Weiter         |
| `Y/n`   | Ja-/Nein-Auswahl (Ja ist Standard) |

---

## 💾 Datenmodell (`printers.json`)

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

---

## 🔐 Sicherheitshinweise

* IP-Adressen müssen **eindeutig** sein
* `.inf`-Pfad muss **gültig** sein
* Standorte dürfen **nur leer gelöscht** werden
* Backups werden **automatisch** gespeichert

---

## ⚠️ Fehlerbehandlung

* ❌ Ungültige IP-Adressen werden abgefangen
* 🔁 Ungültige Menüeingaben werden erneut abgefragt
* Farbige Fehlerausgaben:

  * ❌ Kritischer Fehler
  * ⚠️ Warnung

---

## 🚀 Startanleitung

1. Abhängigkeiten installieren:

   ```bash
   pip install -r requirements.txt
   ```
2. Hauptprogramm starten:

   ```bash
   python main.py
   ```
3. Exe-Datei erstellen (optional):

   ```bash
   pyinstaller --onefile main.py --name druckautoinstall.exe
   ```
4. Webinterface öffnen:
   [http://localhost:8765](http://localhost:8765)

---

**👤 Autor:** Dmytro Shyrokov

