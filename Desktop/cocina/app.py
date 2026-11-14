import json
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
ARCHIVO_RECETAS = "recetas.json"

# Recetas iniciales de ejemplo para que no arranque vacío
RECETAS_INICIALES = {
    "ricota_polvo": {
        "nombre": "Ricota (Base Leche en Polvo)",
        "ingredientes": [
            {"nombre": "Leche en polvo", "cantidad": 160.0, "unidad": "g", "densidad": None},
            {"nombre": "Agua común", "cantidad": 800.0, "unidad": "ml", "densidad": 1.00},
            {"nombre": "Vinagre de alcohol (2%)", "cantidad": 19.2, "unidad": "g", "densidad": 1.01},
            {"nombre": "Sal fina (0.05%)", "cantidad": 0.48, "unidad": "g", "densidad": None}
        ]
    },
    "marinada_cerveza": {
        "nombre": "Marinada Base Cerveza",
        "ingredientes": [
            {"nombre": "Cerveza", "cantidad": 1000.0, "unidad": "ml", "densidad": 1.01},
            {"nombre": "Vinagre de alcohol", "cantidad": 50.0, "unidad": "ml", "densidad": 1.01},
            {"nombre": "Aceite común", "cantidad": 100.0, "unidad": "ml", "densidad": 0.92},
            {"nombre": "Sal fina", "cantidad": 15.0, "unidad": "g", "densidad": None}
        ]
    }
}

def cargar_recetas():
    if not os.path.exists(ARCHIVO_RECETAS):
        guardar_recetas(RECETAS_INICIALES)
        return RECETAS_INICIALES
    with open(ARCHIVO_RECETAS, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_recetas(data):
    with open(ARCHIVO_RECETAS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route("/")
def index():
    recetas = cargar_recetas()
    return render_template("index.html", recetas=recetas)

@app.route("/guardar_receta", methods=["POST"])
def nueva_receta():
    data = request.json
    recetas = cargar_recetas()
    clave = data["nombre"].lower().replace(" ", "_")
    recetas[clave] = {
        "nombre": data["nombre"],
        "ingredientes": data["ingredientes"]
    }
    guardar_recetas(recetas)
    return jsonify({"status": "ok", "recetas": recetas})

if __name__ == "__main__":
    app.run(debug=True)