from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *
from werkzeug.utils import secure_filename
import os
import re
from model import*

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
app.secret_key = 'iswuygdedgv{&75619892__01;;>..zzqwQIHQIWS'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def urlify(s):

     # Remove all non-word characters (everything except numbers and letters)
     s = re.sub(r"[^\w\s]", '', s)

     # Replace all runs of whitespace with a single dash
     s = re.sub(r"\s+", '-', s)

     return s.lower()

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
            return redirect('/panier')
        elif request.form["bouton"] == "calendrier" :
            print("calendrier")
            return redirect('/calendrier')
        elif request.form["bouton"] == "admin":
            print("admin")
            return redirect('/admin')
        else :
            return redirect('/')


## PAGE ADMIN
@app.route('/admin', methods=['GET','POST'])
def admin():

    if 'admin' in session :
        if request.method=='GET':
            return render_template('admin.html',pseudo = session["pseudo"])
        if request.method=='POST':
            if request.form["bouton"]=="logout":
                session.pop("pseudo",None)
                session.pop("admin",None)
                session.clear()
                return redirect('/')
            if request.form["bouton"]=="create":
                return redirect('/set_spectacle/nouveauSpectacle')

    else :
        return redirect('/admin_log')

## LOGIN ADMIN
@app.route('/admin_log', methods=['GET','POST'])
def admin_log():

    if request.method=='GET':
        return render_template('admin_log.html')

    if request.method=='POST':

        sessions = get_sessions()

        login = request.form["login"]
        password = request.form["password"]

        for sess in sessions :
            if login == sess.login and password == sess.password:
                welcomeString = "WELCOME "+login.upper()
                print("\n\n")
                print(len(welcomeString)*'*')
                print(welcomeString)
                print(len(welcomeString)*'*')
                print("\n\n")
                session['pseudo']=login.upper()
                session['admin']="true"
                print(session)

        return redirect('/')

## CALENDRIER
@app.route('/calendrier', methods=['GET'])
def calendrier():
    return render_template('calendrier.html')

## SPECTACLE
@app.route('/spectacle/<nomSpectacle>', methods=['GET','POST'])
def spectacle(nomSpectacle):
    if request.method=="GET":
        thisSpectacle = get_spectacle(nomSpectacle)
        thisDates = get_dates(nomSpectacle)
        print(thisDates)
        if thisSpectacle == None :
            return abort(404)
        return render_template('spectacle.html',spectacle = thisSpectacle,dates = thisDates)
    if request.method == "POST":
        if request.form["submit"] == "modify":
            return redirect('/set_spectacle/'+nomSpectacle)

## MODIFY SPECTACLE
@app.route('/set_spectacle/<nomSpectacle>', methods=['GET','POST'])
def set_spectacle(nomSpectacle):
    if 'admin' in session:
        if request.method=="GET":
            thisSpectacle = get_spectacle(nomSpectacle)
            thisDates = get_dates(nomSpectacle)
            print(thisDates)
            return render_template('set_spectacle.html',spectacle = thisSpectacle)
        if request.method=="POST":
            if "nom" in request.form :
                cont = request.form
                spectacle = Spectacle(cont["nom"],cont["resume"],0 ,cont["liens"])
                # check if the post request has the file part
                if 'photos' not in request.files:
                    print("No photo")
                else:
                    print("There is photos :")
                    name = urlify(spectacle.nom)
                    pathUpload = app.config['UPLOAD_FOLDER']+'/'+name
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
                return redirect('/spectacle/'+request.form["nom"])
    else :
        return abort(403)

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

## PANIER
@app.route('/panier', methods=['GET'])
def shopping_cart():

    """TODO: Display the contents of the shopping cart."""

    if "cart" not in session:
        # flash("There is nothing in your cart.")
        return render_template("cart.html", display_cart = {}, total = 0)
    else:
        items = session["cart"]
        dict_of_places = {}

        total_price = 0

        for item in items:
            # place = get_place_by_id() #A modifier
            place = Place(item,'test','osef','osef',1)
            total_price += 1 # A modifier
            if place.idPlace in dict_of_places:
                dict_of_places[place.idPlace]["qty"] += 1
            else:
                dict_of_places[place.idPlace] = {"qty":1, "name": "spectacle" + str(place.idPlace), "price": 1}

        return render_template("cart.html", display_cart = dict_of_places, total = total_price)

@app.route("/add_to_cart/<int:id>", methods=['POST','GET']) #Provisoire, enlever le get par la suite
def add_to_cart(id):

    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(id)

    flash("Successfully added to cart!")
    return redirect("/panier")



if __name__ == '__main__':
    app.run(debug='true')
    #app.run(host="192.168.43.6",port=2000)
