# Währungskonverter-Webanwendung

Dies ist eine einfache Webanwendung, die es ermöglicht, 
Währungen in Schweizer Franken (CHF) umzurechnen. Das Projekt besteht aus einem Flask-basierten Webserver, 
der Währungskursdaten von externen APIs abruft und dem Benutzer die Möglichkeit bietet, 
Beträge von einer Ausgangswährung in eine Zielwährung umzurechnen.

## Voraussetzungen

Um dieses Projekt auszuführen, benötigen Sie Python 3.x, Flask und eine Internetverbindung, um Währungskursdaten 
von externen APIs abzurufen.

## Installation

1. Klone dieses Repository auf deinen lokalen Computer: git clone https://github.com/rei9050/m122_lb2_wechselkurs.git


2. Wechsel in das Verzeichnis des Projekts: cd m122_lb2_wechselkurs


3. Installiere die erforderlichen Python-Pakete: pip install -r requirements.txt


## Verwendung

1. Starte den Webserver: python app.py

2. Öffne einen Webbrowser und gehe zu http://localhost:5000.

3. Gib den Betrag, die Ausgangswährung und die Zielwährung ein und klicke auf "Umrechnen".

4. Das Ergebnis der Umrechnung wird angezeigt.

## Konfiguration

Die Konfiguration erfolgt über die `config.py`-Datei. Hier müssen Sie Ihre API-Schlüssel für die Währungskurs-APIs angeben.

### Verfügbare APIs und API-Schlüssel

Sie müssen zwei APIs verwenden, um Währungskursdaten abzurufen:

- **Exchange Rate API:** [Exchange Rate API](https://exchangerate-api.com/)
  Um einen API-Schlüssel zu erhalten, registrieren Sie sich auf der Website 
- und folgen Sie den Anweisungen zur Generierung eines API-Schlüssels.
  Fügen Sie den erhaltenen API-Schlüssel der `config.py`-Datei hinzu.

- **Free Currency API:** [Free Currency API](https://app.freecurrencyapi.com/dashboard)
  Um einen API-Schlüssel zu erhalten, registrieren Sie sich auf der Website 
- und folgen Sie den Anweisungen zur Generierung eines API-Schlüssels.
  Fügen Sie den erhaltenen API-Schlüssel ebenfalls der `config.py`-Datei hinzu.

## Sicherheit

Die API-Schlüssel werden in der `config.py`-Datei gespeichert,
die nicht in das öffentliche Repository hochgeladen werden sollte. 
Stellen Sie sicher, dass Sie Ihre API-Schlüssel sicher aufbewahren und nicht öffentlich zugänglich machen.
