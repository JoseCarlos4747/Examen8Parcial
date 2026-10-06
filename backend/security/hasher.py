"""
Módulo de Seguridad: Criptografía y Hashing con bcrypt.
Cumple con los requerimientos de la Semana 8:
- Almacenamiento seguro de contraseñas.
- Prohibición de guardar credenciales en texto plano.
- Encapsulamiento en una clase (POO).
"""
import bcrypt


class PasswordHasher:
    """
    Clase responsable del hashing criptográfico y verificación de contraseñas.
    Aplica el Principio de Responsabilidad Única (SRP).
    """

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """
        Genera un hash seguro utilizando bcrypt con un salt aleatorio de 12 rondas.
        :param plain_password: La contraseña en texto plano recibida.
        :return: String del hash resultante seguro para almacenar en la base de datos.
        """
        if not plain_password or not isinstance(plain_password, str):
            raise ValueError("La contraseña proporcionada es inválida.")

        # Convertir a bytes para que bcrypt pueda procesarlo
        password_bytes = plain_password.encode('utf-8')
        # Generar salt seguro (12 rondas de costo por defecto)
        salt = bcrypt.gensalt(rounds=12)
        # Generar el hash seguro
        hashed = bcrypt.hashpw(password_bytes, salt)
        # Retornar como string decodificado en utf-8
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si una contraseña en texto plano coincide con el hash almacenado.
        :param plain_password: La contraseña ingresada por el usuario.
        :param hashed_password: El hash guardado en la base de datos.
        :return: True si coincide, False en caso contrario.
        """
        if not plain_password or not hashed_password:
            return False

        try:
            password_bytes = plain_password.encode('utf-8')
            hashed_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception:
            return False

