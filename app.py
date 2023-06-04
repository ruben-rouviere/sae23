from flask import Flask, render_template, url_for, redirect, request, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# On utilise une base de donnée SQLite locale.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # On n'utilise pas le système d'events d'sqlalchemy
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)



# On crée les modèles pour l'ORM

class Chicken(db.Model):
    __table_args__ = {'extend_existing': True}
    __table_name__ = "Chickens"
    # Equivalent SQL : 
    """
    CREATE TABLE "Chickens" (
        "identifier"        INTEGER NOT NULL UNIQUE,
        "name"      TEXT NOT NULL,
        "birthdate" INTEGER NOT NULL,
        "breed"     TEXT NOT NULL,
        "notes"     TEXT,
        “isDeleted” INT DEFAULT 0

        PRIMARY KEY("identifier" AUTOINCREMENT)
    );
    """
    # Note: Par défaut, toutes les colonnes sont NOT NULL.
    id = db.Column(db.Integer, primary_key=True) # Auto increment défini implicitement
    name = db.Column(db.String(64))
    birthdate = db.Column(db.String(16)) # FIXME: Utiliser le type Date, cf https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Date
    breed = db.Column(db.String(64))
    notes = db.Column(db.String(128), nullable=True) 
    isDeleted = db.Column(db.Boolean, default=False) # Tombstone. TODO: Ajouter une fonction de "purge" de la DB afin de DELETE les lignes marquées comme étant supprimées

    # On encapsule la logique de tombstone via des getters

    def get_by_identifier(identifier: int): 
        result = Chicken.query.filter_by(id=identifier, isDeleted=False).first()
        return result
    
    def get_all():
        return [chicken for chicken in Chicken.query.all() if not chicken.isDeleted]
        
    def update(self, data):
        Chicken.query.filter_by(id=self.id).update(data)
        db.session.commit()

    def get_all_deleted():
        return Chicken.query.filter_by(isDeleted=True).all()

    def get_deleted(identifier: int):
        return Chicken.query.filter_by(id=identifier, isDeleted=True).first()
    
    def undelete(self):
        self.update({"isDeleted": False})

    def gc():
        result = Chicken.query.filter_by(isDeleted=True).delete()
        db.session.commit()

    # Chicken => String
    def __repr__(self):
        return f"<identifier: {self.id}, name: {self.name}, birthdate: {self.birthdate}, breed, notes: {self.notes} isDeleted: {self.isDeleted}>"




with app.app_context(): # Création des tables à partir des modèles
    db.create_all()





"""
    API
"""

# Create
@app.route("/api/chicken", methods=["POST"])
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

@app.route('/api/chickens', methods=["GET"])
def list_chickens():
    chickens = Chicken.get_all()
    if(not chickens): return make_response("",204) # No content

    response = make_response('\n'.join([str(chicken) for chicken in chickens]), 200)
    response.mimetype = "text/plain"
    return response

# Read item
@app.route('/api/chicken/<int:identifier>', methods=["GET"])
def get_chicken(identifier):
    chicken = Chicken.get_by_identifier(identifier)
    if(not chicken): return make_response("",404);

    response = make_response(str(chicken), 200)
    response.mimetype = "text/plain"
    return response

# Update
@app.route("/api/chicken/<int:identifier>", methods=["PUT"])
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
@app.route("/api/chicken/<int:identifier>", methods=["DELETE"])
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
@app.route('/api/chickens/deleted', methods=["GET"])
def list_deleted_chickens():
    chickens = Chicken.get_deleted()
    if(not chickens): return make_response("",204) # No content

    response = make_response('\n'.join([str(chicken) for chicken in chickens]), 200)
    response.mimetype = "text/plain"
    return response

# Restore (recreate) a chicken

@app.route('/api/chicken/deleted/<int:identifier>', methods=["PUT", "POST"])
def undelete_chicken(identifier):
    chicken = Chicken.get_deleted(identifier)
    if(not chicken): return make_response("",404)

    chicken.undelete()
    return make_response(str(chicken), 200)


# Purge deleted chickens
@app.route("/api/chickens/deleted", methods=["DELETE"])
def gc_chickens():
    Chicken.gc()

    response = make_response(f"Cleared deleted chickens", 200)
    response.mimetype = "text/plain"
    return response



"""
    Frontend
"""

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

# On lance l'application
if __name__ == "__main__":
    app.run(debug=True)