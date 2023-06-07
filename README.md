---
authors: Ruben Rouvière, Louis Maronne
date: 2023-06-07
---
# Eggco

Ruben Rouvière, Louis Maronne

## Documentation technique

La solution logicielle est constituée d'un backend en Flask, interconnecté à une DB SQLite via l'ORM SQLAlchemy.

Le backend possède une API RESTful sous le préfix /api utilisée pour les requêtes AJAX du frontend.

Pour le faible volume de traffic envisagé, l'utilisation d'un serveur WSGI semble superflue et ce dernier a par conséquent été omis.

L'application est protégée derrière un reverse proxy traefik, qui possède le double avantage de permettre l'authentification de l'utilisateur par divers moyens, y compris HTTP Basic Auth) et aussi de permettre la confirguration d'HTTPS de manière assez aisée.

La solution dans son ensemble est packagée dans un fichier docker-compose incluant l'application et son reverse proxy.

## Installation

Prérequis: Docker

Dans le dossier du projet: ``docker compose up -d`` .

Note: la base de donnée du site web sera enregistrée dans le volume docker ``sae23-data``.
Il est bien évidement possible de sauvegarder cette dernière directement sur un bind mount.

## Ressources

- [Tutoriel Flask](https://www.nileshdalvi.com/blog/flask-crud/)

- [Codes HTTP RESTFul](https://www.restapitutorial.com/lessons/httpmethods.html)
