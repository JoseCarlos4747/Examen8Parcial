"""
Servidor Principal de la Aplicación Web EduPapel.
Evaluación Parcial - Semanas 1 a 8.
Integra Flask, CORS, Peewee ORM, Criptografía bcrypt y Arquitectura Limpia/Modular.
Nombres de variables, funciones y controladores en español.
"""
import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import Configuracion
from database import base_datos, inicializar_base_datos
from models.user_model import Usuario
from models.product_model import Producto
from routes.auth_routes import rutas_autenticacion
from routes.product_routes import rutas_productos
from seed import sembrar_base_datos

# Ruta al directorio del Frontend para entrega estática
DIRECTORIO_FRONTEND = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

aplicacion = Flask(__name__, static_folder=DIRECTORIO_FRONTEND, static_url_path='')
aplicacion.config.from_object(Configuracion)

# Habilitar CORS para permitir peticiones asíncronas desde cualquier origen
CORS(aplicacion, resources={r"/api/*": {"origins": "*"}})


# Manejo del ciclo de vida de la base de datos por solicitud HTTP
@aplicacion.before_request
def conectar_base_datos():
    """Abre la conexión con SQLite antes de cada petición."""
    if base_datos.is_closed():
        base_datos.connect()


@aplicacion.teardown_request
def cerrar_base_datos(error_excepcion):
    """Cierra la conexión con SQLite al finalizar la petición."""
    if not base_datos.is_closed():
        base_datos.close()


# Registro de Blueprints (Separación modular de rutas - SOLID SRP)
aplicacion.register_blueprint(rutas_autenticacion)
aplicacion.register_blueprint(rutas_productos)


# Rutas para servir la interfaz web
@aplicacion.route('/')
def servir_inicio():
    """Sirve la página principal de la librería escolar."""
    return send_from_directory(DIRECTORIO_FRONTEND, 'index.html')


@aplicacion.route('/<path:ruta_archivo>')
def servir_archivos_estaticos(ruta_archivo):
    """Sirve archivos estáticos (css, js, imágenes) del frontend."""
    ruta_completa = os.path.join(DIRECTORIO_FRONTEND, ruta_archivo)
    if os.path.exists(ruta_completa):
        return send_from_directory(DIRECTORIO_FRONTEND, ruta_archivo)
    return send_from_directory(DIRECTORIO_FRONTEND, 'index.html')


# Manejadores de errores globales en formato JSON
@aplicacion.errorhandler(404)
def error_no_encontrado(error):
    return jsonify({
        'exito': False,
        'success': False,
        'mensaje': 'Recurso no encontrado (404).'
    }), 404


@aplicacion.errorhandler(500)
def error_servidor_interno(error):
    return jsonify({
        'exito': False,
        'success': False,
        'mensaje': 'Error interno del servidor (500).'
    }), 500


def inicializar_aplicacion():
    """Inicializa la base de datos y asegura datos de prueba al arrancar."""
    inicializar_base_datos([Usuario, Producto])
    if Producto.select().count() == 0:
        print("Base de datos sin registros. Ejecutando semillado inicial...")
        sembrar_base_datos()


# Alias para servidores WSGI
app = aplicacion

if __name__ == '__main__':
    inicializar_aplicacion()
    print("==================================================")
    print(">> Servidor EduPapel iniciado exitosamente")
    print(f">> URL de la Aplicacion: http://127.0.0.1:{Configuracion.PUERTO}")
    print(f">> Endpoints de la API:  http://127.0.0.1:{Configuracion.PUERTO}/api/products")
    print("==================================================")
    aplicacion.run(host='0.0.0.0', port=Configuracion.PUERTO, debug=Configuracion.MODO_DEPURACION)
