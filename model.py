from sqlalchemy import *
from sqlalchemy.sql import *


# Ici je définis des wrappers pour toutes les tables de la DB

class Place:
    def __init__(self,nom,date,heure,nombre):
        self.nom = nom
        self.date = date
        self.heure = heure
        self.nombre = nombre

    def setNombre(self,nombre):
        self.nombre = nombre

class Spectacle:

    def __init__(self, nom, resume, prix, photos, liens):
        self.nom = nom
        self.resume = resume
        self.prix = prix
        self.photos = photos
        self.liens = liens

    def __repr__(self):
        return "<Spectacle: %s, %s, %s€>"%(self.nom, self.resume, self.prix)


# Connexion a la DB

engine = create_engine('sqlite:///baseRotonde.db', echo=True)

def connect(arg):
    conn = engine.connect()
    return conn


# Renvoie une liste contenant tous les spectacles.
def get_spectacles():
    conn = connect()
    query = 'SELECT nom, resume, prix, photos, liens FROM spectacle'
    result = conn.execute(query)

    spectacles = []

    for row in result:
        spectacle = Spectacle(row["nom"], row["resume"], row["prix"], row["photos"], row["liens"])

        spectacles.append(spectacle)

    conn.close()

    return spectacles
