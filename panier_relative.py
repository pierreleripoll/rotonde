from flask import *
from flask import current_app as app
from sqlalchemy import *
from sqlalchemy.sql import *
from werkzeug.utils import secure_filename
import os
import re
from model import*
from jinja2 import TemplateNotFound

panier_relative = Blueprint('panier_relative', __name__,
                        template_folder='templates',static_folder = 'static')

def isInCart(item, cart):
    for idx, show in enumerate(cart):
        if item['nomSpectacle'] == show['nomSpectacle'] and item['date'] == show['date']:
            print(item['nomSpectacle'] + " est dans la carte à la place "+str(idx))
            return idx
    return -1

def calculCart(items):
    display_cart = []
    for item in items:
        idx = isInCart(item,display_cart)
        if idx == -1 or display_cart == []:
            print("il est pas dedans !")
            display_cart.append({'nomSpectacle' : item['nomSpectacle'], 'date':item['date'], 'qte' : 1})
        else:
            display_cart[idx]['qte']+=1
    return display_cart
## PANIER
@panier_relative.route('/panier', methods=['GET','POST'])
def panier():
    if request.method == "GET":
        """TODO: Display the contents of the shopping cart."""


        if "panier" not in session:
            #flash("There is nothing in your cart.")
            return render_template("panier.html", display_cart = {}, total = 0)

        else:
            items = session["panier"]
            print("ITEMS\n",items)
            display_cart = calculCart(items)
            print(display_cart)
            # dict_of_places = {}
            #
            # total_price = 0
            #
            # for item in items:
            #     # place = get_place_by_id() #A modifier
            #     place = Place(item,'test','osef','osef',1)
            #     total_price += 1 # A modifier
            #     if place.idPlace in dict_of_places:
            #         dict_of_places[place.idPlace]["qty"] += 1
            #     else:
            #         dict_of_places[place.idPlace] = {"qty":1, "name": "spectacle" + str(place.idPlace), "price": 1}

            return render_template("panier.html", display_cart = display_cart, total = 10)
    if request.method == "POST":
        if "panier" not in session :
            return redirect(url_for('logout'))
        else:
            if 'nom' not in request.form or request.form['nom'] == "":
                return redirect(url_for('panier_relative.panier'))
            else:
                panier = session['panier']
                name = request.form['nom']
                for p in panier:
                    place = Place(p['nomSpectacle'],name,p['date'],p['nombre'])
                    insert_place(place)
                session.pop('panier')
                return redirect(url_for('logout'))


@panier_relative.route('/add_to_cart/<int:id>', methods=['POST','GET']) #Provisoire, enlever le get
def add_to_cart(id, ):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append(id)
    flash("Successfully added to cart!")
    return redirect("/panier")


    #
    # for i in idx:
    #     if item['date'] == display_cart[i]['date']:
    #         print("et à la même date donc on augmente la qte")
    #         display_cart[idx]['qte']+=1
    # else:
    #     print("la date est différente !")
    #     display_cart.append({'nomSpectacle' : item['nomSpectacle'], 'date':item['date'], 'qte' : 1})
