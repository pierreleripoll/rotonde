# -*- coding: utf-8 -*-

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
from datetime import datetime
import re
from PIL import Image
import shutil

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
        photos = get_all_photos(thisSpectacle.nom)
        paths = get_paths_photos(thisSpectacle.nom)
        print("Paths :",paths)
        photoMain = get_photoSpectacle(thisSpectacle.nom,ordre=0);
        print("Voici toutes les photos : ",photos,"\net la photo principale :" ,photoMain, "\n et sa couleur : ", photoMain.colors);
        return render_template('spectacle.html',spectacle = thisSpectacle,dates = thisDates,paths = paths,photos = photos)
    if request.method == "POST":
        if request.form["submit"] == "modify" and session['pseudo'] == thisSpectacle.admin:
            return redirect(url_for('gestion_spectacle.set_spectacle',nomSpectacle=nomSpectacle))
        if request.form["submit"] == "delete" and session['pseudo'] == thisSpectacle.admin:
            delete_spectacle(nomSpectacle)
            return redirect(url_for('logout'))
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

            if nomSpectacle == "nouveauSpectacle" or thisSpectacle.admin == session['pseudo'] or session['admin']=="super" :
                thisDates = get_dates(nomSpectacle)
                photos = []
                if nomSpectacle != "nouveauSpectacle":
                    photos = get_all_photos(nomSpectacle)
                    print("Set spectacle : ",photos)
                thisContact = get_contact()
                for calendrier in thisDates:
                    calendrier.date = calendrier.date.strftime('%d/%m/%Y %H:%M')
                print(thisDates)

                return render_template('set_spectacle.html',photos=photos,spectacle = thisSpectacle,dates=thisDates,nDates = len(thisDates),contact=thisContact, maxsize=app.config['MAX_CONTENT_LENGTH'], type=session['admin'])
            else:
                return abort(403);
        if request.method=="POST":
            if request.form["button"] == "valider":
                if request.form["nom"] != "":
                    cont = request.form
                    print("\n\n"+ str(cont) +"\n\n")
                    spectacle = Spectacle(nom=cont["nom"],resume=cont["resume"],liens =cont["liens"],admin=session['pseudo'],photos=0,
                        directeur=cont["directeur"],auteur=cont["auteur"],participants=cont["participants"],infoComplementaire=cont["infoComplementaire"],tarif=cont["tarif"],
                        duree=cont["duree"],typeSpectacle=cont["typeSpectacle"], idContact=cont["ajoutContactDB"])
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

                    delete_date(nomSpectacle)
                    for dates in cont:
                        if "datetime" in dates:
                            # strDate = cont[dates];
                            # print(strDate)
                            # strDate = strDate[0:len(strDate)-3]
                            datePy = datetime.strptime(cont[dates], '%d/%m/%Y %H:%M')
                            date = Calendrier(date=datePy,nom=cont["nom"],placesRestantes=int(cont["nPlaces"+str(re.findall(r'\d+', dates)[0])]))
                            alreadyIn = "false"
                            insert_date(date)
                    db.session.commit();
                    return redirect(url_for('gestion_spectacle.spectacle',nomSpectacle=request.form["nom"]))
                else :
                    return redirect(url_for('gestion_spectacle.set_spectacle',nomSpectacle="nouveauSpectacle"))
        if request.form["button"]=="delete_spectacle":
            delete_spectacle(nomSpectacle)
            return redirect(url_for('logout'))
    else :
        return abort(403)

