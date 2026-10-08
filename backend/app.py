"""
Servidor Principal de la Aplicación Web EduPapel.
Evaluación Parcial - Semanas 1 a 8.
Integra Flask, CORS, Peewee ORM, Criptografía bcrypt y Arquitectura Limpia/Modular.
"""
import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import Config
from database import db, init_db
from models.user_model import User
from models.product_model import Product
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from seed import seed_database

# Rutas del Frontend para servir de forma estática opcional
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
app.config.from_object(Config)

# Habilitar CORS para permitir peticiones asíncronas desde el Frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})


# Manejo del ciclo de vida de la base de datos por solicitud (Buenas prácticas Peewee)
@app.before_request
def _db_connect():
    if db.is_closed():
        db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


# Registrar Blueprints (Separación de rutas y controladores - SOLID SRP)
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)


# Rutas para servir la interfaz Frontend desde el mismo servidor Flask
@app.route('/')
def serve_index():
    """Sirve la página principal de la tienda/librería escolar."""
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Sirve archivos estáticos (css, js, imágenes) del frontend."""
    file_path = os.path.join(FRONTEND_DIR, path)
    if os.path.exists(file_path):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, 'index.html')


# Manejadores de errores globales en formato JSON
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'success': False,
        'message': 'Recurso no encontrado (404).'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Error interno del servidor (500).'
    }), 500


def bootstrap_application():
    """Inicializa la base de datos y asegura datos de prueba al arrancar."""
    init_db([User, Product])
    # Si la base de datos está vacía, sembramos datos automáticamente
    if Product.select().count() == 0:
        print("Base de datos sin registros. Ejecutando semillado inicial...")
        seed_database()


if __name__ == '__main__':
    bootstrap_application()
    print("==================================================")
    print(f">> Servidor corriendo en: http://127.0.0.1:{Config.PORT}")
    print(f">> Endpoints de la API:  http://127.0.0.1:{Config.PORT}/api/products")
    print("==================================================")
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
