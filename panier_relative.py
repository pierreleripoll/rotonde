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

            return render_template("panier.html", display_cart = items, total = 10)
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
