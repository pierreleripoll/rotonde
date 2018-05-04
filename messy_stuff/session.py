from flask import *

app = Flask(__name__)
app.secret_key = 'iswuygdedgv{&75619892__01;;>..zzqwQIHQIWS'

@app.route("/")
def index():
    """This is the 'cover' page"""
    return render_template("index.html")

@app.route("/calendrier")
def list_shows():
    """This is the big page showing all the shows"""
    return render_template("calendrier.html")

@app.route("/spectacle/<int:id>")
def show_show(id):
    """This page shows the details of a given show, as well as giving an
    option to buy a seat."""
    return render_template("spectacle.html",
                  show_id = id)

@app.route("/cart")
def shopping_cart():

    """TODO: Display the contents of the shopping cart."""

    if "cart" not in session:
        # flash("There is nothing in your cart.")
        return render_template("cart.html", display_cart = {}, total = 0)
    else:
        items = session["cart"]
        dict_of_shows = {}

        total_price = 0
        for item in items:
            # TODO: implementer ci-dessous
            # show = model.get_show_by_id(item)
            total_price += 1
            if show in dict_of_seats:
                dict_of_seats[show]["qty"] += 1
            else:
                dict_of_seats[show] = {"qty":1, "name": "spectacle" + show, "price": 1}

        return render_template("cart.html", display_cart = dict_of_seats, total = total_price)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):


    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(id)

    flash("Successfully added to cart!")
    return redirect("/cart")

if __name__ == '__main__':
  app.run(debug=True)
