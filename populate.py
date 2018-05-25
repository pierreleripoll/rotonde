from app import app
from model import *
import os
from datetime import datetime

try:
    os.remove("baseRotonde.db")
except OSError:
    pass


ami = Session(login='ami',password='friendly',typeAdmin='normal')
cgr = Session(login='cgr',password='cafards',typeAdmin='super')
superadmin = Session(login='superadmin',password='larotonde')
contact = Contact(nom="---",prenom="---",annee="",depart="")

lorem = 'Bacon ipsum dolor amet nostrud tongue tail corned beef minim porchetta drumstick eu laborum reprehenderit bacon flank. Ribeye flank aliqua frankfurter ham beef quis consequat in porchetta reprehenderit pariatur. '

content = [

Session(login='ami',password='friendly',typeAdmin='normal'),
Session(login='cgr',password='cafards',typeAdmin='super'),
Session(login='superadmin',password='larotonde',typeAdmin='super'),
Contact(nom="---",prenom="---",annee="",depart=""),

Spectacle(nom='Candide',resume=lorem,admin='AMI',photos=1,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=0,duree=60,typeSpectacle='Théâtre'),
Spectacle(nom='Chroniques Nocturne',resume=lorem,admin='AMI',photos=1,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=0,duree=60,typeSpectacle='Théâtre'),
Spectacle(nom='Hamlet 60',resume=lorem,admin='AMI',photos=1,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=0,duree=60,typeSpectacle='Théâtre'),
Spectacle(nom='Jeanne de Derteil',resume=lorem,admin='AMI',photos=1,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=0,duree=60,typeSpectacle='Théâtre'),
Spectacle(nom='Rapa Nui',resume=lorem,admin='AMI',photos=1,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=0,duree=60,typeSpectacle='Théâtre'),

Calendrier(date=datetime(2018,5,25,20,30),nom='Candide',placesRestantes=300),
Calendrier(date=datetime(2018,5,26,20,30),nom='Spectacle sans photo',placesRestantes=300),
Calendrier(date=datetime(2018,5,27,20,30),nom='Chroniques Nocturne',placesRestantes=300),
Calendrier(date=datetime(2018,5,28,20,30),nom='Hamlet 60',placesRestantes=300),
Calendrier(date=datetime(2018,5,29,20,30),nom='Jeanne de Derteil',placesRestantes=300),
Calendrier(date=datetime(2018,5,30,20,30),nom='Rapa Nui',placesRestantes=300)

]

with app.app_context():
    db.create_all();

    for elem in content:
        db.session.add(elem)

    db.session.commit()
