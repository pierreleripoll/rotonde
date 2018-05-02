from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *

app = Flask(__name__)

engine = create_engine('sqlite:///baseRotonde.db', echo=True)

metadata = MetaData()


spectacle = Table('spectacle', metadata,
            Column('nom', String, primary_key=True),
            Column('resume', String, nullable = True),
            Column('photo', String, nullable = True), #lien vers un file upload
            Column('liens', String, nullable = True))

calendrier = Table('calendrier', metadata,
            Column('date', String, nullable = False),
            Column('nom', String, ForeignKey('spectacle.nom')),
            Column('placesRestantes', Integer, nullable = False))

places = Table('places', metadata,
            Column('idPlaces', Integer, autoincrement=True, primary_key=True),
            Column('date', String, ForeignKey('calendrier.date')),
            Column('nomUser', String, nullable = False))

metadata.create_all(engine)

connection = engine.connect()


@app.route('/panier', methods=['GET','POST'])
def panier():
    if request.method=='GET':
        return render_template('ajoutvaleur.html')
    if request.method=='POST':
        print("HELLLO")
        connection = engine.connect()
        connection.execute(places.insert() , [ {"date":request.form["the_date"], "nomUser":request.form["name"]}] )
        return redirect('/')

@app.route('/calendrier', methods=['GET','POST'])
def calendrier():
    if request.method=='GET':
        return render_template('calendrier.html')
    if request.method=='POST':
        return redirect('/')

@app.route('/spectacle', methods=['GET','POST'])
def spectacle():
    if request.method=='GET':
        return render_template('spectacle.html')
    if request.method=='POST':
        return redirect('/')

@app.route('/', methods=['GET','POST'])
def logout():
    connection = engine.connect()
    NomSpectacle = []
    for row in connection.execute('SELECT nom FROM spectacle'):
        print(row)
        NomSpectacle.append(row)
    print("\n")
    if request.method=='GET':
        return render_template('accueil.html', name=NomSpectacle)
    if request.method=='POST':
        if request.form["panier"] :
            print("panier")
            return redirect('/panier')
        elif request.form["calendrier"] :
            print("calendrier")
            return redirect('/calendrier')
        elif request.form["spectacle"] :
            print("spectacle")
            return redirect('/spectacle')
        else :
            return redirect('/')

if __name__ == '__main__':
  app.run(debug=True)


connection.close()
