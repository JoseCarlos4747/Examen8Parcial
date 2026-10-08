"""
Clase Base de Servicio.
Aplica principios de Programación Orientada a Objetos (Herencia y Abstracción).
Centraliza la estructura estándar de respuestas de la lógica de negocio.
"""


class BaseService:
    """
    Clase padre de la cual heredan los servicios del sistema.
    Aplica el principio Open/Closed (OCP) permitiendo extender lógica común.
    """

    @staticmethod
    def success_response(data=None, message="Operación exitosa", status_code=200):
        """Genera una respuesta estandarizada de éxito."""
        return {
            'success': True,
            'message': message,
            'data': data
        }, status_code

    @staticmethod
    def error_response(message="Ha ocurrido un error", status_code=400, errors=None):
        """Genera una respuesta estandarizada de error."""
        response = {
            'success': False,
            'message': message
        }
        if errors:
            response['errors'] = errors
        return response, status_code

