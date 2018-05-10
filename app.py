from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *
from werkzeug.utils import secure_filename
import os
import re
from model import*
from gestion_spectacle import *
from panier_relative import *
from admin_relative import *

UPLOAD_FOLDER = './static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
app.secret_key = 'iswuygdedgv{&75619892__01;;>..zzqwQIHQIWS'

app.register_blueprint(gestion_spectacle)
app.register_blueprint(panier_relative)
app.register_blueprint(admin_relative)

#PAGE DE TEST JAVASCRIPT
@app.route('/javascript')
def javascript():
    return render_template('testJS.html')


## PAGE D'ACCUEIL
@app.route('/', methods=['GET','POST'])
def logout():
    print("\nSession en cours : \n",session,"\n")
    NomsSpectacles = []
    spectacles = get_spectacles()

    for spectacle in spectacles:
        NomsSpectacles.append(spectacle.nom)

    if request.method=='GET':
        return render_template('accueil.html', names=NomsSpectacles)
    if request.method=='POST':
        if request.form["bouton"] == "panier" :
            print("panier")
            return redirect(url_for('panier_relative.panier'))
        elif request.form["bouton"] == "calendrier" :
            print("calendrier")
            return redirect(url_for('calendrier'))
        elif request.form["bouton"] == "admin":
            print("admin")
            return redirect(url_for('admin_relative.admin'))
        else :
            return redirect(url_for('lougout'))



@app.route('/empty_cart')
def empty_cart():
    if 'panier' in session :
        session.pop('panier')
    return redirect(url_for('panier_relative.panier'))


## CALENDRIER
@app.route('/calendrier', methods=['GET','POST'])
def calendrier():
	dates= get_all_dates();
	if request.method=="GET":
		return render_template('calendrier.html',dates=dates)
	else:
		if not 'panier' in session:
			session['panier'] =[]
		places = session['panier']
		for date in dates:
			try:
				n=int(request.form[str(date.date)])
				if n>0:
					place = Place(date.nom,"",date.date,n)
					print("Place added", place.__dict__)
					places.append(place.__dict__)
			except ValueError:
				print("it's a string", request.form[str(date.date)])
				pass

		session['panier']=places
	return redirect ("/panier")

## SHOW UPLOADS FILES
@app.route('/uploads/<nomSpectacle>', methods=['GET'])
def uploads(nomSpectacle):

    if 'admin' in session:
        if request.method=="GET":
            path = app.config['UPLOAD_FOLDER']+'/'+urlify(nomSpectacle)
            if not os.path.isdir(path) :
                print(path+" is not a dir")
                return abort(404)
            else:
                paths = []
                for fileName in os.listdir(path):
                    paths.append('.'+path+'/'+fileName)
                print("Paths :",paths)
                return render_template('uploaded.html',paths = paths)
    else :
        return abort(403)




if __name__ == '__main__':
    app.run(debug='true')
    #app.run(host="192.168.43.6",port=2000)
