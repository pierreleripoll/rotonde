# -*- coding: utf-8 -*-

from app import app
from model import *
import os
import shutil
import time

if os.path.exists("baseRotonde.db"):
    os.remove("baseRotonde.db")

folder = 'static/uploads'
sauvegarde = 'sauvegarde'

if os.path.exists(folder):
    shutil.rmtree(folder)
time.sleep(1)
folders = os.listdir(sauvegarde)

for fol in folders:
    if os.path.isdir(sauvegarde+'/'+fol):
        print('dir',fol)
        shutil.copytree(sauvegarde+'/'+fol, folder+'/'+fol)




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

Spectacle(nom='Candide',resume=lorem,admin='AMI',photos=1,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=3,duree=60,typeSpectacle='Theatre'),
Spectacle(nom='Spectacle sans photo',resume=lorem,admin='AMI',photos=0,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=0,duree=60,typeSpectacle='Theatre'),
Spectacle(nom='Chroniques Nocturne',resume=lorem,admin='AMI',photos=1,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=0,duree=60,typeSpectacle='Theatre'),
Spectacle(nom='Hamlet 60',resume=lorem,admin='AMI',photos=1,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=0,duree=60,typeSpectacle='Theatre'),
Spectacle(nom='Jeanne de Derteil',resume=lorem,admin='AMI',photos=1,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=0,duree=60,typeSpectacle='Theatre'),
Spectacle(nom='Rapa Nui',resume=lorem,admin='AMI',photos=1,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=0,duree=60,typeSpectacle='Theatre'),

Photo(path="/static/uploads/hamlet-60/fight-for-the-water-hole-1903.jpg",spectacle="Hamlet 60",ordre=0,size=141619),
Photo(path="/static/uploads/chroniques-nocturne/dance-class-at-the-opera-1872.jpg",spectacle="Chroniques Nocturne",ordre=0,size=216401),
Photo(path="/static/uploads/candide/large_pierrot_le_fou_blu-ray6x.jpg",spectacle="Candide",ordre=0,size=469024),
Photo(path="/static/uploads/jeanne-de-derteil/march-1895.jpg",spectacle="Jeanne de Derteil",ordre=0,size=1554534),
Photo(path="/static/uploads/rapa-nui/river-in-saint-clair.jpg",spectacle="Rapa Nui",ordre=0,size=598110),

Calendrier(date=datetime(2018,5,26,20,30),nom='Spectacle sans photo',placesRestantes=300),
Calendrier(date=datetime(2018,5,27,20,30),nom='Chroniques Nocturne',placesRestantes=300),
Calendrier(date=datetime(2018,5,28,20,30),nom='Hamlet 60',placesRestantes=300),
Calendrier(date=datetime(2018,5,29,20,30),nom='Jeanne de Derteil',placesRestantes=300),
Calendrier(date=datetime(2018,5,30,20,30),nom='Rapa Nui',placesRestantes=300),
Calendrier(date=datetime(2018,5,31,20,30),nom='Rapa Nui',placesRestantes=300),
Calendrier(date=datetime(2018,6,1,20,30),nom='Rapa Nui',placesRestantes=300),
Calendrier(date=datetime(2018,6,2,20,30),nom='Rapa Nui',placesRestantes=300),
Calendrier(date=datetime(2018,6,3,20,30),nom='Candide',placesRestantes=300),
Calendrier(date=datetime(2018,6,4,20,30),nom='Candide',placesRestantes=300),
Calendrier(date=datetime(2018,6,5,20,30),nom='Candide',placesRestantes=300),

]

with app.app_context():
    db.create_all();

    for elem in content:
        db.session.add(elem)

    db.session.commit()
