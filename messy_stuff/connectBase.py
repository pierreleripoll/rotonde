from sqlalchemy import *
from flask  import *


engine = create_engine('sqlite:///baseRotonde.db', echo=True)

metadata = MetaData()

spectacle = Table('spectacle', metadata,
            Column('nom', String, primary_key=True),
            Column('resume', String, nullable = True),
            Column('photo', String, nullable = True), #lien vers un file upload
            Column('liens', String, nullable = True))

calendrier = Table('calendrier', metadata,
            Column('date', String, nullable = False),
            Column('nom', String, ForeignKey('spectacle.nom')),
            Column('placesRestantes', Integer, nullable = False))

places = Table('places', metadata,
            Column('idPlaces', Integer, autoincrement=True, primary_key=True),
            Column('date', String, ForeignKey('calendrier.date')),
            Column('nomUser', String, nullable = False))

connection = engine.connect()

connection.execute(spectacle.insert(), [
    {'nom': 'patron', 'resume': 'aaaaaaaaaaa'}
])

connection.execute(calendrier.insert(), [
    {'date' : 'dimanche', 'nom': 'Don Juan', 'placesRestantes': 13},
])

connection.execute(places.insert(), [
    {'date': 'dimanche', 'nomUser': 'Arthuro'},
])

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
