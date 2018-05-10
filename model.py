from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
import os
# Connexion a la DB


db = SQLAlchemy()

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

class Spectacle(db.Model):
    nom = db.Column(db.String(80), primary_key = True)
    resume = db.Column(db.Text, nullable = True)
    photo = db.Column(db.Integer, nullable = True)
    liens = db.Column(db.String, nullable = True)

    def __repr__(self):
        return '<Spectacle: %r>' % self.nom

class Calendrier(db.Model):
    date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow, primary_key = True)
    nom = db.Column(db.String(80),db.ForeignKey('spectacle.nom'), nullable = False)
    placesRestantes = db.Column(db.Integer, nullable = False)

    spectacle = db.relationship('Spectacle', backref = db.backref('calendriers', lazy = True)) # Peut etre a changer, pas sur de ce que je fais

    def __repr__(self):
        return '<Calendrier: %r>' % self.date

class Place(db.Model):
    idPlace = db.Column(db.Integer, autoincrement = True, primary_key = True)
    nomSpectacle = db.Column(db.String(80), db.ForeignKey('spectacle.nom'), nullable = False)
    date = db.Column(db.DateTime, db.ForeignKey('calendrier.date'), nullable = False)
    nomUser = db.Column(db.String(80), nullable = False)

    calendrier = db.relationship('Calendrier', backref = db.backref('places', lazy = True)) #idem qu'au dessus

    def __repr__(self):
        return '<Place: %r>' % self.idPlace

class Session(db.Model):
    login = db.Column(db.String(80), nullable = False, primary_key = True)
    password = db.Column(db.String(300), nullable = False) # TODO: encrypter le mdp avec passlib

    def __repr__(self):
        return '<Session: %r %r>' % (self.login, self.password)

class Place:
    def __init__(self,nomSpectacle,nomUser,date,nombre):
        self.nomSpectacle=nomSpectacle
        self.nomUser = nomUser
        self.date = date
        self.nombre = nombre

    def setNombre(self,nombre):
        self.nombre = nombre


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

def get_all_places():
    conn = connect()
    query = 'SELECT * FROM places'
    result = conn.execute(query)
    places = []
    for row in result:
        place = Place(row["nomSpectacle"], row["nomUser"], row["date"],1)
        places.append(place)
    conn.close()

    return places

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

def insert_place(place):
    conn = connect()
    for i in range(place.nombre):
        query = '''INSERT INTO places (date,nomUser,nomSpectacle) VALUES ('''+"'"+place.date+"'"+","+"'"+place.nomUser+"'"+","+"'"+place.nomSpectacle+"'"+")"
        result = conn.execute(query)
    return
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
