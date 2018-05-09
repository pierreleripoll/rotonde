from sqlalchemy import *
from sqlalchemy.sql import *
import re
import os
# Connexion a la DB

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

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
Column('date', String, ForeignKey('calendrier.date')),
Column('nomUser', String, nullable = False))

sessions = Table('sessions', metadata,
Column('login',String,nullable=False),
Column('password',String,nullable=False))

metadata.create_all(engine)

# Ici je definis des wrappers pour toutes les tables de la DB

class Date:
    def __init__(self,date,nom,placesRestantes):
        self.date = date
        self.nom = nom
        self.placesRestantes = placesRestantes
    def __str__(self):
        return self.nom+","+self.date+","+str(self.placesRestantes)
    def __repr__(self):
        return str(self)

class Place:
    def __init__(self,idPlace,nom,date,heure,nombre):
        self.idPlace = idPlace
        self.nom = nom
        self.date = date
        self.heure = heure
        self.nombre = nombre

    def setNombre(self,nombre):
        self.nombre = nombre

class Spectacle:
    def __init__(self, nom, resume, photos, liens):
        self.nom = nom
        self.resume = resume
        # self.prix = prix
        self.photos = photos
        self.liens = liens

    def __repr__(self):
        return "<Spectacle: %s, %s, %s>"%(self.nom, self.resume, self.prix)

class Session:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return "<Session: %s, %s>"%(self.login, self.password)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def urlify(s):

     # Remove all non-word characters (everything except numbers and letters)
     s = re.sub(r"[^\w\s]", '', s)

     # Replace all runs of whitespace with a single dash
     s = re.sub(r"\s+", '-', s)

     return s.lower()

def connect():
    conn = engine.connect()
    return conn


# Renvoie une liste contenant tous les spectacles.
def get_spectacles():
    conn = connect()
    query = 'SELECT nom, resume, photo, liens FROM spectacle'
    result = conn.execute(query)
    spectacles = []
    for row in result:
        spectacle = Spectacle(row["nom"], row["resume"], row["photo"], row["liens"])
        spectacles.append(spectacle)
    conn.close()

    return spectacles


# Renvoie le spectacle portant le nom specifife
def get_spectacle(nomSpectacle):
    conn = connect()
    name = "'" + nomSpectacle +"'"
    query = '''SELECT * FROM spectacle WHERE nom == '''+name
    result = conn.execute(query)
    spectacle = None
    for row in result:
        spectacle = Spectacle(row["nom"], row["resume"], row["photo"], row["liens"])


    conn.close()

    return spectacle

def insert_spectacle(spectacle):
    conn = connect()
    query = '''INSERT INTO spectacle (nom,resume,photo,liens) VALUES ('''+"'"+spectacle.nom+"'"+","+"'"+spectacle.resume+"'"+","+"'"+str(spectacle.photos)+"'"+","+"'"+spectacle.liens+"'"+")"
    result = conn.execute(query)
    return

# Update un spectacle
def update_spectacle(spectacle):
    conn = connect()
    query = '''UPDATE spectacle SET resume ='''+"'"+spectacle.resume+"'"+","+"photo ="+"'"+str(spectacle.photos)+"'"+","+"liens="+"'"+spectacle.liens+"'"+'''
    WHERE nom= spectacle.nom'''
    result = conn.execute(query)
    return
# Renvoie les dates disponibles pour un spectacles
def get_dates(nomSpectacle):
    conn = connect()
    name = "'" + nomSpectacle +"'"
    query = '''SELECT * FROM calendrier WHERE nom == '''+name
    result = conn.execute(query)
    dates = []
    for row in result:
        date = Date(row["date"], row["nom"], row["placesRestantes"])
        dates.append(date)

    conn.close()

    return dates

def get_sessions():
    conn = connect()
    query = 'select login, password from sessions'
    result = conn.execute(query)

    sessions = []

    for row in result:
        sess = Session(row["login"], row["password"])
        sessions.append(sess)

    conn.close()

    return sessions
