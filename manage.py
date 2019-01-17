import config
from flask import render_template, session, redirect
from api import api
from util import login_required
from models import StuInfo, app

app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = config.PERMANENT_SESSION_LIFETIME


@app.route('/', methods=["GET"])
def login():
    if session.get('id'):
        return redirect('/confirm')
    return render_template('login.html')


@app.route('/confirm', methods=["GET"])
@login_required
def confirm():
    return render_template('confirm.html')


app.register_blueprint(api)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
