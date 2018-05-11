from flask import *
from flask import current_app as app
from sqlalchemy import *
from sqlalchemy.sql import *
from werkzeug.utils import secure_filename
import os
import re
from model import*
from jinja2 import TemplateNotFound

UPLOAD_FOLDER = './static/uploads'

gestion_spectacle = Blueprint('gestion_spectacle', __name__,
                        template_folder='templates',static_folder = 'static')

## SPECTACLE
@gestion_spectacle.route('/spectacle/<nomSpectacle>', methods=['GET','POST'])
def spectacle(nomSpectacle):
    if request.method=="GET":
        thisSpectacle = get_spectacle(nomSpectacle)
        thisDates = get_dates(nomSpectacle)
        print(thisDates)
        if thisSpectacle == None :
            return abort(404)
        path = app.config['UPLOAD_FOLDER']+'/'+urlify(nomSpectacle)
        paths = []
        if not os.path.isdir(path) :
            print(path+" no uploads dir for this spectacle")
        else:
            for fileName in os.listdir(path):
                paths.append('.'+path+'/'+fileName)
            print("Paths :",paths)
        return render_template('spectacle.html',spectacle = thisSpectacle,dates = thisDates,paths = paths)
    if request.method == "POST":
        if request.form["submit"] == "modify":
            return redirect(url_for('gestion_spectacle.set_spectacle',nomSpectacle=nomSpectacle))
        if request.form["submit"] == "valider":
            print(request.form)
            if not 'panier' in session :
                session['panier'] = []
            places = session['panier']
            for date in request.form :
                try:
                    n = int(request.form[date])
                    if n> 0 :
                        print("Add a place !")
                        place = Place(nomSpectacle,"",date,n)
                        print(place.__dict__)
                        places.append(place.__dict__)
                except ValueError:
                    print("its a string ",request.form[date])
                    pass
            session['panier']=places
            return redirect(url_for('gestion_spectacle.spectacle',nomSpectacle=nomSpectacle))

        if request.form["submit"] == "accueil":
            return redirect(url_for('logout'))
## MODIFY SPECTACLE
@gestion_spectacle.route('/set_spectacle/<nomSpectacle>', methods=['GET','POST'])
def set_spectacle(nomSpectacle):
    if 'admin' in session:
        if request.method=="GET":
            thisSpectacle = get_spectacle(nomSpectacle)
            thisDates = get_dates(nomSpectacle)
            for calendrier in thisDates:
                calendrier.date = datePytoHTML(calendrier.date)
            print(thisDates)
            return render_template('set_spectacle.html',spectacle = thisSpectacle,dates=thisDates,nDates = len(thisDates))
        if request.method=="POST":
            if "nom" in request.form :
                cont = request.form
                spectacle = Spectacle(nom=cont["nom"],resume=cont["resume"],liens =cont["liens"])
                # check if the post request has the file part
                if 'photos' not in request.files:
                    print("No photo")
                else:
                    print("There is photos :")
                    name = urlify(spectacle.nom)
                    pathUpload = app.config['UPLOAD_FOLDER']+'/'+name
                    if not os.path.isdir(pathUpload):
                        os.mkdir(pathUpload)
                    numberPhotos = 0
                    for f in request.files.getlist('photos'):
                        print(f.filename)
                        # if user does not select file, browser also
                        # submit a empty part without filename
                        if f.filename == '':
                            flash('No selected file')
                        if f and allowed_file(f.filename):
                            filename = secure_filename(f.filename)
                            f.save(os.path.join(pathUpload, filename))
                            numberPhotos +=1
                    spectacle.photos=numberPhotos
                if get_spectacle(spectacle.nom) :
                    update_spectacle(spectacle)
                else:
                    insert_spectacle(spectacle)

                nombrePlace = 1
                actualDates = get_dates(nomSpectacle)
                while "datetime"+str(nombrePlace) in cont :
                    datePy =dateHTMLtoPy(cont["datetime"+str(nombrePlace)])
                    date = Calendrier(date=datePy,nom=cont["nom"],placesRestantes=int(cont["nPlaces"+str(nombrePlace)]))
                    nombrePlace +=1
                    alreadyIn="false"
                    for actualDate in actualDates:
                        if datePy == actualDate.date:
                            update_date(date)
                            alreadyIn = "true"
                    if alreadyIn == "false":
                        insert_date(date)

                return redirect(url_for('gestion_spectacle.spectacle',nomSpectacle=request.form["nom"]))
    else :
        return abort(403)
