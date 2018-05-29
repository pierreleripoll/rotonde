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

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

panier_relative = Blueprint('panier_relative', __name__,template_folder='templates',static_folder = 'static')


def sendMail (adressedest, cart, nomUser):

	mailrotonde="rotondeinsatest@gmail.com"
	mdprotonde="motdepasse1!"
	fromaddr = mailrotonde

	toaddr = adressedest
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Reservation spectacle"

	html= render_template("mail.html", nomUser=nomUser, places=cart)
	msg.attach(MIMEText(html, 'html'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "motdepasse1!")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()


def isInCart(item, cart):
	for idx, show in enumerate(cart):
		if item['nomSpectacle'] == show['nomSpectacle'] and item['date'] == show['date']:
			return idx
	return -1

def calculCart(items):
	print("entering calculCart with items = "+str(items))
	display_cart = []
	taille=1
	for item in items:
		idx = isInCart(item,display_cart)
		if idx == -1 or display_cart == []:
			date = get_date(date=dateJSONToPy(str(item['date'])))
			#print(date)
			getPrice=get_spect_price(item['nomSpectacle'])
			left = date.placesRestantes
			display_cart.append({'nomSpectacle' : item['nomSpectacle'], 'date':item['date'], 'qte' : 1, 'left' : left, 'price':getPrice, 'taille':taille})
			taille += 1
		else:
			display_cart[idx]['qte']+=1
	return display_cart

def lenCart(cart):
	taille = 0
	for car in cart:
		if car['taille'] > taille:
			taille = car['taille']
	return taille

def udpateQte(cont):
	global display_cart
	for i, show in enumerate(display_cart):
		index = 'qte'+str(i+1)
		toDelete = []
		change = int(cont[index]) - int(show['qte'])
		print(change)
		print(str(cont[index]) +" - "+ str(show['qte'])+" = "+str(change))
		if(change ==0):
			print("non changed")
		else:
			while (change != 0):
				if(change < 0):
					for j, place in enumerate(session['panier']):
						if place['nomSpectacle'] == show['nomSpectacle'] and place['date'] == show['date']:
							#print("on supprime une des places : "+place['nomSpectacle'] + " " + place['date'] +" "+ str(j))
							session['panier'].pop(j)
							change += 1
							break
				else:
					place = Place(nomSpectacle=show['nomSpectacle'],date=show['date'],nomUser="", valide=0)
					placeJSON = place.serialize()
					print("on ajoute une places : "+str(placeJSON))
					session['panier'].append(placeJSON)
					change -= 1
	print("voici le panier de la session : "+ str(session['panier']))
	session.update()



## PANIER
@panier_relative.route('/panier', methods=['POST','GET'])
def panier():
	if "panier" not in session:
		return render_template("panier.html", display_cart = {}, len=0)

	global display_cart
	display_cart = calculCart(session['panier'])
	if request.method == "GET":
		"""TODO: Display the contents of the shopping cart."""
		print("\n\n\n\n\n\n\n\nEntering in GET\n\n\n\n\n\n\n\n\n");

		if "panier" not in session:
			return render_template("panier.html", display_cart = {}, len=0)

		else:
			return render_template("panier.html", display_cart = display_cart, len=lenCart(display_cart))
	if request.method == "POST":
		print("\n\n\n\n\n\n\n\nEntering in POST\n\n\n\n\n\n\n\n\n");
		if "panier" not in session :
			return redirect(url_for('logout'))
		else:
			if request.form['foo']=='valider':
				cont = request.form
				print("\n\n\n\n"+str(cont)+"\n\n\n\n")
				print(display_cart)
				udpateQte(cont);
			if 'nom' not in request.form or request.form['nom'] == "":
				return redirect(url_for('panier_relative.panier'))
			else:
				print("on m'appelle")
				panier = session['panier']
				print(panier)
				name = request.form['nom']
				mail = request.form['mail']
				display_cart = calculCart(session['panier'])
				for show in display_cart:
					print("requesting date")
					date = dateJSONToPy(str(show['date']))
					added=0
					datemodif=get_date(date=date)
					for i in range(1, show['qte']+1):
						added+=1
						print(i)
						place = Place(ordre=added,nomSpectacle=show['nomSpectacle'],nomUser=name,date=date, adresseMail=mail, valide=0)
						insert_place(place)
					res=update_placesRestantes(datemodif,added)
					if(res==-1):
						return redirect(url_for('panier_relative.panier'))
				session.pop('panier')
				places=get_places_mail(mail)
				sendMail(mail, places, name)
			return redirect(url_for('logout'))

@panier_relative.route('/panier/<string:idSite>/<string:idClient>/<string:mail>/<int:nbrPlace>/<int:cost>/<string:token>', methods=['GET', 'POST'])
def gestion_panier(idSite, idClient, mail, nbrPlace, cost, token):
	if token == "invalidate":
		return redirect(url_for('panier_relative.panier'))
	elif token == "token":
		#cont = request.form
		#cont = []
		#udpateQte(cont);
		panier = session['panier']
		name = idClient
		mail = mail
		display_cart = calculCart(session['panier'])
		for show in display_cart:
			print("requesting date")
			date = dateJSONToPy(str(show['date']))
			added=0
			datemodif=get_date(date=date)
			for i in range(1, show['qte']+1):
				added+=1
				print(i)
				place = Place(ordre=added,nomSpectacle=show['nomSpectacle'],nomUser=name,date=date, adresseMail=mail)
				insert_place(place)
			res=update_placesRestantes(datemodif,added)
			if(res==-1):
				return redirect(url_for('panier_relative.panier'))
		session.pop('panier')
		places=get_places_mail(mail)
		sendMail(mail, places, name)
		return redirect(url_for('logout'))
	else:
		return abort(404)
