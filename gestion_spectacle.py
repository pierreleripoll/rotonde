from flask import *
from flask import current_app as app
from sqlalchemy import *
from sqlalchemy.sql import *
from werkzeug.utils import secure_filename
from json import dumps
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

        paths = get_paths_photos(thisSpectacle.nom)
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
        if request.form["Color1"] != 0:
            print("wow it's working")
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

            if nomSpectacle == "nouveauSpectacle" or thisSpectacle.admin == session['pseudo'] or session['admin']=="super" :
                paths = []
                if nomSpectacle != "nouveauSpectacle":
                    photos = get_all_photos(nomSpectacle)
                    print("Set spectacle : ",paths)
                return render_template('set_spectacle.html',photos=photos,spectacle = thisSpectacle,dates=thisDates,nDates = len(thisDates),contact=thisContact, maxsize=app.config['MAX_CONTENT_LENGTH'])
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
                    print("\nSPECTACLE ALREADY IN\n")
                    if not( alreadyIn.admin == session['pseudo'] or session['admin']=="super"):
                        print("\n\nNOT ALLOWED MODIFY THIS SPECTACLE\n\n")
                        return abort(403)
                    spectacle.photos = alreadyIn.photos
                # check if the post request has the file part

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

@gestion_spectacle.route('/api/deleteFile/<string:nomSpectacle>/<string:filename>',methods=['POST'])
def deleteFile (nomSpectacle,filename):
    if 'admin' not in session :
        return abort(401)
    else :
        spectacle=get_spectacle(nomSpectacle)
        if session['pseudo']==spectacle.admin or session['admin']=='super':
            photos = get_all_photos(nomSpectacle)
            nomSpectacle = urlify(nomSpectacle)
            print ("spectacle"+nomSpectacle)
            pathUpload =app.config['UPLOAD_FOLDER']+'/'+nomSpectacle+'/'
            pathPhoto = os.path.join(pathUpload,filename)
            os.remove("."+pathPhoto)
            print("Spectacle.photos :",spectacle.photos)


            photo = get_photo(pathPhoto)

            for p in photos:
                if p.ordre>photo.ordre:
                    p.ordre -=1

            delete(photo)

            spectacle.photos -= 1
            db.session.commit()
            print(photos)
            dic = {"succes":"total"}
            return json.dumps(dic)
        else:
            return abort(401)

@gestion_spectacle.route('/api/uploadFile/<string:nomSpectacle>/',methods=['POST'])
def uploadFile (nomSpectacle):
    if 'admin' in session :
        spectacle=get_spectacle(nomSpectacle)

        if session['pseudo']==spectacle.admin or session['admin']=='super':

            nomSpectacle = urlify(nomSpectacle)
            print ("spectacle"+nomSpectacle)
            pathUpload =app.config['UPLOAD_FOLDER']+'/'+nomSpectacle+'/'

            if not os.path.isdir("."+pathUpload):
                os.mkdir("."+pathUpload)
            print("Spectacle.photos :",spectacle.photos)
            print(request.files)
            f = request.files['photos']
            numero = -1
            nomFichier = f.filename
            path = os.path.join(pathUpload,nomFichier)
            f.save("."+path)
            photo = Photo(path=path,size=os.path.getsize('.'+path),spectacle=spectacle.nom,ordre=spectacle.photos)
            insert_photo(photo)
            spectacle.photos +=1
            print("Number photos add, state :",spectacle.photos)

            print(request.form)
            print(request.files)
            db.session.commit()
            dic = {
            'initialPreview': [path],
            'initialPreviewConfig': [
              {'caption': nomFichier, 'size':str(photo.size),'filename': nomFichier,'url':'/api/deleteFile/'+spectacle.nom+'/'+nomFichier,'key': str(photo.ordre) },
            ],
            'initialPreviewThumbTags': [    ],
            'append': 'true'
            }
            return json.dumps(dic)

        else:
            return jsonify({
            'error': 'Not authentified',
            'errorkeys': [],
            'initialPreview': [],
            'initialPreviewConfig': [],
            'initialPreviewThumbTags': [    ],
            'append': 'false'
            })
    else:
        return jsonify({
        'error': 'Not authentified',
        'errorkeys': [],
        'initialPreview': [],
        'initialPreviewConfig': [],
        'initialPreviewThumbTags': [    ],
        'append': 'false'
        })


@gestion_spectacle.route('/api/changeOrder/<string:nomSpectacle>/<int:oldIndex>/<int:newIndex>/')
def changeOrder(nomSpectacle,oldIndex,newIndex):
    print(nomSpectacle,oldIndex,newIndex)
    photos= get_all_photos(nomSpectacle);
    photos[oldIndex].ordre = -1
    for photo in photos:
        change= 0
        if photo.ordre > oldIndex:
            change-=1
        if photo.ordre >= newIndex:
            change+=1
        photo.ordre += change

    photos[oldIndex].ordre=newIndex;
    db.session.commit()
    return "fine"

@gestion_spectacle.route('/api/uploadColor/<int:id>/<string:hex>/<int:bool>/')
def uploadColor(id,hex,bool):
    test = get_color(hex,id);
    color = Color(hexa=hex,photo=id,actif=bool);

    if(test is None):
        print("elles sont différentes");
        insert_color(color)
    else:
        print("couleur déjà registered pour cette image")

    return "niquel chrome";
