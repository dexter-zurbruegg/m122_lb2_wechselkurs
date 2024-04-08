from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = '07b43fd62ae9d052c6ab74c6'
API_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    from_currency = request.form['from_currency']
    to_currency = request.form['to_currency']
    amount = float(request.form['amountt'])

    response = requests.get(API_URL + from_currency)
    data = response.json()
    conversion_rate = data['conversion_rates'][to_currency]
    converted_amount = amount * conversion_rate

    return render_template('result.html', from_currency=from_currency, to_currency=to_currency, amount=amount, converted_amount=converted_amount)

if __name__ == '__main__':
    app.run(debug=True)
