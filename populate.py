from app import app
from model import *

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
Spectacle(nom='Rapa Nui',resume=lorem,admin='AMI',photos=1,directeur='John Doe',auteur='John Doe',participants='John Doe',infoComplementaire=lorem,tarif=0,duree=60,typeSpectacle='Théâtre')

]

with app.app_context():
    db.create_all();

    for elem in content:
        db.session.add(elem)

    db.session.commit()
