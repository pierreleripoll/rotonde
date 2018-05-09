from sqlalchemy import *



engine = create_engine('sqlite:///baseRotonde.db', echo=True)


metadata = MetaData()



spectacle = Table('spectacle', metadata,
Column('nom', String, primary_key=True),
Column('resume', String, nullable = True),
Column('photo', Integer, nullable = True), #nombre de photos, path vers le dossier /uploads/nomSpectacle
Column('liens', String, nullable = True))

calendrier = Table('calendrier', metadata,
Column('date', String, nullable = False),
Column('nom', String, ForeignKey('spectacle.nom')),
Column('placesRestantes', Integer, nullable = False))

place = Table('places', metadata,
Column('idPlace', Integer, autoincrement=True, primary_key=True),
Column('nomSpectacle'),String,ForeignKey('spectacle.nom'),
Column('date', String, ForeignKey('calendrier.date')),
Column('nomUser', String, nullable = False))

sessions = Table('sessions', metadata,
Column('login',String,nullable=False),
Column('password',String,nullable=False))




metadata.create_all(engine)
connection = engine.connect()

connection.execute(spectacle.insert(), [
    {'nom': 'Don Juan', 'resume': 'pas cool'},
    {'nom': 'Le Cid', 'resume': 'not yet', 'photo' : 0},
    {'nom': 'Hamlet', 'resume': 'theatreEtude des petits', 'photo' : 0, 'liens' : 'coucou'}
])

connection.execute(calendrier.insert(), [
    {'date' : 'lundi', 'nom': 'Don Juan', 'placesRestantes': 10},
    {'date' : 'jeudi', 'nom': 'Don Juan', 'placesRestantes': 13},
    {'date' : 'mardi', 'nom': 'Le Cid', 'placesRestantes': 15},
    {'date' : 'mercredi', 'nom': 'Hamlet', 'placesRestantes': 0}
])

connection.execute(places.insert(), [
    {'date': 'lundi', 'nomUser': 'Arthur'},
    {'date': 'lundi', 'nomUser': 'Mathilde'},
    {'date': 'mardi', 'nomUser': 'Pierre'}
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
