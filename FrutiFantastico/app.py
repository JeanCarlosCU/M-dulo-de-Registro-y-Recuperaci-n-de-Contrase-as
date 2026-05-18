from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import certifi

app = Flask(__name__)

url = "mongodb+srv://frutiAdmin:Cetis#61@cluster0.rfqjfus.mongodb.net/?appName=Cluster0"

cliente = MongoClient(
    url,
    tlsCAFile=certifi.where()
)

db = cliente["FrutiFantasticoDB"]

clientes = db["clientes"]
usuarios = db["usuarios"]
productos = db["productos"]


if clientes.count_documents({}) == 0:

    clientes.insert_many([
        {
            "nombre": "Smart",
            "ciudad": "Ciudad Juarez"
        },
        {
            "nombre": "Frutas DonCarlos",
            "ciudad": "Ciudad Juarez"
        },
        {
            "nombre": "Supermercado Gonzales",
            "ciudad": "Chihuahua"
        }
    ])


if productos.count_documents({}) == 0:

    productos.insert_many([

        {
            "nombre": "Fresa",
            "categoria": "Bayas",
            "stock": 120
        },

        {
            "nombre": "Mango",
            "categoria": "Exoticas",
            "stock": 80
        },

        {
            "nombre": "Naranja",
            "categoria": "Citricos",
            "stock": 200
        },

        {
            "nombre": "Manzana",
            "categoria": "Fruta dulce",
            "stock": 150
        },

        {
            "nombre": "Sandia",
            "categoria": "Cucurbitaceas",
            "stock": 60
        }

    ])

@app.route("/", methods=["GET", "POST"])
def login():

    mensaje = ""

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        usuario_db = usuarios.find_one({
            "usuario": usuario,
            "password": password
        })

        if usuario_db:

            return redirect("/dashboard")

        else:

            mensaje = "Usuario o contraseña incorrectos"

    return render_template(
        "login.html",
        mensaje=mensaje
    )

@app.route("/registro", methods=["GET", "POST"])
def registro():

    mensaje = ""

    if request.method == "POST":

        usuario = request.form["usuario"]
        correo = request.form["correo"]
        password = request.form["password"]

        existe = usuarios.find_one({
            "$or": [
                {"usuario": usuario},
                {"correo": correo}
            ]
        })

        if existe:

            mensaje = "El usuario o correo ya existe"

        else:

            usuarios.insert_one({

                "usuario": usuario,
                "correo": correo,
                "password": password

            })

            return redirect("/")

    return render_template(
        "registro.html",
        mensaje=mensaje
    )

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    mensaje = ""

    if request.method == "POST":

        correo = request.form["correo"]

        usuario = usuarios.find_one({
            "correo": correo
        })

        if usuario:

            return redirect(
                url_for(
                    "reset_password",
                    correo=correo
                )
            )

        else:

            mensaje = "Correo no encontrado"

    return render_template(
        "forgot_password.html",
        mensaje=mensaje
    )

@app.route("/reset-password/<correo>", methods=["GET", "POST"])
def reset_password(correo):

    if request.method == "POST":

        nueva_password = request.form["password"]

        usuarios.update_one(

            {"correo": correo},

            {
                "$set": {
                    "password": nueva_password
                }
            }

        )

        return redirect("/")

    return render_template(
        "reset_password.html",
        correo=correo
    )

@app.route("/dashboard")
def dashboard():

    lista_productos = list(productos.find())
    lista_clientes = list(clientes.find())

    return render_template(
        "dashboard.html",
        clientes=lista_clientes,
        productos=lista_productos
    )

if __name__ == "__main__":

    app.run(debug=True)