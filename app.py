from flask import Flask, render_template, request
import api


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    alt_response = api.get_alternative_exchange_rates()
    print(alt_response)
    return render_template('index.html', exchange_rates=api.get_exchange_rates())


if __name__ == '__main__':
    app.run(debug=True)
