"""
Controlador / Rutas de Autenticación.
Aplica el Principio de Responsabilidad Única (SRP):
Su única función es recibir solicitudes HTTP, invocar al AuthService y devolver respuestas JSON.
"""
from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')
auth_service = AuthService()


@auth_bp.route('/register', methods=['POST'])
def register():
    """Endpoint para registrar un usuario de forma segura."""
    payload = request.get_json(silent=True) or {}
    response_data, status_code = auth_service.register(payload)
    return jsonify(response_data), status_code


@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint para iniciar sesión verificando hash bcrypt."""
    payload = request.get_json(silent=True) or {}
    response_data, status_code = auth_service.login(payload)
    return jsonify(response_data), status_code


@auth_bp.route('/status', methods=['GET'])
def status():
    """Verifica el estado del servicio de autenticación."""
    return jsonify({
        'success': True,
        'message': 'Módulo de autenticación seguro activo.'
    }), 200

