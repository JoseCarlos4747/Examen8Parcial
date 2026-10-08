"""
Configuración centralizada de la aplicación.
Semana 8: Evita hardcoding de claves secretas y rutas sensibles mediante python-dotenv.
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    """Clase base de configuración aplicando Principio de Responsabilidad Única (SRP)."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key_fallback_only')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
    PORT = int(os.getenv('FLASK_PORT', 5000))

    # Ruta a la base de datos SQLite
    DB_NAME = os.getenv('DATABASE_NAME', 'libreria_escolar.db')
    DB_PATH = os.path.join(BASE_DIR, DB_NAME)

