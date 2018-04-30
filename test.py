
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


engine = create_engine('sqlite:////tmp/base.db', echo=True)

connection=engine.connect()

@app.route('/test', methods=['GET','POST'])
def function():
    if request.method=='GET':
        return render_template('ajoutvaleur.html')
    if request.method=='POST':
        a=0
        #connection.execute.append(request.form['post'])
        return redirect('/')

@app.route('/')
def logout():
  return 'Sauvegarde'

if __name__ == '__main__':
  app.run(debug=True)

connection.close()
