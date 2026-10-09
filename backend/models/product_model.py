"""
Modelo de Producto para la librería de útiles escolares.
Aplica Herencia de ModeloBase y encapsula la estructura de datos del catálogo escolar.
Variables, atributos y métodos en español.
"""
from peewee import CharField, FloatField, IntegerField, TextField, BooleanField
from models.base_model import ModeloBase


class Producto(ModeloBase):
    """
    Entidad de Producto / Útil Escolar en la base de datos.
    Mapeada a la tabla 'productos' en SQLite.
    """
    codigo_sku = CharField(max_length=30, unique=True, index=True)
    nombre = CharField(max_length=150, index=True)
    categoria = CharField(max_length=60, index=True)
    precio = FloatField()
    stock = IntegerField(default=0)
    descripcion = TextField(default='')
    imagen_url = CharField(max_length=255, default='')
    esta_activo = BooleanField(default=True)

    class Meta:
        table_name = 'productos'

    def a_diccionario(self):
        """Devuelve un diccionario limpio para las respuestas JSON de la API."""
        return {
            'id': self.id,
            'codigo_sku': self.codigo_sku,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'precio': round(float(self.precio), 2),
            'stock': int(self.stock),
            'descripcion': self.descripcion,
            'imagen_url': self.imagen_url,
            'esta_activo': self.esta_activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

    # Alias
    def to_dict(self):
        return self.a_diccionario()


# Alias para compatibilidad
Product = Producto
