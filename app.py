from flask import Flask, jsonify,Response, redirect, render_template, request, flash
from pony.flask import Pony
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
from datetime import datetime
from random import randint
from model import *

app = Flask(__name__)
Pony(app)
login_manager = LoginManager(app)
login_manager.login_view = '/'

odgovori = {}


@login_manager.user_loader
def load_user(user_id):
    return db.Users.get(id=user_id)

# @app.route("/game/<int:pitanje>")
@app.route("/game/<int:pitanje>/<int:odg>")
@login_required
def game(pitanje, odg):
    global odgovori
    users = select(u for u in Users)
    n_pit = len(select(q for q in Questions))
    
    if odg != 0:
        odgovori.update({pitanje-1: odg})
        
    if pitanje > n_pit:
        return redirect("/kraj")
    
    data = {
        "users" : users,
        "question" : Questions[pitanje],
        "nextlink": f'/game/{pitanje+1}',
    }
    return render_template("game.html", data=data)


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
            # print(current_user.get_id())
            return redirect("/game/1/0")
    else:    
        flash("Pogresan username ili password!")
        print("Pogresan username ili password!")
        return redirect("/")
        
    

@app.route("/kraj")
@login_required
def kraj():
    """
    poslednji korak koji proverava tacne odgovore i upisuje broj poena u tabelu Users
    """ 
    poena = 0   
    for (pit, odg) in odgovori.items():
        if Answers[odg].the_value == 1:
            poena += Questions[pit].value_points
        
    userid  = current_user.get_id()
    print(userid)

    if poena >  Users[userid].points:
        with db_session:
            Users[userid].points= poena

    # Isctrava poslednju stranicu sa obavestenjem da je igra zavrsena
    data = {
        'users' : select(u for u in Users),
        'poena': poena
    }
    return render_template("kraj.html", data=data)



@app.route("/time")
def show_time():
    ''' Prikazuje vreme na serveru '''
    return jsonify(datetime.now())

app.secret_key = 'secret123'

if __name__ == '__main__':
    print('Web server is running ...',)

    app.run(host='0.0.0.0', debug=True)

