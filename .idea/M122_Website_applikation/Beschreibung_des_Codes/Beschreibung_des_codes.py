from flask import Flask, render_template, request  # Importieren der benötigten Flask-Module
import requests  # Importieren der requests-Bibliothek zum Senden von HTTP-Anfragen
import logging  # Importieren des logging-Moduls zum Protokollieren von Aktivitäten
import config  # Importieren der Konfigurationsdatei

app = Flask(__name__)  # Initialisierung der Flask-App

# Konfiguration des Loggers
logging.basicConfig(filename='../currency_converter.log', level=logging.INFO)

# Funktion zum Abrufen der Wechselkurse von der API nur für CHF
def get_exchange_rates(api_key):
    # URL zur API für Wechselkurse von CHF
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/CHF"

    try:
        # Senden einer GET-Anfrage an die API
        response = requests.get(url)
        response.raise_for_status()  # Werfen einer Ausnahme bei einem HTTP-Fehlerstatuscode
        data = response.json()  # Konvertieren der API-Antwort in JSON
        return data.get("conversion_rates")  # Rückgabe der Umrechnungskurse
    except requests.RequestException as e:
        # Protokollieren einer Warnung bei einem Fehler beim Abrufen der Wechselkurse
        error_message = f"Fehler beim Abrufen der Wechselkurse von der API: {str(e)}"
        logging.warning(error_message)
        return None  # Rückgabe von None im Fehlerfall

# Funktion zur Währungsumrechnung
def convert_currency(amount, from_currency, to_currency, exchange_rates):
    if from_currency == to_currency:
        # Überprüfung, ob Ausgangs- und Zielwährung identisch sind
        error_message = "Die Ausgangs- und Zielwährungen sind identisch."
        logging.warning(error_message)
        return None  # Rückgabe von None, wenn Ausgangs- und Zielwährung identisch sind

    if from_currency not in exchange_rates or to_currency not in exchange_rates:
        # Überprüfung, ob die Währungen gültig sind
        error_message = f"Ungültige Währung(en) verwendet: von {from_currency} zu {to_currency}"
        logging.warning(error_message)
        return None  # Rückgabe von None bei ungültigen Währungen

    # Berechnung des Umrechnungsbetrags
    conversion_rate = exchange_rates[to_currency] / exchange_rates[from_currency]
    converted_amount = amount * conversion_rate
    return converted_amount  # Rückgabe des umgerechneten Betrags

# Funktion zum Protokollieren von Aktivitäten
def log_activity(message):
    logging.info(message)  # Protokollieren der Aktivität mit dem gegebenen Nachrichteninhalt

# Liste für die Speicherung der Umrechnungshistorie
conversion_history = []  # Eine leere Liste, um Umrechnungshistorie zu speichern

# Hauptfunktion
@app.route("/", methods=["GET", "POST"])
def main():
    # Abrufen der Umrechnungskurse nur für CHF von der API
    api_key = config.EXCHANGE_RATE_API_KEY
    exchange_rates = get_exchange_rates(api_key)

    # Liste der 20 verschiedenen Währungen
    currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CNY", "INR", "SGD", "CHF",
                  "MYR", "NZD", "THB", "ZAR", "HKD", "SEK", "NOK", "MXN", "DKK", "RUB"]

    # Umrechnungen von 1 CHF in 20 verschiedene Währungen
    conversions = []  # Eine leere Liste für Umrechnungen
    if exchange_rates:
        for currency in currencies:
            if currency in exchange_rates:
                conversion_rate = exchange_rates[currency]  # Abrufen des Umrechnungskurses
                conversions.append((1, "CHF", conversion_rate, currency))  # Hinzufügen zur Liste der Umrechnungen

    if request.method == "POST":
        amount = request.form.get("amount", type=float)  # Abrufen des Betrags aus dem Formular
        from_currency = request.form.get("from_currency", "").upper()  # Abrufen der Ausgangswährung
        to_currency = request.form.get("to_currency", "").upper()  # Abrufen der Zielwährung

        if exchange_rates:
            # Umrechnung des Betrags mit den Umrechnungskursen
            converted_amount = convert_currency(amount, from_currency, to_currency, exchange_rates)
            if converted_amount is not None:
                # Protokollieren der durchgeführten Umrechnung
                log_activity(f"{amount} {from_currency} entspricht {converted_amount} {to_currency}.")
                # Hinzufügen der Umrechnung zur Umrechnungshistorie
                conversion_history.append((amount, from_currency, converted_amount, to_currency))
                # Rendern der Vorlage mit dem Ergebnis
                return render_template("result.html", amount=amount, from_currency=from_currency,
                                       converted_amount=converted_amount, to_currency=to_currency)
            else:
                error_message = "Die Umrechnung konnte nicht durchgeführt werden."
                logging.warning(error_message)
                return render_template("error.html", error_message=error_message)

    # Rendern der Startseite mit den Umrechnungen
    return render_template("index.html", conversions=conversions)

# Route für die Anzeige der Umrechnungshistorie
@app.route("/history")
def history():
    return render_template("history.html", conversion_history=conversion_history)

# Starten der Flask-Anwendung
if __name__ == "__main__":
    app.run(debug=True)  # Starten der Anwendung im Debug-Modus
