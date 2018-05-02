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
