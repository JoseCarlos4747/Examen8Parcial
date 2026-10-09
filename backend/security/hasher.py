"""
Módulo de Seguridad: Criptografía y Hashing con bcrypt.
Semana 8: Almacenamiento seguro de contraseñas.
Nombres de clases, métodos y variables en español.
"""
import bcrypt


class EncriptadorClaves:
    """
    Clase responsable del hashing criptográfico y verificación de contraseñas.
    Aplica el Principio de Responsabilidad Única (SRP).
    """

    @staticmethod
    def hashear_clave(clave_plana: str) -> str:
        """
        Genera un hash seguro utilizando bcrypt con un salt aleatorio de 12 rondas.
        :param clave_plana: La contraseña en texto plano recibida.
        :return: Cadena de texto con el hash seguro para almacenar en SQLite.
        """
        if not clave_plana or not isinstance(clave_plana, str):
            raise ValueError("La contraseña proporcionada es inválida.")

        # Convertir a bytes para el algoritmo de bcrypt
        bytes_clave = clave_plana.encode('utf-8')
        # Generar semilla (salt) de 12 rondas de complejidad
        semilla_salt = bcrypt.gensalt(rounds=12)
        # Generar el hash seguro
        clave_hasheada = bcrypt.hashpw(bytes_clave, semilla_salt)
        return clave_hasheada.decode('utf-8')

    @staticmethod
    def verificar_clave(clave_plana: str, clave_hasheada: str) -> bool:
        """
        Verifica si una contraseña en texto plano coincide con el hash almacenado.
        :param clave_plana: La contraseña ingresada por el usuario.
        :param clave_hasheada: El hash guardado en la base de datos.
        :return: True si coinciden, False en caso contrario.
        """
        if not clave_plana or not clave_hasheada:
            return False

        try:
            bytes_plano = clave_plana.encode('utf-8')
            bytes_hash = clave_hasheada.encode('utf-8')
            return bcrypt.checkpw(bytes_plano, bytes_hash)
        except Exception:
            return False

    # Alias para compatibilidad
    hash_password = hashear_clave
    verify_password = verificar_clave


# Alias de clase
PasswordHasher = EncriptadorClaves
