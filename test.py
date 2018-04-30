
from flask import *
from sqlalchemy import *

app = Flask(__name__)


engine = create_engine('sqlite:///baseRotonde.db', echo=True)


connection = engine.connect()

@app.route('/test', methods=['GET','POST'])
def function():
    if request.method=='GET':
        return render_template('ajoutvaleur.html')
    if request.method=='POST':
        connection = engine.connect()
        connection.execute(places.insert(), [ {'date' :"mardi", "nomUser" : "Mickael"} ] )
        return redirect('/')

@app.route('/')
def logout():
  return 'Sauvegarde'

if __name__ == '__main__':
  app.run(debug=True)

connection.close()
