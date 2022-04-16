from enum import unique
from flask_login import UserMixin
from pony.orm import *

db = Database()

class Users(db.Entity, UserMixin):
  id = PrimaryKey(str)
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
  related_question = Required(Questions)
  the_value = Required(bool)


if __name__ == '__main__':
  db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
  set_sql_debug(True)
  db.generate_mapping(create_tables=True)
else:
  db.bind(provider='sqlite', filename='database.sqlite', create_db=False)
  set_sql_debug(False)
  db.generate_mapping(create_tables=False)


"""
with db_session:
  with open('Questions.txt', 'r') as f:
    Lines = f.read().splitlines()

    for i in range (len(Lines)):
      Questions(question=Lines[i], value_points=i)


with db_session:
  with open('Answers.txt', 'r') as f:
    Lines = f.read().splitlines()

    for i in range (len(Lines)):
      Answers(question=Lines[i], value_points=i)"""