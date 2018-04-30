from sqlalchemy import *
from flask  import *


engine = create_engine('sqlite:///baseRotonde.db', echo=True)


connection = engine.connect()

for row in connection.execute("select * from spectacle"):
    print(row)
print('\n')

for row in connection.execute("select * from calendrier"):
    print(row)
print('\n')

for row in connection.execute("select * from places"):
    print(row)
print('\n')

s = text('SELECT * FROM spectacle WHERE spectacle.nom LIKE :x')
for row in connection.execute(s, x='Hamlet%'):
    print(row)
print('\n')

connection.close()
