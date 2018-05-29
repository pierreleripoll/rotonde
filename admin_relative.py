# -*- coding: utf-8 -*-

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
    #
    # if request.form["submit"] == "accueil":
    #     return redirect(url_for('logout'))
    # login = request.form["login"]
    if 'admin' in session :
        if request.method=='GET':
            admin=get_session(session['pseudo'])
            print(admin)
            return render_template('admin.html',admin=admin)
        if request.method=='POST':
            if request.form["bouton"]=="logout":
                session.pop("pseudo",None)
                session.pop("admin",None)
                session.clear()
                return redirect(url_for('logout'))
            if request.form["bouton"]=="createspectacle":
                return redirect(url_for('gestion_spectacle.set_spectacle',nomSpectacle='nouveauSpectacle'))
            if request.form["bouton"]=="showPlaces":
                return redirect(url_for('admin_relative.show_places'))
            if request.form["bouton"]=="accueil":
                return redirect(url_for('logout'))
            if request.form["bouton"]=="createadmin":
                return redirect(url_for('admin_relative.set_admin',login="nouveladmin"))
            if request.form["bouton"]=="adminlist":
                return redirect(url_for('admin_relative.adminlist'))
            if request.form["bouton"]=="modifySelf":
                return redirect(url_for('admin_relative.set_admin', login=session['pseudo']))

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

        if request.form["submit"] == "accueil":
            return redirect(url_for('logout'))
        login = request.form["login"]

        sessions = get_sessions()

        password = request.form["password"]

        for sess in sessions :
            if login == sess.login and sess.validate_password(password):
                welcomeString = "WELCOME "+login.upper()
                print("\n\n")
                print(len(welcomeString)*'*')
                print(welcomeString)
                print(len(welcomeString)*'*')
                print("\n\n")
                session['pseudo']=sess.login
                session['admin']=sess.typeAdmin
                print(session)

        return redirect(url_for('admin_relative.admin'))

@admin_relative.route('/set_admin/<login>', methods=['GET','POST'])
def set_admin(login):
    if session['admin']=="super" or session['pseudo']==login:
        if request.method=="GET":
            print(login)
            sessionAdmin=get_session(login)
            thisContact=get_contact()
            if login=="nouveladmin" or sessionAdmin.typeAdmin=="normal" or sessionAdmin.typeAdmin=="super":
                return render_template('set_admin.html', admin=sessionAdmin, contact=thisContact, type=session['admin'])
            else:
                return abort(403)

        if request.method=="POST":
            if request.form["login"] != "" and request.form["password"] != "":

                cont = request.form
                print("\n\n"+ str(cont) +"\n\n")
                admin = Session(login=cont["login"],password=cont["password"],typeAdmin =cont["admintype"], idContact=cont["ajoutContactDB"])
                print("\n\n"+ str(cont) +"\n\n")
                alreadyIn = get_session(admin.login)
                if alreadyIn:
                    print("\nSESSION ALREADY IN\n")
                    if not(session['admin']=="super"):
                        print("\n\nNOT ALLOWED MODIFY THIS SPECTACLE\n\n")
                        return abort(403)
                    print("CALL update_session")
                    update_session(admin)
                else:
                    insert_session(admin)
                db.session.commit();
                return redirect(url_for('admin_relative.admin'))
            else :
                return redirect(url_for('admin_relative.set_admin',login="nouveladmin"))
    else :
        return abort(403)

@admin_relative.route('/adminlist', methods=['GET','POST'])
def adminlist():
    if session['admin']=="super":
        if request.method=="GET":
            admins=get_all_admins()
            return render_template('adminlist.html', admins=admins)
    else :
        return abort(403)
