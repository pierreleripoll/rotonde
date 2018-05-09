from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *
from werkzeug.utils import secure_filename
import os
import re
from model import*
from gestion_spectacle import *
from panier_relative import *
from admin_relative import *

UPLOAD_FOLDER = './static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
app.secret_key = 'iswuygdedgv{&75619892__01;;>..zzqwQIHQIWS'

app.register_blueprint(gestion_spectacle)
app.register_blueprint(panier_relative)
app.register_blueprint(admin_relative)


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
            return redirect(url_for('panier_relative.panier'))
        elif request.form["bouton"] == "calendrier" :
            print("calendrier")
            return redirect(url_for('calendrier'))
        elif request.form["bouton"] == "admin":
            print("admin")
            return redirect(url_for('admin_relative.admin'))
        else :
            return redirect(url_for('lougout'))




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




if __name__ == '__main__':
    app.run(debug='true')
    #app.run(host="192.168.43.6",port=2000)
