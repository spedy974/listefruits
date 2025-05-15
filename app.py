from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

# Initialisation
app = Flask(__name__)
app.secret_key = 'secret123'

# Base de données
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'fruits.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle
class Fruit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

# Routes

@app.route('/')
def index():
    fruits = Fruit.query.all()
    return render_template('index.html', fruits=fruits)

@app.route('/fruit/<int:fruit_id>')
def fruit_detail(fruit_id):
    fruit = Fruit.query.get_or_404(fruit_id)
    return render_template('fruit.html', fruit=fruit)

@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter_fruit():
    if request.method == 'POST':
        nom = request.form['nom']
        image = request.form['image']
        description = request.form['description']
        nouveau_fruit = Fruit(nom=nom, image=image, description=description)
        db.session.add(nouveau_fruit)
        db.session.commit()
        flash("Fruit ajouté avec succès.")
        return redirect(url_for('index'))
    return render_template('ajouter.html')

@app.route('/modifier/<int:fruit_id>', methods=['GET', 'POST'])
def modifier_fruit(fruit_id):
    fruit = Fruit.query.get_or_404(fruit_id)
    if request.method == 'POST':
        fruit.nom = request.form['nom']
        fruit.image = request.form['image']
        fruit.description = request.form['description']
        db.session.commit()
        flash("Fruit modifié avec succès.")
        return redirect(url_for('fruit_detail', fruit_id=fruit.id))
    return render_template('modifier.html', fruit=fruit)

@app.route('/supprimer/<int:fruit_id>', methods=['POST'])
def supprimer_fruit(fruit_id):
    fruit = Fruit.query.get_or_404(fruit_id)
    db.session.delete(fruit)
    db.session.commit()
    flash("Fruit supprimé.")
    return redirect(url_for('index'))

# Initialisation de la base de données si besoin
#@app.before_first_request
##db.create_all()

# Lancement
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
