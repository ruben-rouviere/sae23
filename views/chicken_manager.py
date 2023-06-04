from flask import Flask, render_template, url_for, redirect, request, make_response

import app

@app.route('/base.css')
def css():
    response = make_response(render_template('base.css'), 200)
    response.mimetype = "text/css"
    return response

@app.route('/favicon.ico')
def favicon():
    return "",204 # FIXME: Ajouter une favicon

@app.route('/')
def index():
    return '<a href="/chickens">Gestion poules</a>'

@app.route('/chickens', methods=["GET"])
def chicken_manager():
    chickens = Chicken.get_all()
    return render_template("chickens.html", chickens=chickens)

@app.route('/chickens/deleted', methods=["GET"])
def deleted_chicken_manager():
    chickens = Chicken.get_all_deleted()
    return render_template("deleted-chickens.html", chickens=chickens)