"""
Clase Base de Servicio.
Aplica principios de Programación Orientada a Objetos (Herencia y Abstracción).
Centraliza la estructura estándar de respuestas de la lógica de negocio.
Variables, métodos y parámetros en español.
"""


class ServicioBase:
    """
    Clase padre de la cual heredan los servicios del sistema.
    Aplica el principio Open/Closed (OCP) permitiendo extender lógica común.
    """

    @staticmethod
    def respuesta_exitosa(datos=None, mensaje="Operación exitosa", codigo_estado=200):
        """Genera una respuesta estandarizada de éxito."""
        cuerpo_respuesta = {
            'exito': True,
            'success': True,  # Mantiene compatibilidad
            'mensaje': mensaje,
            'message': mensaje,
            'datos': datos,
            'data': datos
        }
        return cuerpo_respuesta, codigo_estado

    @staticmethod
    def respuesta_error(mensaje="Ha ocurrido un error", codigo_estado=400, errores=None):
        """Genera una respuesta estandarizada de error."""
        cuerpo_respuesta = {
            'exito': False,
            'success': False,
            'mensaje': mensaje,
            'message': mensaje
        }
        if errores:
            cuerpo_respuesta['errores'] = errores
            cuerpo_respuesta['errors'] = errores
        return cuerpo_respuesta, codigo_estado

    # Alias para compatibilidad
    success_response = respuesta_exitosa
    error_response = respuesta_error


# Alias de clase
BaseService = ServicioBase
