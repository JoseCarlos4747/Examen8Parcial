"""
Clase base para modelos Peewee.
Aplica Programación Orientada a Objetos (Herencia y Encapsulamiento)
y el Principio de Responsabilidad Única (SRP).
"""
import datetime
from peewee import Model, DateTimeField
from database import db


class BaseModel(Model):
    """
    Clase abstracta/base de la cual heredarán todas las entidades del dominio.
    Demuestra Herencia en POO para reutilizar la configuración de la BD y fechas.
    """
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

    def to_dict(self):
        """
        Método base para transformar el modelo a un diccionario serializable a JSON.
        Las clases hijas pueden sobreescribir este método según sus necesidades (Polimorfismo).
        """
        data = {}
        for field_name in self._meta.fields:
            value = getattr(self, field_name)
            if isinstance(value, (datetime.datetime, datetime.date)):
                data[field_name] = value.isoformat()
            else:
                data[field_name] = value
        return data

