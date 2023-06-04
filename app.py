from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# On utilise une base de donnée SQLite locale.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # On n'utilise pas le système d'events d'sqlalchemy
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

with app.app_context(): # Création des tables à partir des modèles
    db.create_all()

from controllers import Chicken
app.register_blueprint(Chicken.bp)


# On lance l'application
if __name__ == "__main__":
    app.run(debug=True)