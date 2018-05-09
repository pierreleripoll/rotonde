from flask import *
from flask import current_app as app
from sqlalchemy import *
from sqlalchemy.sql import *
from werkzeug.utils import secure_filename
import os
import re
from model import*
from jinja2 import TemplateNotFound

admin_relative = Blueprint('admin_relative', __name__,
                        template_folder='templates',static_folder = 'static')

## PAGE ADMIN
@admin_relative.route('/admin', methods=['GET','POST'])
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
                return redirect(url_for('gestion_spectacle.set_spectacle',nomSpectacle='nouveauSpectacle'))
            if request.form["bouton"]=="showPlaces":
                return redirect(url_for('admin_relative.show_places'))

    else :
        return redirect(url_for('admin_relative.admin_log'))


@admin_relative.route('/places',methods=['GET'])
def show_places():
    if 'admin' in session:
        places = get_all_places()
        return render_template('show_places.html',places=places)
    else:
        return redirect(url_for('logout'))

## LOGIN ADMIN
@admin_relative.route('/admin_log', methods=['GET','POST'])
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

        return redirect(url_for('admin_relative.admin'))
