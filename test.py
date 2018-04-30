
from flask import *
from sqlalchemy import *

app = Flask(__name__)


engine = create_engine('sqlite:///memory', echo=True)


metadata = MetaData()

valeurs = Table('valeurs',metadata,
            Column( 'val',Integer))

metadata.create_all(engine)

connection=engine.connect()


@app.route('/test', methods=['GET','POST'])
def function():
    if request.method=='GET':
        return render_template('ajoutvaleur.html')
    if request.method=='POST':
        connection.execute(valeurs.insert(), [ {'val' : 10} ] )
        return redirect('/')

@app.route('/')
def logout():
  return 'Sauvegarde'

if __name__ == '__main__':
  app.run(debug=True)

connection.close()
