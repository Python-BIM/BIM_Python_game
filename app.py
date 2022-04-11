from flask import Flask, jsonify,Response, render_template
from datetime import datetime
from model import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login ():
    return render_template("login.html")


@app.route("/time")
def show_time():
    return jsonify(datetime.now())



@app.route("/src")
def show_source():
    with open('app.py', 'r') as file:
        resp = Response(file.read())
        resp.headers['Content-type'] = 'text/plan'
        return resp


if __name__ == '__main__':
    print('Web server is running ...',)
    # app.secret_key=''
    app.run(host='0.0.0.0', debug=True)
# %%
