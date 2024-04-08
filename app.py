from flask import Flask, render_template
import api

app = Flask(__name__)


@app.route('/')
def index():
    exchange_rates = api.get_exchange_rates()
    return render_template('index.html', exchange_rates=exchange_rates)


if __name__ == '__main__':
    app.run()


