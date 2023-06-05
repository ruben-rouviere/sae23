# PEP 366
if __name__ == "__main__" and __package__ is None:
        __package__ = "app"

import os.path
import sys
sys.path.append('.')


from flask import Flask

def create_app():
    print("Creating app.")
    app = Flask(__name__)
    # On utilise une base de donnée SQLite locale.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # On n'utilise pas le système d'events d'sqlalchemy
    app.config['SQLALCHEMY_ECHO'] = True

    db.init_app(app)


    with app.app_context(): # Création des tables à partir des modèles
        db.create_all()


    from controllers import chicken
    app.register_blueprint(chicken.bp)
    
    from views import chicken_manager
    app.register_blueprint(chicken_manager.bp)


    # On lance l'application
    if __name__ == "__main__":
        app.run(debug=True)
        
    return app

# On initialise la db
from db import db

app = create_app()