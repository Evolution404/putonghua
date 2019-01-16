from flask import Flask
from flask import render_template, request
from api import api

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


app.register_blueprint(api)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
