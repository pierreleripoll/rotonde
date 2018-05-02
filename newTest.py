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

sessions = Table('sessions', metadata,
            Column('login',String,nullable=False),
            Column('password',String,nullable=False))

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

@app.route('/admin_log', methods=['GET','POST'])
def admin_log():
    if request.method=='GET':
        return render_template('admin_log.html')
    if request.method=='POST':
        connection = engine.connect()
        result = connection.execute(select([sessions]))
        login = request.form["login"]
        password = request.form["password"]
        for row in result :
            if login == row[0] and password == row[1]:
                welcomeString = "WELCOME "+login.upper()
                print("\n\n")
                print(len(welcomeString)*'*')
                print(welcomeString)
                print(len(welcomeString)*'*')
                print("\n\n")
                session['pseudo']=login.upper()
                session['root']="true"

        return redirect('/')

@app.route('/admin', methods=['GET','POST'])
def admin():

    if 'pseudo' in session :
        if request.method=='GET':
            return render_template('admin.html',pseudo = session["pseudo"])
        if request.method=='POST':
            return redirect('/')
    else :
        return redirect('/admin_log')


@app.route('/calendrier', methods=['GET','POST'])
def calendrier():
    if request.method=='GET':
        return render_template('calendrier.html')
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
        return render_template('accueil.html', names=NomSpectacle)
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

if __name__ == '__main__':
  app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
  app.run(debug=True)


connection.close()
