"""
Capa de Conexión y Gestión de Base de Datos SQLite usando Peewee ORM.
Semana 5-6 y 8: El uso de Peewee ORM previene inyecciones SQL (SQLi)
al parametrizar automáticamente todas las consultas.
"""
from peewee import SqliteDatabase
from config import Config

# Instancia de conexión a SQLite
db = SqliteDatabase(
    Config.DB_PATH,
    pragmas={
        'journal_mode': 'wal',
        'cache_size': -1024 * 64,
        'foreign_keys': 1,
        'ignore_check_constraints': 0,
        'synchronous': 1
    }
)


def init_db(models):
    """
    Inicializa la base de datos creando las tablas que no existan.
    :param models: Lista de clases de modelos Peewee a registrar.
    """
    with db:
        db.create_tables(models, safe=True)

