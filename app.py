from flask import Flask

app = Flask(__name__)


@app.route('/')
def api_call():  # put application's code here
    return '<div>Hello World!<div>'


if __name__ == '__main__':
    app.run()


