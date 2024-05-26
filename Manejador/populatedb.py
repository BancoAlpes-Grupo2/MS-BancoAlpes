import random
from faker import Faker
from app import app, db, Usuario, Tarjeta

fake = Faker()

def agregar_tarjetas():
    if Tarjeta.query.count() == 0:
        tarjetas = [
            Tarjeta(tipo="Tarjeta Básica", puntaje_minimo=0),
            Tarjeta(tipo="Tarjeta Silver", puntaje_minimo=50),
            Tarjeta(tipo="Tarjeta Gold", puntaje_minimo=75),
        ]
        db.session.bulk_save_objects(tarjetas)
        db.session.commit()
        print("Tarjetas agregadas a la base de datos.")
    else:
        print("Las tarjetas ya están en la base de datos.")

def agregar_usuarios(cantidad):
    usuarios = []
    for _ in range(cantidad):
        nombre = fake.name()
        puntaje = random.randint(0, 100)
        usuario = Usuario(nombre=nombre, puntaje=puntaje)
        usuarios.append(usuario)
    db.session.bulk_save_objects(usuarios)
    db.session.commit()
    print(f"{cantidad} usuarios agregados a la base de datos.")

if __name__ == "__main__":
    with app.app_context():
        agregar_tarjetas()
        agregar_usuarios(10000)  # Cambia este número para agregar más o menos usuarios
