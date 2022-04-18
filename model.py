from flask_login import UserMixin
from pony.orm import *
from csv import DictReader

db = Database()

class Users(db.Entity, UserMixin):
  id = PrimaryKey(int)
  email = Required(str, unique=True)
  nickname = Required(str, unique=True)
  password = Required(str)
  points = Optional(int)  


class Questions(db.Entity):
  question = Required(str)
  options = Set("Answers")
  value_points = Required(int)


class Answers(db.Entity):
  answer = Required(str)
  related_question = Optional(Questions)  # Optional(Questions)
  the_value = Required(int)


if __name__ == '__main__':
  db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
  set_sql_debug(True)
  db.generate_mapping(create_tables=True)

  # import data from csv files into DB tables
  with db_session:
    with open('Users.txt') as f:    
      [Users(**r)for r in DictReader(f)]

    with open('Answers.txt') as f:    
      [Answers(**r) for r in DictReader(f)]

    with open('Questions.txt') as f:    
      for i, q in enumerate(DictReader(f)):
        Questions(**q).options.add( 
          [Answers[4*i+1], Answers[4*i+2], Answers[4*i+3], Answers[4*i+4]]
        )

else:
  db.bind(provider='sqlite', filename='database.sqlite', create_db=False)
  set_sql_debug(False)
  db.generate_mapping(create_tables=False)


"""
q1 = Questions(name='John', **q)
q1.cars 

q = Questions(**r)
q.tags.add([Answers['Party'], Answers['New Year']])

with db_session:
    o1 = Answers(answer='5', related_question=0, the_value=False)
    o2 = Answers(answer='0b101', related_question=0, the_value=True)
    o3 = Answers(answer='bin', related_question=0, the_value=False)
    o4 = Answers(answer='Error', related_question=0, the_value=False)
    Questions(question='Rezultat od bin(5) je?', options=[o1, o2, o3, o4], value_points=15)

Questions(**r).tags.add([Answers['Party'], Answers['New Year']])

q1 = Questions(**r)
a1 = Answers(**a)
a1.related_question = q1

Answers(**a).related_question = Questions(**r)

with db_session:
  with open('Questions.txt', 'r') as f:
    Lines = f.read().splitlines()

    for i in range (len(Lines)):
      Questions(question=Lines[i], value_points=i)


with db_session:
  with open('Answers.txt', 'r') as f:
    Lines = f.read().splitlines()

    for i in range (len(Lines)):
      Answers(question=Lines[i], value_points=i)

"""