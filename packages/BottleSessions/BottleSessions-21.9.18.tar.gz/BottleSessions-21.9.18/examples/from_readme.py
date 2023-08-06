#app.py:

from BottleSessions import BottleSessions
from bottle import Bottle, request

app = Bottle()
btl = BottleSessions(app)

@app.route('/set/<key>/<val>')
def set_sess(key,val=None):

    request.session[key] = val
    return {key: val}

@app.route('/get/<key>')
def get_sess(key=None):

    return {key: request.session.get(key,'does not exist')}

@app.route('/')
def hello():
    return 'hello world'

if __name__ == '__main__':
    app.run()
