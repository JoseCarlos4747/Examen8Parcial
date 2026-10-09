"""
Controlador / Rutas de Autenticación.
Aplica el Principio de Responsabilidad Única (SRP):
Recibe solicitudes HTTP, invoca a ServicioAutenticacion y devuelve respuestas JSON.
Variables, funciones y parámetros en español.
"""
from flask import Blueprint, request, jsonify
from services.auth_service import ServicioAutenticacion

rutas_autenticacion = Blueprint('rutas_autenticacion', __name__, url_prefix='/api/auth')
servicio_autenticacion = ServicioAutenticacion()


@rutas_autenticacion.route('/register', methods=['POST'])
@rutas_autenticacion.route('/registro', methods=['POST'])
def registrar_usuario():
    """Endpoint para registrar un usuario de forma segura."""
    datos_recibidos = request.get_json(silent=True) or {}
    respuesta_datos, codigo_estado = servicio_autenticacion.registrar(datos_recibidos)
    return jsonify(respuesta_datos), codigo_estado


@rutas_autenticacion.route('/login', methods=['POST'])
@rutas_autenticacion.route('/ingreso', methods=['POST'])
def iniciar_sesion():
    """Endpoint para iniciar sesión verificando hash bcrypt."""
    datos_recibidos = request.get_json(silent=True) or {}
    respuesta_datos, codigo_estado = servicio_autenticacion.iniciar_sesion(datos_recibidos)
    return jsonify(respuesta_datos), codigo_estado


@rutas_autenticacion.route('/status', methods=['GET'])
@rutas_autenticacion.route('/estado', methods=['GET'])
def verificar_estado():
    """Verifica el estado del servicio de autenticación."""
    return jsonify({
        'exito': True,
        'success': True,
        'mensaje': 'Módulo de autenticación seguro activo.'
    }), 200


# Alias para compatibilidad
auth_bp = rutas_autenticacion
