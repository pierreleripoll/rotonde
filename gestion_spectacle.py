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
    thisSpectacle = get_spectacle(nomSpectacle)
    thisDates = get_dates(nomSpectacle)
    if request.method=="GET":
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
        if request.form["submit"] == "modify" and session['pseudo'] == thisSpectacle.admin:
            return redirect(url_for('gestion_spectacle.set_spectacle',nomSpectacle=nomSpectacle))
        if request.form["submit"] == "valider" :
            print(request.form)
            if not 'panier' in session :
                session['panier'] = []
            places = session['panier']
            for date in request.form :
                try:
                    n = int(request.form[date])
                    if n> 0 :
                        print("Add a place !")
                        for i in range(n):
                            place = Place(nomSpectacle=nomSpectacle,date=date,nomUser="")
                            placeJSON = place.serialize()
                            print(placeJSON)
                            places.append(place.serialize())
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
            thisContact = get_contact()
            for calendrier in thisDates:
                calendrier.date = datePytoHTML(calendrier.date)
            print(thisDates)
            if thisSpectacle.admin == session['pseudo'] or session['admin']=="super":
                return render_template('set_spectacle.html',spectacle = thisSpectacle,dates=thisDates,nDates = len(thisDates),contact=thisContact, maxsize=app.config['MAX_CONTENT_LENGTH'])
            else:
                return abort(403);
        if request.method=="POST":
            if request.form["nom"] != "":

                cont = request.form
                print("\n\n"+ str(cont) +"\n\n")
                spectacle = Spectacle(nom=cont["nom"],resume=cont["resume"],liens =cont["liens"],admin=session['pseudo'],photos=0,
                    directeur=cont["directeur"],auteur=cont["auteur"],participants=cont["participants"],infoComplementaire=cont["infoComplementaire"],tarif=cont["tarif"],
                    duree=cont["duree"],typeSpectacle=cont["typeSpectacle"])
                print("\n\n"+ str(cont) +"\n\n")
                alreadyIn = get_spectacle(spectacle.nom)
                if alreadyIn:
                    if not( alreadyIn.admin == session['pseudo'] or session['admin']=="super"):
                        return abort(403)
                    spectacle.photos = alreadyIn.photos
                # check if the post request has the file part
                if 'photos' not in request.files:
                    print("No photo")
                else:
                    print("There is photos :")
                    name = urlify(spectacle.nom)
                    pathUpload = app.config['UPLOAD_FOLDER']+'/'+name
                    if not os.path.isdir(pathUpload):
                        os.mkdir(pathUpload)
                    numberPhotos = spectacle.photos
                    for f in request.files.getlist('photos'):
                        print(f.filename)
                        # if user does not select file, browser also
                        # submit a empty part without filename
                        if f.filename == '':
                            flash('No selected file')
                        if f and allowed_file(f.filename):
                            filename = secure_filename(f.filename)
                            f.save(os.path.join(pathUpload, urlify(spectacle.nom)+"_"+str(numberPhotos)))
                            numberPhotos +=1
                    spectacle.photos=numberPhotos
                if alreadyIn :
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
                db.session.commit();
                return redirect(url_for('gestion_spectacle.spectacle',nomSpectacle=request.form["nom"]))
            else :
                return redirect(url_for('gestion_spectacle.set_spectacle',nomSpectacle="nouveauSpectacle"))
    else :
        return abort(403)

@gestion_spectacle.route('/api/ajoutContact/<string:nomUser>/<string:prenomUser>/<int:tel>/<string:mail>/<int:anneeSelect>/<string:departSelect>')
def ajoutContact(nomUser, prenomUser, tel, mail, anneeSelect, departSelect):
    contact = Contact(nom=nomUser,prenom=prenomUser,telephone=tel,adresseMail=mail,annee=anneeSelect, depart=departSelect)
    insert_contact(contact)
    return jsonify(nom = nomUser, prenom = prenomUser, an = anneeSelect, dep = departSelect, id = getID_contact(nomUser, prenomUser))
