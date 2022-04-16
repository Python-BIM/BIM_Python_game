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

# @app.route("/")
@app.route("/game")
@login_required
# pogledati sta se desava kada odemo na /game
def game():
    users = select(u for u in Users)
    question = list(select(q for q in Questions))[0]
    data = {
        "users" : users,
        "question" : question
    }
    return render_template("index.html", data=data)

# @app.route("/login")
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/logovanje", methods=["POST"])
def logovanje ():
    username = request.form['user']
    password = request.form['password']
    user = db.Users.get(email=username)
    sifra_iz_baze = user.password 
   
    if (sifra_iz_baze!=password):
        flash("Pogresan username ili password!")
        print("Pogresan username ili password!")
        return redirect("/")
    else: 
        print('+++ logovanje OK')
        login_user(user)
        return redirect("/game")
        

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
