from pony.orm import *

db = Database()

class Users(db.Entity):
  email = PrimaryKey(str)
  nickname = Required(str, unique=True)
  password = Required(str)
  points = Optional(int)  


class Questions(db.Entity):
  question = Set("Answers")
  value_points = Required(int)


class Answers(db.Entity):
  answer = Required(str)
  related_question = Required(Questions)
  the_value = Required(bool)


db.bind(provider='sqlite', filename='database.sqlite', create_db=False)

set_sql_debug(True)

db.generate_mapping(create_tables=True)