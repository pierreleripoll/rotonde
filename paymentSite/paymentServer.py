from flask import *
import requests

app = Flask(__name__)

## PAGE D'ACCUEIL
@app.route('/')
def homePage():
    return "Vous êtes sur le site de paiement"


## PAYMENT
@app.route('/payment/<string:idSite>/<string:idClient>/<string:mail>/<int:nbrPlace>/<int:cost>', methods=['GET','POST'])
def pageContact(idSite, idClient, mail, nbrPlace, cost):
    siteRotonde = "123456789"
    if request.method == "POST":
        form = request.form
        print(form)
        print("je suis dans le site avec :",idSite, idClient, nbrPlace, cost)
        return "cool"
    if request.method=="GET":
        if idSite == siteRotonde:
            form = []
            return render_template('paymentPage.html', nomSite="La Rotonde", idSite=idSite, idClient=idClient, mail=mail, places=nbrPlace, price=cost, cont=form)
        else :
            return abort(404)
    else:
        return abort(404)



if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5500, debug='true')
