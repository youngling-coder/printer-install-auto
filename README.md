Hier ist deine aktualisierte **Dokumentation** für das Druckerverwaltungssystem — **komplett ohne Web-Oberfläche** und mit klarer Beschreibung der **CLI-Kommandos inklusive `overview`-Tabelle** via `prettytable` und `colorama`.

---

# 🖨️ Druckerverwaltungssystem – Dokumentation

## 📌 Einführung

Dieses Python-basierte System dient zur Verwaltung von Druckern an verschiedenen Standorten über eine **Kommandozeilenoberfläche (CLI)**. Es unterstützt:

* Druckerübersicht mit Status (verfügbar/nicht erreichbar)
* Druckerinstallation inkl. Treiberanbindung
* JSON-basierte Datenspeicherung
* Automatische & manuelle Backups

---

## ⚙️ Voraussetzungen

* Python **3.10+**
* Abhängigkeiten installieren:

  ```bash
  pip install -r requirements.txt
  ```

---

## 🧰 Hauptfunktionen

### 1. Standortverwaltung

* 🏢 **Standort hinzufügen**
  → per Befehl `create-location`

* ❌ **Standort entfernen**
  → nur möglich, wenn der Standort **leer** ist
  → per Befehl `remove-location`

---

### 2. Druckerverwaltung

* ➕ **Drucker hinzufügen**
  → mit IP, Name, Modell, Treibername & Treiberpfad (`.inf`)

* ➖ **Drucker entfernen**
  → über IP & Standortname

---

### 3. Druckerinstallation

Führt automatisch folgende Schritte aus:

1. TCP/IP-Port einrichten
2. Treiber installieren
3. Drucker anlegen

---

### 4. Backups & Wiederherstellung

* 💾 Automatische Backups bei Änderungen
* 🔄 Wiederherstellung via `restore`
* 📦 Manuelle Sicherung mit `backup`

---

## 🖥️ CLI-Bedienung

```bash
python main.py <command> [Argumente]
```

---

### 📜 Verfügbare Kommandos

#### 1. `overview`

Zeigt eine Tabelle aller Standorte & Drucker inkl. Verfügbarkeitsstatus (Ping).

```bash
python main.py overview
```

Optional kannst du nur einen Standort anzeigen:

```bash
python main.py overview --location "Büro EG"
```

---

#### 2. `add`

Fügt einen neuen Drucker hinzu.

```bash
python main.py add <location-name> <ip> <name> <model> <driver_name> <driver_inf_path>
```

| Argument          | Beschreibung            |
| ----------------- | ----------------------- |
| `location-name`   | Zielstandort            |
| `ip`              | IP-Adresse des Druckers |
| `name`            | Anzeigename             |
| `model`           | Modellbezeichnung       |
| `driver_name`     | Name des Treibers       |
| `driver_inf_path` | Pfad zur `.inf`-Datei   |

---

#### 3. `remove`

Entfernt einen Drucker anhand IP & Standort.

```bash
python main.py remove <ip> <location-name>
```

---

#### 4. `install`

Installiert einen Drucker anhand seiner IP.

```bash
python main.py install <ip>
```

---

#### 5. `create-location`

Erstellt einen neuen Standort.

```bash
python main.py create-location <location-name>
```

---

#### 6. `remove-location`

Löscht einen Standort (nur wenn leer).

```bash
python main.py remove-location <location-name>
```

---

#### 7. `restore`

Stellt das letzte Backup wieder her.

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

## 📊 Übersichtstabelle (Beispiel: `overview`-Kommando)

Ausgabe mit `colorama` + `prettytable`:

```
Standort 1: Büro EG

+---+-------------+-------------+--------------+---------------------+------------+
| # | Name        | IP          | Modell       | Treiber             | Verfügbar  |
+---+-------------+-------------+--------------+---------------------+------------+
| 1 | HP LaserJet | 10.0.0.5    | HP LJ P1102  | HPUniversalDriver   | ✅ Ja      |
| 2 | Canon Pixma | 10.0.0.7    | Canon MX920  | CanonDriverX        | ❌ Nein    |
+---+-------------+-------------+--------------+---------------------+------------+
```

---

## ⌨️ Tastaturbefehle (nur im interaktiven Modus)

| Eingabe | Funktion                       |
| ------- | ------------------------------ |
| `exit`  | Programm beenden               |
| `ENTER` | Weiter / Bestätigen            |
| `Y/n`   | Ja-/Nein-Auswahl (Default: Ja) |

---

## 💾 Datenstruktur (`printers.json`)

```json
{
  "Büro EG": [
    {
      "ip": "10.97.207.86",
      "name": "Canon123",
      "driver_inf_path": "C:/Treiber/canon.inf",
      "driver_name": "CanonUFRII",
      "model": "Canon MF123"
    }
  ]
}
```

---

## 🔐 Sicherheitshinweise

* IP-Adressen müssen eindeutig sein
* Treiberpfad (`.inf`) muss gültig & zugreifbar sein
* Standorte dürfen nur gelöscht werden, wenn sie **leer** sind
* Backups erfolgen automatisch bei jeder Änderung

---

## ⚠️ Fehlerbehandlung

* ❌ Ungültige IPs werden abgefangen
* 🔁 Ungültige Eingaben im Menü werden erneut abgefragt
* Farbliche Ausgaben:

  * ❌ = Fehler
  * ⚠️ = Warnung

---

## 🚀 Startanleitung

1. Abhängigkeiten installieren:

   ```bash
   pip install -r requirements.txt
   ```

2. CLI starten:

   ```bash
   python main.py
   ```

3. Exe erzeugen (optional):

   ```bash
   pyinstaller --onefile main.py --name druckautoinstall.exe
   ```

---

**👤 Autor:** Dmytro Shyrokov

---

Wenn du willst, exportiere ich diese Doku auch als `.md`, `.pdf` oder füge sie in dein Projekt ein (`README.md`). Sag einfach Bescheid!
