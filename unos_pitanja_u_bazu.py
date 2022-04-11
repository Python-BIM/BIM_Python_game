# U ovom fajlu je dat primer kako se unose podaci u bazu
# pomocu SQL-a i Pony ORM-a
# iskorstite ovaj primer za pravljenje import skirpte ili 
# backenda koga poziva forma za unos

from model import *

# Kroz SQL
# db.execute("INSERT INTO Questions VALUES(0, 'Šta vrać type(0)',10);")
# db.execute("INSERT INTO Answers VALUES(1, '0',0);")
# db.execute("INSERT INTO Answers VALUES(2, 'flaot',0);")
# db.execute("INSERT INTO Answers VALUES(3, 'false',0);")
# db.execute("INSERT INTO Answers VALUES(4, 'int',0);")


# korak po korak interaktivno u python konzoli
'''
db.Users(email='mika@gmaio.com', nickname='Mika', password='sta', points=10)
db.Users(email='joca@gmail.com', nickname='Joca', password='fajld', points=0)

db.Questions(question='Šta vraća type(0)', value_points=10)
db.Answers(answer='0', related_question=1, the_value=False)
db.Answers(answer='float', related_question=1, the_value=False)
db.Answers(answer='type', related_question=1, the_value=False)
db.Answers(answer='int', related_question=1, the_value=True)
'''

# Ovaj je testiran
with db_session:
    o1 = Answers(answer='5', related_question=5, the_value=False)
    o2 = Answers(answer='0b101', related_question=5, the_value=True)
    o3 = Answers(answer='bin', related_question=5, the_value=False)
    o4 = Answers(answer='Error', related_question=5, the_value=False)
    Questions(question='Rezultat od bin(5) je?', options=[o1, o2, o3, o4], value_points=15)

