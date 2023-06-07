import os.path
import sys
sys.path.append('..')

from flask_sqlalchemy import SQLAlchemy

import db as db_holder
db = db_holder.db
    


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

