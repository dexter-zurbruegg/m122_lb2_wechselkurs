from flask import Flask, render_template, request
import api
import schedule
import time
import threading

app = Flask(__name__)

def run_program():
    api.get_exchange_rates()

def scheduled_job():
    schedule.every(12).hours.do(run_program)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', exchange_rates=api.get_exchange_rates())

if __name__ == '__main__':
    threading.Thread(target=scheduled_job).start()
    app.run(debug=True)
