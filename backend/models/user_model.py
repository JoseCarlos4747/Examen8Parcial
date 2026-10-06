"""
Modelo de Usuario para autenticación y control de acceso.
Aplica Herencia (hereda de BaseModel) y Encapsulamiento de datos sensibles.
"""
from peewee import CharField, BooleanField
from models.base_model import BaseModel


class User(BaseModel):
    """
    Entidad de usuario en la base de datos.
    Almacena credenciales de manera segura (contraseña con hash bcrypt).
    """
    username = CharField(max_length=50, unique=True, index=True)
    email = CharField(max_length=120, unique=True, index=True)
    password_hash = CharField(max_length=255)
    role = CharField(max_length=20, default='admin')
    is_active = BooleanField(default=True)

    class Meta:
        table_name = 'users'

    def to_dict(self, include_sensitive=False):
        """
        Sobrescritura polimórfica de to_dict.
        Encapsulamiento: Por seguridad (OWASP Top 10), nunca incluye el hash
        de la contraseña a menos que se indique explícitamente en el backend.
        """
        data = super().to_dict()
        if not include_sensitive:
            data.pop('password_hash', None)
        return data

