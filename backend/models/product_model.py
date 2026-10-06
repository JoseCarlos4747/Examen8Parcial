"""
Modelo de Producto para la librería de útiles escolares.
Aplica Herencia de BaseModel y encapsula la estructura de datos del catálogo escolar.
"""
from peewee import CharField, FloatField, IntegerField, TextField, BooleanField
from models.base_model import BaseModel


class Product(BaseModel):
    """
    Entidad de Producto / Útil Escolar.
    Mapeada a la tabla 'products' en SQLite.
    """
    sku = CharField(max_length=30, unique=True, index=True)
    name = CharField(max_length=150, index=True)
    category = CharField(max_length=60, index=True)
    price = FloatField()
    stock = IntegerField(default=0)
    description = TextField(default='')
    image_url = CharField(max_length=255, default='')
    is_active = BooleanField(default=True)

    class Meta:
        table_name = 'products'

    def to_dict(self):
        """Devuelve un diccionario limpio para las respuestas JSON de la API."""
        return {
            'id': self.id,
            'sku': self.sku,
            'name': self.name,
            'category': self.category,
            'price': round(float(self.price), 2),
            'stock': int(self.stock),
            'description': self.description,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

