import os.path
import sys
sys.path.append('..')

from flask import Blueprint, render_template, url_for, redirect, request, make_response
from controllers.chicken import Chicken

bp = Blueprint('chicken_manager', __name__, url_prefix='/')


@bp.route('/base.css')
def css():
    response = make_response(render_template('base.css'), 200)
    response.mimetype = "text/css"
    return response

@bp.route('/favicon.ico')
def favicon():
    return "",204 # FIXME: Ajouter une favicon

@bp.route('/')
def index():
    return '<a href="/chickens">Gestion poules</a>'

@bp.route('/chickens', methods=["GET"])
def chicken_manager():
    chickens = Chicken.get_all()
    return render_template("chickens.html", chickens=chickens)

@bp.route('/chickens/deleted', methods=["GET"])
def deleted_chicken_manager():
    chickens = Chicken.get_all_deleted()
    return render_template("deleted-chickens.html", chickens=chickens)