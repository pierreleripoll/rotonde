# -*- coding: utf-8 -*-

from flask import *
from werkzeug.utils import secure_filename
import os
import re
from model import *
from model import db
from gestion_spectacle import *
from panier_relative import *
from admin_relative import *

UPLOAD_FOLDER = '/static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baseRotonde.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['MAX_CONTENT_LENGTH'] =  1024 * 1024
app.secret_key = 'iswuygdedgv{&75619892__01;;>..zzqwQIHQIWS'
app.jinja_env.filters['urlify']=urlify

app.register_blueprint(gestion_spectacle)
app.register_blueprint(panier_relative)
app.register_blueprint(admin_relative)

app.jinja_env.filters['datetime'] = prettify_date

db.init_app(app)

@app.context_processor
def utility_processor():
    def niceUrl(s):
        return urlify(s)
    return dict(niceUrl=niceUrl)

@app.template_filter('mainPhoto')
def mainPhoto_filter(nom):
	spectacle = get_spectacle(nom)
	photo = spectacle.getPhoto(0)
	return photo.path

@app.template_filter('originalPhoto')
def originalPhoto_filter(path):
	pathSplit = path.split('/')
	return path.replace(pathSplit[-1],'originals/'+pathSplit[-1])


@app.template_filter('nameFromPath')
def nameFromPath_filter(path):
	return path.rsplit('/',1)[-1]

## PAGE D'ACCUEIL
@app.route('/', methods=['GET','POST'])
def logout():
	print("\nSession en cours : \n",session,"\n")

	NomsSpectacles = []
	spectacles = get_spectacles()


	if request.method=='GET':
		return render_template('accueil.html', spectacles=spectacles)
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
	else:
		return redirect(url_for('logout'))

@app.route('/how_to')
def how_to():
    return render_template('how_to.html')

## CALENDRIER
@app.route('/calendrier', methods=['GET','POST'])
def calendrier():
	dates= get_all_dates();
	if request.method=="GET":
		return render_template('calendrier.html',dates=dates)
	if request.method=="POST":
		if request.form["foo"]=="valider":
			if not 'panier' in session:
				session['panier'] =[]
			places = session['panier']
			for date in dates:
				try:
					n=int(request.form[str(date.date)])
					if n>0:
						for i in range (0,n):
							place = Place(nomSpectacle=date.nom,nomUser="",date=(date.date))
							placeJSON=place.serialize()
							print("Place added", placeJSON)
							places.append(placeJSON)
				except ValueError:
					print("it's a string", request.form[str(date.date)])
					pass
				session['panier']=places
		if request.form["foo"] == "accueil":
			return redirect(url_for('logout'))
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
	#app.run(debug='true')
	app.run(host="192.168.0.22",port=5000)
