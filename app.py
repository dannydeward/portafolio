import os
from dotenv import load_dotenv  # 1. Importar la librería
from flask import Flask, render_template
from github import Github
import json

# 2. Cargar el archivo .env PRIMERO
#load_dotenv()

app = Flask(__name__)

# 3. Leer las variables DESPUÉS de load_dotenv()
#GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
#GITHUB_USER = os.getenv("GITHUB_USER")

# ⚠️ PASO 1: PEGA TU TOKEN CLASSIC REAL AQUÍ (entre las comillas)
# Asegúrate de que NO haya espacios antes de 'ghp' ni después de la última letra.
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# ⚠️ PASO 2: TU USUARIO REAL DE GITHUB (sin el @)
GITHUB_USER = "dannydeward"

 #⚠️ PASO 3: ESTAS LÍNEAS NOS DIRÁN LA VERDAD
print("🔍 DEBUG - Longitud del token:", len(GITHUB_TOKEN))
print("🔍 DEBUG - El token empieza por:", GITHUB_TOKEN[:10])
print("🔍 DEBUG - El token termina por:", GITHUB_TOKEN[-5:])

# ... (aquí sigue el resto de tu código de CATEGORIAS y rutas) ...

# 🎯 LISTA DE REPOS QUE QUIERES MOSTRAR
CATEGORIAS = {
    "Redes Neuronales e IA": {
        "nombre": "Redes Neuronales e IA",
        "icono": "fa-solid fa-circle-nodes",
        "repos":["Mini_photoshop", "redes-neuronales--GAN-","chatbot"]},
   "APP Webs": {
           "nombre": "Aplicaciones Web",
           "icono": "fa-globe",
           "repos": [ "Runfun", "inmouser", "AppClima-main","gestion_de_pedidos", "Petnow",  "comparador-de-precios", "Finanzas"]
   },
 "Python": {
            "nombre": "Python",
            "icono": "fa-globe",
            "repos": ["calculo-de-interes","supermarket", "Programa-contable"]
 },
 "Aplicaciones Escritorio": {
             "nombre": "Aplicaciones de escritorio",
             "icono": "fa-globe",
             "repos": ["Organizador-de-recetas", "Biblioteca-en-VB.net"]
 }

}

def obtener_repos_por_categoria():
    g = Github(GITHUB_TOKEN)
    usuario = g.get_user(GITHUB_USER)
    
    # Diccionario para guardar los repos ya obtenidos (evita llamadas duplicadas)
    repos_cache = {}
    for repo in usuario.get_repos():
        repos_cache[repo.name] = repo
    
    # Construimos la estructura final
    categorias_con_repos = {}
    for cat_id, cat_data in CATEGORIAS.items():
        repos_filtrados = []
        for nombre_repo in cat_data["repos"]:
            if nombre_repo in repos_cache:
                repo = repos_cache[nombre_repo]
                repos_filtrados.append({
                    "nombre": repo.name,
                    "descripcion": repo.description or "Sin descripción",
                    "tecnologias": [repo.language] if repo.language else [],
                    "github": repo.html_url,
                    "demo": repo.homepage if repo.homepage else None,
                    "estrellas": repo.stargazers_count,
                    "categoria": cat_id
                })
        
        # Solo añadimos la categoría si tiene al menos 1 repo
        if repos_filtrados:
            categorias_con_repos[cat_id] = {
                "nombre": cat_data["nombre"],
                "icono": cat_data["icono"],
                "repos": repos_filtrados
            }
    
    return categorias_con_repos

@app.route('/')
def index():
    # 1. Cargar tus proyectos de GitHub (tu lógica actual)
    categorias = obtener_repos_por_categoria()
    todos_repos = []
    for cat in categorias.values():
        todos_repos.extend(cat["repos"])
    
    # 2. Cargar tus proyectos locales de Análisis de Datos
    with open('data_projects.json', 'r', encoding='utf-8') as f:
        proyectos_analisis = json.load(f)

    # 3. Enviar ambos a la plantilla
    return render_template(
        'index.html', 
        proyectos_destacados=todos_repos[:6], 
        proyectos_analisis=proyectos_analisis # <-- AÑADIDO
    )

@app.route('/proyectos')
def proyectos():
    categorias = obtener_repos_por_categoria()
    return render_template('proyectos.html', categorias=categorias)

if __name__ == '__main__':
    app.run(debug=True)