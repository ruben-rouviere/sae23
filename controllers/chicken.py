from flask import request, make_response, Blueprint

from models.Chicken import Chicken

bp = Blueprint('api', __name__, url_prefix='/api')

import db as db_holder
db = db_holder.db


import os.path
import sys
sys.path.append('.')

# Create
@bp.route("/chicken", methods=["POST"])
def new_chicken():
    new_chicken = Chicken(
            name=request.form.get("name"),
            birthdate=request.form.get("birthdate"),
            breed=request.form.get("breed"),
            notes=request.form.get("notes"),
        )
    db.session.add(new_chicken)
    db.session.commit()

    response = make_response(str(new_chicken), 201)
    response.mimetype = "text/plain"
    return response

# Read collection

@bp.route('/chickens', methods=["GET"])
def list_chickens():
    chickens = Chicken.get_all()
    if(not chickens): return make_response("",204) # No content

    response = make_response('\n'.join([str(chicken) for chicken in chickens]), 200)
    response.mimetype = "text/plain"
    return response

# Read item
@bp.route('/chicken/<int:identifier>', methods=["GET"])
def get_chicken(identifier):
    chicken = Chicken.get_by_identifier(identifier)
    if(not chicken): return make_response("",404);

    response = make_response(str(chicken), 200)
    response.mimetype = "text/plain"
    return response

# Update
@bp.route("/chicken/<int:identifier>", methods=["PUT"])
def edit_chicken(identifier):
    chicken = Chicken.get_by_identifier(identifier)
    if(not chicken): return make_response("",404);
    chicken.update({
        "name":         request.form.get("name"),
        "birthdate":    request.form.get("birthdate"), # TODO: Validentifieration de la date coté backend
        "breed":        request.form.get("breed"),
        "notes":        request.form.get("notes")
    })

    response = make_response(str(chicken), 200)
    response.mimetype = "text/plain"
    return response

# Delete
@bp.route("/chicken/<int:identifier>", methods=["DELETE"])
def delete_chicken(identifier):
    chicken = Chicken.get_by_identifier(identifier)
    if(not chicken): return make_response("",404);

    chicken.isDeleted = True # On ne supprime pas réellement la poule conformément au cahieŕ des charges (tombstone)
    db.session.commit()

    response = make_response(f"Deleted {str(chicken)}", 200)
    response.mimetype = "text/plain"
    return response


# Gestion des poules supprimées

# Read deleted chickens
@bp.route('/chickens/deleted', methods=["GET"])
def list_deleted_chickens():
    chickens = Chicken.get_deleted()
    if(not chickens): return make_response("",204) # No content

    response = make_response('\n'.join([str(chicken) for chicken in chickens]), 200)
    response.mimetype = "text/plain"
    return response

# Restore (recreate) a chicken

@bp.route('/chicken/deleted/<int:identifier>', methods=["PUT", "POST"])
def undelete_chicken(identifier):
    chicken = Chicken.get_deleted(identifier)
    if(not chicken): return make_response("",404)

    chicken.undelete()
    return make_response(str(chicken), 200)


# Purge deleted chickens
@bp.route("/chickens/deleted", methods=["DELETE"])
def gc_chickens():
    Chicken.gc()

    response = make_response(f"Cleared deleted chickens", 200)
    response.mimetype = "text/plain"
    return response