@gestion_spectacle.route('/api/ajoutContact/<string:nomUser>/<string:prenomUser>/<int:tel>/<string:mail>/<int:anneeSelect>/<string:departSelect>',methods=['POST'])
def ajoutContact(nomUser, prenomUser, tel, mail, anneeSelect, departSelect):
    if 'admin' in session:
        if mail == " ":
            mail = ""
        if tel == 0:
            contact = Contact(nom=nomUser,prenom=prenomUser,adresseMail=mail,annee=anneeSelect, depart=departSelect)
            insert_contact(contact)
            return jsonify(nom = nomUser, prenom = prenomUser, an = anneeSelect, dep = departSelect, id = getID_contact(nomUser, prenomUser))
        else :
            contact = Contact(nom=nomUser,prenom=prenomUser,telephone=tel,adresseMail=mail,annee=anneeSelect, depart=departSelect)
            insert_contact(contact)
            return jsonify(nom = nomUser, prenom = prenomUser, an = anneeSelect, dep = departSelect, id = getID_contact(nomUser, prenomUser))
    else:
        return abort(401)


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
            pathOriginal = os.path.join(pathUpload+'originals/',filename)
            if os.path.exists("."+pathOriginal):
                os.remove("."+pathOriginal)
            os.remove("."+pathPhoto)

            print("Spectacle.photos :",spectacle.photos)


            photo = get_photo(pathPhoto)

            id = photo.id
            print("lol")
            colors = get_all_colors(id)
            print(colors);
            for color in colors:
                delete(color)
            colors = get_all_colors(id)
            print(colors);
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
            if not os.path.isdir("."+pathUpload+'/originals'):
                os.mkdir("."+pathUpload+"/originals")
            print("Spectacle.photos :",spectacle.photos)
            print(request.files)

            f = request.files['photos']
            numero = -1
            nomFichier = secure_filename(f.filename)
            path = os.path.join(pathUpload,nomFichier)
            f.save("."+path)
            print("Path :",path)
            pathOriginal = os.path.join(pathUpload,"originals",nomFichier)
            print("Path original :",pathOriginal)
            shutil.copyfile("."+path,"."+pathOriginal)

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
            'append': 'true',
            'id':photo.id
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


@gestion_spectacle.route('/api/changeOrder/<string:nomSpectacle>/<int:oldIndex>/<int:newIndex>/',methods=["POST"])
def changeOrder(nomSpectacle,oldIndex,newIndex):
    print(nomSpectacle,oldIndex,newIndex)
    photos= get_all_photos(nomSpectacle);
    photos[oldIndex].ordre = -1
    print(photos)
    for photo in photos:
        if photo.ordre > oldIndex:
            photo.ordre-=1
        if photo.ordre >= newIndex:
            photo.ordre+=1
        print(photo)

    photos[oldIndex].ordre=newIndex;
    print(photos)
    db.session.commit()
    return "fine"

@gestion_spectacle.route('/api/crop/<string:nomSpectacle>/<int:id>/',methods=["POST"])
def crop(nomSpectacle,id):
    print("CROP ",nomSpectacle,id)
    print(request.form)
    form = request.form
    photo = get_photo_byid(id)
    photo.width = int(form['w'])
    photo.height = int(form['h'])
    photo.x = int(form['x'])
    photo.y = int(form['y'])
    photo.scale = float(form['scale'])
    update_photo(photo)
    print(photo.path)
    pathSplit = photo.path.split('/')
    pathCropped =photo.path
    pathOriginal = pathCropped.replace(pathSplit[-1],'originals/'+pathSplit[-1])
    img = Image.open("."+pathOriginal)
    W, H = img.size
    newSize = (int(W*photo.scale),int(H*photo.scale))
    print("Original :",pathOriginal)
    print("Cropped :",pathCropped)
    s = 1/photo.scale
    area=(int(s*photo.x),int(s*photo.y),int(s*(photo.x+photo.width)),int(s*(photo.y+photo.height)))
    cropped_img = img.crop(area)
    cropped_img.save("."+pathCropped,quality=90)

    return "fine"

@gestion_spectacle.route('/api/uploadColor/<int:id>/<string:hex>/<int:bool>/',methods=['POST'])
def uploadColor(id,hex,bool):
    test = get_color(hex,id);
    color = Color(hexa=hex,idPhoto=id,actif=bool);
    photo = get_photo_byid(id);

    if(bool==1):
        set_active_colors(id,hex)
    else:
        if(test is None):
            print("elles sont différentes");
            insert_color(color)
        else:
            print("couleur déjà registered pour cette image")

    return "niquel chrome";
