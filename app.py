from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *
from werkzeug.utils import secure_filename
import os
import re
from model import*
from gestion_spectacle import *

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
app.secret_key = 'iswuygdedgv{&75619892__01;;>..zzqwQIHQIWS'
app.register_blueprint(gestion_spectacle)


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
            return redirect(url_for('panier'))
        elif request.form["bouton"] == "calendrier" :
            print("calendrier")
            return redirect(url_for('calendrier'))
        elif request.form["bouton"] == "admin":
            print("admin")
            return redirect(url_for('admin'))
        else :
            return redirect(url_for('lougout'))


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
                return redirect(url_for('logout'))
            if request.form["bouton"]=="create":
                return redirect(url_for('set_spectacle',nomSpectacle='nouveauSpectacle'))

    else :
        return redirect(url_for('admin_log'))

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

        return redirect(url_for('admin'))

## CALENDRIER
@app.route('/calendrier', methods=['GET'])
def calendrier():
    return render_template('calendrier.html')

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
def panier():

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
