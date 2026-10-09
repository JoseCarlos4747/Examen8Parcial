"""
Clase base para modelos de base de datos con Peewee ORM.
Aplica Programación Orientada a Objetos (Herencia y Encapsulamiento).
Variables, atributos y métodos en español.
"""
import datetime
from peewee import Model, DateTimeField
from database import base_datos


class ModeloBase(Model):
    """
    Clase abstracta/padre de la cual heredarán todas las entidades del dominio.
    Aplica Herencia en POO para compartir configuración de base de datos y campos comunes.
    """
    fecha_creacion = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = base_datos

    def a_diccionario(self):
        """
        Método base para transformar el modelo a un diccionario serializable a JSON.
        Demuestra Polimorfismo, permitiendo que las clases hijas lo sobreescriban.
        """
        datos = {}
        for nombre_campo in self._meta.fields:
            valor = getattr(self, nombre_campo)
            if isinstance(valor, (datetime.datetime, datetime.date)):
                datos[nombre_campo] = valor.isoformat()
            else:
                datos[nombre_campo] = valor
        return datos

    # Alias para compatibilidad
    def to_dict(self):
        return self.a_diccionario()


# Alias para compatibilidad de importación
BaseModel = ModeloBase
