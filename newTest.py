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


@app.route('/test', methods=['GET','POST'])
def function():
    if request.method=='GET':
        return render_template('ajoutvaleur.html')
    if request.method=='POST':
        print("HELLLO")
        connection = engine.connect()
        connection.execute(places.insert() , [ {"date":request.form["the_date"], "nomUser":request.form["name"]}] )
        return redirect('/')

@app.route('/')
def logout():
    if request.method=='GET':
        return render_template('allerPanier.html')
    if request.method=='POST':
        return redirect('/test')

if __name__ == '__main__':
  app.run(debug=True)


connection.close()
