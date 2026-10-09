"""
Servicio de Autenticación y Cuentas de Usuario.
Aplica POO (Hereda de ServicioBase) y Principios SOLID (SRP).
Utiliza EncriptadorClaves (bcrypt) y SanitizadorEntradas para seguridad (OWASP).
Variables, métodos y parámetros en español.
"""
from models.user_model import Usuario
from services.base_service import ServicioBase
from security.hasher import EncriptadorClaves
from security.sanitizer import SanitizadorEntradas


class ServicioAutenticacion(ServicioBase):
    """
    Gestiona la lógica de negocio de usuarios:
    registro seguro con bcrypt y validación de credenciales en el inicio de sesión.
    """

    def registrar(self, datos: dict):
        """
        Registra un nuevo usuario en la base de datos con contraseña hasheada.
        """
        es_valido, mensaje_error, datos_limpios = SanitizadorEntradas.validar_datos_usuario(datos)
        if not es_valido:
            return self.respuesta_error(mensaje=mensaje_error, codigo_estado=400)

        nombre_usuario = datos_limpios['nombre_usuario']
        correo = datos_limpios['correo']
        clave_plana = datos_limpios['clave']

        # Verificación segura anti-SQLi usando Peewee ORM
        usuario_existente = Usuario.select().where(
            (Usuario.nombre_usuario == nombre_usuario) | (Usuario.correo == correo)
        ).exists()

        if usuario_existente:
            return self.respuesta_error(
                mensaje="El nombre de usuario o correo electrónico ya se encuentra registrado.",
                codigo_estado=409
            )

        try:
            # Hashing seguro con bcrypt
            clave_encriptada = EncriptadorClaves.hashear_clave(clave_plana)

            nuevo_usuario = Usuario.create(
                nombre_usuario=nombre_usuario,
                correo=correo,
                clave_hash=clave_encriptada,
                rol='admin'
            )

            return self.respuesta_exitosa(
                datos=nuevo_usuario.a_diccionario(incluir_sensible=False),
                mensaje="Usuario registrado exitosamente.",
                codigo_estado=201
            )
        except Exception as error_excepcion:
            return self.respuesta_error(
                mensaje=f"Error al registrar usuario: {str(error_excepcion)}",
                codigo_estado=500
            )

    def iniciar_sesion(self, datos: dict):
        """
        Valida las credenciales del usuario y verifica el hash bcrypt.
        """
        if not isinstance(datos, dict):
            return self.respuesta_error(mensaje="Formato de datos no válido.", codigo_estado=400)

        identificador_crudo = (
            datos.get('identificador') or
            datos.get('identifier') or
            datos.get('correo') or
            datos.get('email') or
            datos.get('usuario') or
            datos.get('username') or
            ''
        )
        identificador = SanitizadorEntradas.limpiar_cadena(identificador_crudo).lower()
        clave = str(datos.get('clave') or datos.get('password') or datos.get('contrasena') or '').strip()

        if not identificador or not clave:
            return self.respuesta_error(
                mensaje="Debe ingresar su usuario o correo y su contraseña.",
                codigo_estado=400
            )

        # Buscar usuario en SQLite mediante consulta parametrizada
        usuario_encontrado = Usuario.get_or_none(
            (Usuario.correo == identificador) | (Usuario.nombre_usuario == identificador)
        )

        if not usuario_encontrado or not usuario_encontrado.esta_activo:
            return self.respuesta_error(
                mensaje="Credenciales incorrectas o usuario no encontrado.",
                codigo_estado=401
            )

        # Verificación criptográfica con bcrypt
        clave_es_correcta = EncriptadorClaves.verificar_clave(clave, usuario_encontrado.clave_hash)
        if not clave_es_correcta:
            return self.respuesta_error(
                mensaje="Credenciales incorrectas o usuario no encontrado.",
                codigo_estado=401
            )

        datos_usuario = usuario_encontrado.a_diccionario(incluir_sensible=False)
        return self.respuesta_exitosa(
            datos={
                'usuario': datos_usuario,
                'user': datos_usuario,
                'token': f"token_edupapel_{usuario_encontrado.id}_{usuario_encontrado.nombre_usuario}"
            },
            mensaje="Inicio de sesión exitoso.",
            codigo_estado=200
        )

    # Alias para compatibilidad
    register = registrar
    login = iniciar_sesion


# Alias de clase
AuthService = ServicioAutenticacion
