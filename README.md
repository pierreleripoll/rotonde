# Rotonde

Site de réservation de places à la Rotonde

:warning: IL FAUT SUPPRIMER VOTRE ANCIENNE DB ET CHAQUE FOIS QUE VOUS DEVEZ EN CRÉER UNE UTILISER LE SCRIPT `populate.py` :warning:

Si vous avez des modifs à faire dans la db faîtes les dans le script pour que tout le monde les ait.

# TODO

- [ ] rendre clean le css (bootstrap commun pour tout le monde)
- [x] rendre clean le html (jinja2, extends, import...)
- [x] MATHILDE : mail de confirmation
- [ ] ARTHUR : gérer le dépassement de places (vérif côté serveur etc)
- [x] rajouter infos sur le spectacle
- [JN] rendre plus beau contact
- [ ] gestion des vignettes (trop grande, trop petite, mauvais format)
- [ ] image par déf
- [ ] gestion des dates à modifier (#firefox not working...)
- [ ] interface pour spectacle | gestion spectacle
- [ ] PIERRE : mode super admin / admin -> contact email, UTILISER FLASK SESSION/ADMIN/USER ?
- [ ] calendrier a faire
- [ ] site de paiement (utiliser Stripe ?)
- [x] gérer la reservation dans la base de données -> places insérées dans la BD
- [x] actualiser le nombre de places restantes lors de l'ajout de places
- [x] Faire la page html d'acceuil avec défilement des spectacles et redirection vers page spectacle, (spectacle en argument)
- [x] Faire page html spectacle qui prend en argument un spectacle (objet déjà créer dans model.py), l'affiche et présente des dates possibles en bas de pages
- [ ] Utiliser bootstrap dans calendrier ?
- [x] Valider le panier -> (paiement ?) + rajout dans db -> il faut actualiser le nombre de places restantes
- [x] Remplir le panier -> dans la session on ajoute des places en faisant session.append["places"](place)




Vous pouvez ajouter les TODOs ici ! ;)

# QUIFAITQUOI
## Pierre
 - Il faut pouvoir préciser les dates des spectacles

## Mathilde
 - Remplissage de la BD lors de la validation du panier

## Arthur
- Bootstrap calendrier



# Questions sur le projet

## Antoine

- Les champs de `calendrier` ne pourraient-ils pas être intégrés à la table `spectacle` ?
- Ajouter `prix` dans la table `spectacle` ?
- Avoir un champ `id` dans spectacle comme clé principale plutôt que `nom` ?
- Avoir la table place liée à un nom et un spectacle, mais laisser date heure et tout dans spectacle ?
- truc sur le nombre or something

## Jean-Nicolas

## Mathilde

## Pierre

- Quelqu'un peut-il m'expliquer pourquoi Antoine vient m'emmerder en PRS ? Merci d'avance

---

Vous pouvez ajouter vos questions ici ! ;)
