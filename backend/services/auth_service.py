"""
Servicio de Autenticación y Cuentas de Usuario.
Aplica POO (Hereda de BaseService) y Principios SOLID (SRP).
Utiliza PasswordHasher (bcrypt) e InputSanitizer para seguridad (OWASP).
"""
from models.user_model import User
from services.base_service import BaseService
from security.hasher import PasswordHasher
from security.sanitizer import InputSanitizer


class AuthService(BaseService):
    """
    Gestiona la lógica de negocio de usuarios:
    registro seguro con bcrypt y validación de credenciales en el login.
    """

    def register(self, payload: dict):
        """
        Registra un nuevo usuario en la base de datos con contraseña hasheada.
        """
        is_valid, error_msg, clean_data = InputSanitizer.validate_user_payload(payload)
        if not is_valid:
            return self.error_response(message=error_msg, status_code=400)

        username = clean_data['username']
        email = clean_data['email']
        plain_password = clean_data['password']

        # Verificar si el usuario o email ya existe (consultas parametrizadas con Peewee -> Anti SQLi)
        if User.select().where((User.username == username) | (User.email == email)).exists():
            return self.error_response(
                message="El nombre de usuario o correo electrónico ya se encuentra registrado.",
                status_code=409
            )

        try:
            # Encriptación / Hashing seguro de la contraseña usando bcrypt
            password_hash = PasswordHasher.hash_password(plain_password)

            # Creación del usuario en la base de datos
            new_user = User.create(
                username=username,
                email=email,
                password_hash=password_hash,
                role='admin'
            )

            # Retornar datos seguros sin exponer password_hash
            return self.success_response(
                data=new_user.to_dict(include_sensitive=False),
                message="Usuario registrado exitosamente.",
                status_code=201
            )
        except Exception as ex:
            return self.error_response(
                message=f"Error al registrar usuario: {str(ex)}",
                status_code=500
            )

    def login(self, payload: dict):
        """
        Valida las credenciales del usuario y verifica el hash bcrypt.
        """
        if not isinstance(payload, dict):
            return self.error_response(message="Formato de datos no válido.", status_code=400)

        identifier = InputSanitizer.sanitize_string(payload.get('identifier', payload.get('email', ''))).lower()
        password = str(payload.get('password', '')).strip()

        if not identifier or not password:
            return self.error_response(
                message="Debe ingresar su usuario o correo y su contraseña.",
                status_code=400
            )

        # Buscar usuario por username o email de manera segura
        user = User.get_or_none((User.email == identifier) | (User.username == identifier))
        if not user or not user.is_active:
            # Mensaje genérico para evitar enumeración de usuarios (OWASP)
            return self.error_response(
                message="Credenciales incorrectas o usuario no encontrado.",
                status_code=401
            )

        # Verificación segura de la contraseña usando bcrypt
        is_password_correct = PasswordHasher.verify_password(password, user.password_hash)
        if not is_password_correct:
            return self.error_response(
                message="Credenciales incorrectas o usuario no encontrado.",
                status_code=401
            )

        # Login exitoso
        user_info = user.to_dict(include_sensitive=False)
        return self.success_response(
            data={
                'user': user_info,
                # Token de sesión simulado / demostrativo para el frontend
                'token': f"edupapel_token_{user.id}_{user.username}"
            },
            message="Inicio de sesión exitoso.",
            status_code=200
        )

