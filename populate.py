from app import app
from model import *
import os
import shutil

if os.path.exists("baseRotonde.db"):
    os.remove("baseRotonde.db")

folder = 'static/uploads'
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            if os.path.basename(file_path) not in ['hamlet-60','candide',"chroniques-nocturne","rapa-nui","jeanne-de-derteil"]:
                shutil.rmtree(file_path)
    except Exception as e:
        print(e)

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
Spectacle(nom='Spectacle sans photo',resume=lorem,admin='AMI',photos=0,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=0,duree=60,typeSpectacle='Théâtre'),
Spectacle(nom='Chroniques Nocturne',resume=lorem,admin='AMI',photos=1,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=0,duree=60,typeSpectacle='Théâtre'),
Spectacle(nom='Hamlet 60',resume=lorem,admin='AMI',photos=1,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=0,duree=60,typeSpectacle='Théâtre'),
Spectacle(nom='Jeanne de Derteil',resume=lorem,admin='AMI',photos=1,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=0,duree=60,typeSpectacle='Théâtre'),
Spectacle(nom='Rapa Nui',resume=lorem,admin='AMI',photos=1,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=0,duree=60,typeSpectacle='Théâtre'),

Photo(path="./static/uploads/hamlet-60/fight-for-the-water-hole-1903.jpg",spectacle="Hamlet 60",ordre=0),
Photo(path="./static/uploads/chroniques-nocturne/dance-class-at-the-opera-1872.jpg",spectacle="Chroniques Nocturne",ordre=0),
Photo(path="./static/uploads/candide/large_pierrot_le_fou_blu-ray6x.jpg",spectacle="Candide",ordre=0),
Photo(path="./static/uploads/jeanne-de-derteil/march-1895.jpg",spectacle="Jeanne de Derteil",ordre=0),
Photo(path="./static/uploads/rapa-nui/river-in-saint-clair.jpg",spectacle="Rapa Nui",ordre=0)




]

with app.app_context():
    db.create_all();

    for elem in content:
        db.session.add(elem)

    db.session.commit()
