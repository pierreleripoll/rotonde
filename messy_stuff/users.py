from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *

app = Flask(__name__)

engine = create_engine('sqlite:///mabase.db', echo=True)

metadata = MetaData()

users = Table('users', metadata,
            Column('id', Integer, autoincrement=True, primary_key=True),
            Column('name', String))

emails = Table('emails', metadata,
            Column('id', Integer, autoincrement=True, primary_key=True),
            Column('uid', None, ForeignKey('users.id')),
            Column('email', String, nullable=False))

metadata.create_all(engine)
connection = engine.connect()

u_ins = users.insert()
connection.execute(u_ins.values(name="Roger"))

@app.route('/test', methods=['GET','POST'])
def function():
    if request.method=='GET':
        return render_template('ajoutvaleur.html')
    if request.method=='POST':
        print("HELLLO")
        connection = engine.connect()
        connection.execute(users.insert() , [ {"name" : request.form["foo"]}] )
        return redirect('/')

@app.route('/')
def logout():
  return 'Sauvegarde'

if __name__ == '__main__':
  app.run(debug=True)


connection.close()
