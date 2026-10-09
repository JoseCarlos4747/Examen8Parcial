"""
Configuración centralizada de la aplicación.
Semana 8: Evita hardcoding de claves secretas y rutas sensibles mediante python-dotenv.
Todas las variables, constantes y atributos se encuentran nombrados en español.
"""
import os
from dotenv import load_dotenv

# Ruta absoluta al directorio base del backend
DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
ruta_archivo_entorno = os.path.join(DIRECTORIO_BASE, '.env')

if os.path.exists(ruta_archivo_entorno):
    load_dotenv(ruta_archivo_entorno)


class Configuracion:
    """Clase de configuración aplicando el Principio de Responsabilidad Única (SRP)."""
    CLAVE_SECRETA = os.getenv('SECRET_KEY', 'clave_secreta_edupapel_2026')
    ENTORNO = os.getenv('FLASK_ENV', 'development')
    MODO_DEPURACION = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
    PUERTO = int(os.getenv('FLASK_PORT', 5000))

    # Nombre y ruta del archivo SQLite
    NOMBRE_BASE_DATOS = os.getenv('DATABASE_NAME', 'libreria_escolar.db')
    RUTA_BASE_DATOS = os.path.join(DIRECTORIO_BASE, NOMBRE_BASE_DATOS)

    # Compatibilidad con variables internas que busca Flask
    SECRET_KEY = CLAVE_SECRETA
    DEBUG = MODO_DEPURACION
