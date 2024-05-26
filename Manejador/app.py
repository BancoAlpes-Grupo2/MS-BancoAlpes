from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import random
from models import db, Usuario, Tarjeta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manejador.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.json
    puntaje = random.randint(0, 100)
    usuario = Usuario(nombre=data['nombre'], puntaje=puntaje)
    db.session.add(usuario)
    db.session.commit()
    return jsonify({"id": usuario.id, "nombre": usuario.nombre, "puntaje": usuario.puntaje})

@app.route('/usuarios/<int:id>/tarjetas', methods=['GET'])
def obtener_tarjetas(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    tarjetas = Tarjeta.query.filter(Tarjeta.puntaje_minimo <= usuario.puntaje).all()
    tarjetas_asignadas = [{"tipo": tarjeta.tipo, "puntaje_minimo": tarjeta.puntaje_minimo} for tarjeta in tarjetas]
    return jsonify(tarjetas_asignadas)

if __name__ == '__main__':
    app.run(debug=True)
