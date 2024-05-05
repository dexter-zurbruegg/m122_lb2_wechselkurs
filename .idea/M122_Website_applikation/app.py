from flask import Flask, render_template, request
import requests
import logging
import config

app = Flask(__name__)


# Funktion zum Abrufen der Wechselkurse von der API
def get_exchange_rates(api_key):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("conversion_rates")
    except requests.RequestException as e:
        app.logger.warning(f"Fehler beim Abrufen der Wechselkurse von der API: {str(e)}")
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
        amount = float(request.form.get("amount", 0))
        from_currency = request.form.get("from_currency", "").upper()
        to_currency = request.form.get("to_currency", "").upper()

        api_key = config.EXCHANGE_RATE_API_KEY
        exchange_rates = get_exchange_rates(api_key)

        if exchange_rates:
            converted_amount = convert_currency(amount, from_currency, to_currency, exchange_rates)
            if converted_amount:
                log_activity(f"{amount} {from_currency} entspricht {converted_amount} {to_currency}.")
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
