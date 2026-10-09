"""
Capa de Conexión y Gestión de Base de Datos SQLite usando Peewee ORM.
Semana 5-6 y 8: Previene inyecciones SQL (SQLi) con consultas parametrizadas.
Variables, funciones y parámetros nombrados en español.
"""
from peewee import SqliteDatabase
from config import Configuracion

# Instancia de conexión a la base de datos SQLite
base_datos = SqliteDatabase(
    Configuracion.RUTA_BASE_DATOS,
    pragmas={
        'journal_mode': 'wal',
        'cache_size': -1024 * 64,
        'foreign_keys': 1,
        'ignore_check_constraints': 0,
        'synchronous': 1
    }
)


def inicializar_base_datos(modelos):
    """
    Inicializa la base de datos creando las tablas que no existan.
    :param modelos: Lista de clases de modelos a registrar.
    """
    with base_datos:
        base_datos.create_tables(modelos, safe=True)


# Alias en español y convención
db = base_datos
init_db = inicializar_base_datos
