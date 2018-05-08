from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *

import model

app = Flask(__name__)
app.secret_key = 'iswuygdedgv{&75619892__01;;>..zzqwQIHQIWS'


## PAGE D'ACCUEIL
@app.route('/', methods=['GET','POST'])
def logout():
    NomsSpectacles = []
    spectacles = model.get_spectacles()

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

    if 'pseudo' in session :
        if request.method=='GET':
            return render_template('admin.html',pseudo = session["pseudo"])
        if request.method=='POST':
            if request.form["bouton"]=="logout":
                session.pop("pseudo",None)
                session.pop("login",None)
                session.pop("password",None)
            return redirect('/')
    else :
        return redirect('/admin_log')

## LOGIN ADMIN
@app.route('/admin_log', methods=['GET','POST'])
def admin_log():

    if request.method=='GET':
        return render_template('admin_log.html')

    if request.method=='POST':

        sessions = model.get_sessions()

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
                session['root']="true"

        return redirect('/')

## CALENDRIER
@app.route('/calendrier', methods=['GET'])
def calendrier():
    return render_template('calendrier.html')


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
            # place = model.get_place_by_id() #A modifier
            place = model.Place(item,'test','osef','osef',1)
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
