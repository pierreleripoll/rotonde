from flask import *
from flask import current_app as app
from sqlalchemy import *
from sqlalchemy.sql import *
from werkzeug.utils import secure_filename
import os
import re
from model import*
from jinja2 import TemplateNotFound

panier = Blueprint('panier', __name__,
                        template_folder='templates',static_folder = 'static')

## PANIER
@panier.route('/panier', methods=['GET'])
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

@panier.route('/add_to_cart/<int:id>', methods=['POST','GET']) #Provisoire, enlever le get par la suite
def add_to_cart(id):

    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(id)

    flash("Successfully added to cart!")
    return redirect("/panier")

