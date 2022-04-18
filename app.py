from flask import Flask, jsonify,Response, redirect, render_template, request, flash
from pony.flask import Pony
from flask_login import LoginManager, UserMixin, login_required, login_user
from datetime import datetime
from random import randint
from model import *

app = Flask(__name__)
Pony(app)
login_manager = LoginManager(app)
login_manager.login_view = '/'

@login_manager.user_loader
def load_user(user_id):
    return db.Users.get(id=user_id)

@app.route("/game")
@login_required
def game():
    users = select(u for u in Users)
    all_questions = list(select(q for q in Questions))
    # izaberi slucajno pitanje
    question = all_questions[ randint(0, len(all_questions)-1) ]
    data = {
        "users" : users,
        "question" : question
    }
    return render_template("game.html", data=data)
    # return render_template("index.html", data=data)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/logovanje", methods=["POST"])
def logovanje ():
    username = request.form['user']
    password = request.form['password']
    user = db.Users.get(email=username)
    if user:
        sifra_iz_baze = user.password     
        if (sifra_iz_baze == password):
            print('logovanje OK')
            login_user(user)
            return redirect("/game")
    else:    
        flash("Pogresan username ili password!")
        print("Pogresan username ili password!")
        return redirect("/")
        
    
@app.route("/time")
def show_time():
    return jsonify(datetime.now())



if __name__ == '__main__':
    print('Web server is running ...',)
    app.secret_key='secret123'
    app.run(host='0.0.0.0', debug=True)
# %%
