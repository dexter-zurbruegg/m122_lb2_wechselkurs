from flask import Flask, render_template, request, redirect, url_for
import requests
import logging

app = Flask(__name__)

# Funktion zum Abrufen der Wechselkurse von der API
def get_exchange_rates():
    api_key = "07b43fd62ae9d052c6ab74c6"
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data["conversion_rates"]
    else:
        print("Fehler beim Abrufen der Daten von der API.")
        return None

# Funktion zur Währungsumrechnung
def convert_currency(amount, from_currency, to_currency, exchange_rates):
    if from_currency not in exchange_rates or to_currency not in exchange_rates:
        return None

    conversion_rate = exchange_rates[to_currency] / exchange_rates[from_currency]
    converted_amount = amount * conversion_rate
    return converted_amount

# Funktion zum Protokollieren von Aktivitäten
def log_activity(message):
    logging.basicConfig(filename='currency_converter.log', level=logging.INFO)
    logging.info(message)

# Liste für die Speicherung der Umrechnungshistorie
conversion_history = []

# Hauptfunktion
@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        amount = float(request.form["amount"])
        from_currency = request.form["from_currency"].upper()
        to_currency = request.form["to_currency"].upper()

        exchange_rates = get_exchange_rates()
        converted_amount = convert_currency(amount, from_currency, to_currency, exchange_rates)

        if converted_amount:
            log_activity(f"{amount} {from_currency} entspricht {converted_amount} {to_currency}.")
            # Speichern der Umrechnung in der Historie
            conversion_history.append((amount, from_currency, converted_amount, to_currency))

            return render_template("result.html", amount=amount, from_currency=from_currency,
                                   converted_amount=converted_amount, to_currency=to_currency)

    return render_template("index.html")

# Route für die Anzeige der Umrechnungshistorie
@app.route("/history")
def history():
    return render_template("history.html", conversion_history=conversion_history)

if __name__ == "__main__":
    app.run(debug=True)
