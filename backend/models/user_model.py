"""
Modelo de Usuario para autenticación y control de acceso.
Aplica Herencia (hereda de ModeloBase) y Encapsulamiento de datos sensibles.
Variables, atributos y métodos en español.
"""
from peewee import CharField, BooleanField
from models.base_model import ModeloBase


class Usuario(ModeloBase):
    """
    Entidad de usuario en la base de datos.
    Almacena credenciales de manera segura (contraseña con hash bcrypt).
    """
    nombre_usuario = CharField(max_length=50, unique=True, index=True)
    correo = CharField(max_length=120, unique=True, index=True)
    clave_hash = CharField(max_length=255)
    rol = CharField(max_length=20, default='admin')
    esta_activo = BooleanField(default=True)

    class Meta:
        table_name = 'usuarios'

    def a_diccionario(self, incluir_sensible=False):
        """
        Sobrescritura polimórfica de a_diccionario.
        Encapsulamiento: Por seguridad (OWASP Top 10), nunca incluye el hash
        de la contraseña a menos que se indique explícitamente en el backend.
        """
        datos = {
            'id': self.id,
            'nombre_usuario': self.nombre_usuario,
            'correo': self.correo,
            'rol': self.rol,
            'esta_activo': self.esta_activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
        if incluir_sensible:
            datos['clave_hash'] = self.clave_hash
        return datos

    # Alias
    def to_dict(self, include_sensitive=False):
        return self.a_diccionario(incluir_sensible=include_sensitive)


# Alias para compatibilidad
User = Usuario
