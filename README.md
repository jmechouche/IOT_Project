# Projet IOT

## Cours IOT M2 ASTRA

## Broker Mqtt
Le projet se reposant integralement sur Mqtt il est nécessaire d'avoir un broker mqtt comme mosquitto qui fonctionne

## Serveur Python
Pour demarrer le serveur python il suffit de ce placer dans le dossier du projet puis d'executer la commande suivante
  python SmartHome/core.py
Attention si le broker Mqtt n'est pas hébergé en local il faudra changer la valeur de la variable IP_BROKER et renseigner l'adresse IP du broker

## Serveur Web
Pour lancer le serveur Web, il faut avoir installer django et lancer la commande suivante dans le repertoire du projet:
  python manage.py runserver
Les deux pages web sont accessibles via les deux liens suivants:
http://{IP}/LedManager/accueil
http://{IP}/LedManager/LedManage
