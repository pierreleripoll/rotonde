from flask_sqlalchemy import SQLAlchemy#,CheckConstraint
from datetime import datetime
import re
import os
# Connexion a la DB


db = SQLAlchemy()

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

class Spectacle(db.Model):
    nom = db.Column(db.String(80), primary_key = True,nullable=False)
    resume = db.Column(db.Text, nullable = True)
    photos = db.Column(db.Integer, nullable = True)
    liens = db.Column(db.String(150), nullable = True)
    admin = db.Column(db.String(20), nullable =True)
    idContact = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable = True)
    directeur = db.Column(db.String(30),nullable=True)
    auteur = db.Column(db.String(30),nullable=True)
    participants = db.Column(db.String(30),nullable=True)
    infoComplementaire = db.Column(db.String(100),nullable=True)
    tarif = db.Column(db.Integer,nullable=True)
    duree = db.Column(db.Integer,nullable=True)
    typeSpectacle = db.Column(db.String(20),nullable=True)
    def __repr__(self):
        return '<Spectacle: %r>' % self.nom

class Contact(db.Model):
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    nom = db.Column(db.String(80))
    prenom = db.Column(db.String(80))
    telephone = db.Column(db.Integer, nullable = True)
    adresseMail = db.Column(db.String, nullable = True)
    annee = db.Column(db.Integer, nullable = True) #si 0 =  c'est un exterieur de l'INSA
    depart = db.Column(db.String, nullable = True)
    def __repr__(self):
        return '<Contact: %r>' % self.nom

class Calendrier(db.Model):
    date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow, primary_key = True)
    nom = db.Column(db.String(80),db.ForeignKey('spectacle.nom'), nullable = False)
    placesRestantes = db.Column(db.Integer, nullable = False)
    spectacle = db.relationship('Spectacle', backref = db.backref('calendriers', lazy = True)) # Peut etre a changer, pas sur de ce que je fais
    #CheckConstraint('placesRestantes >= 0', name='pos')
    def __repr__(self):
        return '<Calendrier: %r>' % self.date

class Place(db.Model):
    idPlace = db.Column(db.Integer, autoincrement = True, primary_key = True)
    nomSpectacle = db.Column(db.String(80), db.ForeignKey('spectacle.nom'), nullable = False)
    date = db.Column(db.DateTime, db.ForeignKey('calendrier.date'), nullable = False)
    nomUser = db.Column(db.String(80), nullable = False)
    adresseMail = db.Column(db.String(100),nullable=True)
    calendrier = db.relationship('Calendrier', backref = db.backref('places', lazy = True)) #idem qu'au dessus
    def __repr__(self):
        return '<Place: %r>' % self.idPlace

    def serialize(self):
        dic = {}
        dic["nomSpectacle"]=self.nomSpectacle
        dic["date"]=self.date
        dic["nomUser"]=self.nomUser
        return dic

    # TODO: Remettre le setNombre si besoin ?

class Session(db.Model):
    login = db.Column(db.String(80), nullable = False, primary_key = True)
    password = db.Column(db.String(300), nullable = False) # TODO: encrypter le mdp avec passlib
    typeAdmin = db.Column(db.String(30),nullable=False)
    idContact = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable = True)
    def __repr__(self):
        return '<Session: %r %r>' % (self.login, self.password)


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
    spectacles = Spectacle.query.all()
    return spectacles

def get_all_places():
    places = Place.query.all()
    return places

# Renvoie les places correspondant a un nom
def get_places_user_name(userName):
	places = Place.query.filter_by(nomUser=userName).all()
	return places

def get_contact():
    contact = Contact.query.all()
    return contact

# Renvoie le spectacle portant le nom specifife
def get_spectacle(nomSpectacle):
    spectacle = Spectacle.query.filter_by(nom=nomSpectacle).first()

    return spectacle

# Renvoie l'objet Date correspondant a la date en param
def get_date (date):
	date= Calendrier.query.filter_by(date=date).first()
	return date

def insert_place(place):
    db.session.add(place)


def commit_place_insertion():
    db.session.commit()

    return

def insert_date(date):
    db.session.add(date)
    return

def insert_contact(contact):
    db.session.add(contact)
    db.session.commit()
    return

def insert_spectacle(spectacle):
    db.session.add(spectacle)
    db.session.commit()
    return

# Update un spectacle
def update_spectacle(spectacle):
    oldSpectacle = Spectacle.query.filter_by(nom=spectacle.nom).first()

    oldSpectacle.resume = spectacle.resume
    oldSpectacle.photos = spectacle.photos
    oldSpectacle.liens = spectacle.liens

    db.session.commit()

    return

# Update une date
def update_date(newDate):
    oldDate = Calendrier.query.filter_by(date=newDate.date).first()
    oldDate.date = newDate.date
    oldDate.nom = newDate.nom
    oldDate.placesRestantes = newDate.placesRestantes

    db.session.commit()

    return

#update le nombre de places sur une date
def update_placesRestantes (date, placesPrises):
	date.placesRestantes=date.placesRestantes - placesPrises

	db.session.commit()

	return

#Convertir une date html en python
def dateHTMLtoPy(date_in):
    datetimePy = datetime.strptime(date_in,'%Y-%m-%dT%H:%M')
    return datetimePy

def dateJSONToPy(date_in):
    print("dateJSONToPy ",date_in)
    datetimePy = datetime.strptime(date_in,'%Y-%m-%d %H:%M:%S')
    return datetimePy

def datePytoHTML(date_in):
    datetimeHTML = date_in.strftime('%Y-%m-%dT%H:%M')
    return datetimeHTML

# Renvoie les dates disponibles pour un spectacle
def get_dates(nomSpectacle):
    dates = Calendrier.query.filter_by(nom = nomSpectacle).all()

    return dates

#Renvoie l'ensemble des dates disponibles
def get_all_dates ():
    dates = Calendrier.query.all()

    return dates

def get_sessions():

    sessions = Session.query.all()

    return sessions
