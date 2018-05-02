from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *

import model

app = Flask(__name__)
app.secret_key = 'iswuygdedgv{&75619892__01;;>..zzqwQIHQIWS'

# TODO: Voir s'il serait possible de sortir la connexion et creation de la db de ce fichier

engine = create_engine('sqlite:///baseRotonde.db', echo=True)

metadata = MetaData()


spectacle = Table('spectacle', metadata,
            Column('nom', String, primary_key=True),
            Column('resume', String, nullable = True),
            Column('photo', String, nullable = True), #lien vers un file upload
            Column('liens', String, nullable = True)
            Column('prix', float, nullable = True))

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

connection = engine.connect()

@app.route('/', methods=['GET','POST'])
def logout():
    NomsSpectacles = []
    spectacles = get_spectacles()

    for spectacle in spectacles:
        NomsSpectacles.append(spectacle.nom)

    if request.method=='GET':
        return render_template('accueil.html', names=NomsSpectacles)
    if request.method=='POST':
        if request.form["bouton"] == "panier" :
            print("panier")
            return redirect('/panier')
        elif request.form["bouton"] == "calendrier" :
            print("calendrier")
            return redirect('/calendrier')
        elif request.form["bouton"] == "admin":
            print("admin")
            return redirect('/admin')
        else :
            return redirect('/')
