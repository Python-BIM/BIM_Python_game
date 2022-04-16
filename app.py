from flask import Flask, jsonify,Response, redirect, render_template, request, flash
from pony.flask import Pony
from flask_login import LoginManager, UserMixin, login_required, login_user
from datetime import datetime
from model import *

app = Flask(__name__)
Pony(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.Users.get(id=user_id)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login ():
    return render_template("login.html")

@app.route("/logovanje", methods=["POST"])
def logovanje ():
    username = request.form['user']
    password = request.form['password']
    user = db.Users.get(email=username)
    if (not user):
        flash("Pogresan username ili password!")
        print("Pogresan username ili password!")
        return redirect("/login")
    else: 
        print('+++ logovanje OK')
        login_user(user)
        return redirect("/")
        

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
    app.secret_key='secret123'
    app.run(host='0.0.0.0', debug=True)
# %%
