"""
Módulo de Seguridad: Sanitización y Validación de Entradas (OWASP Top 10).
Semana 8: Mitiga vulnerabilidades de Cross-Site Scripting (XSS) e inyecciones.
Nombres de clases, métodos y variables en español.
"""
import re
import html


class SanitizadorEntradas:
    """
    Clase para la sanitización y validación defensiva de datos ingresados por el usuario.
    Aplica el Principio de Responsabilidad Única (SRP).
    """

    @staticmethod
    def limpiar_cadena(texto: str, longitud_maxima: int = 255) -> str:
        """
        Limpia un texto eliminando espacios sobrantes y escapando caracteres peligrosos
        para neutralizar inyecciones XSS (Cross-Site Scripting).
        """
        if texto is None:
            return ""
        cadena_limpia = str(texto).strip()
        cadena_limpia = cadena_limpia[:longitud_maxima]
        return html.escape(cadena_limpia)

    @staticmethod
    def validar_datos_producto(datos: dict) -> tuple[bool, str, dict]:
        """
        Valida y sanitiza los campos de un producto antes de guardarlo en la base de datos.
        Acepta nombres en español y alternativos por flexibilidad.
        :param datos: Diccionario con los datos recibidos del cliente.
        :return: Tupla (es_valido: bool, mensaje_error: str, datos_limpios: dict)
        """
        if not isinstance(datos, dict):
            return False, "El cuerpo de la solicitud debe ser un objeto JSON válido.", {}

        # 1. Validación de Código SKU
        sku_original = datos.get('codigo_sku') or datos.get('sku') or ''
        codigo_sku = SanitizadorEntradas.limpiar_cadena(sku_original, longitud_maxima=30).upper()
        if not codigo_sku:
            return False, "El código SKU del producto es obligatorio.", {}

        # 2. Validación de Nombre
        nombre_original = datos.get('nombre') or datos.get('name') or ''
        nombre = SanitizadorEntradas.limpiar_cadena(nombre_original, longitud_maxima=150)
        if len(nombre) < 3:
            return False, "El nombre del útil escolar debe tener al menos 3 caracteres.", {}

        # 3. Validación de Categoría
        categoria_original = datos.get('categoria') or datos.get('category') or ''
        categoria = SanitizadorEntradas.limpiar_cadena(categoria_original, longitud_maxima=60)
        if not categoria:
            return False, "La categoría es obligatoria.", {}

        # 4. Validación de Precio
        precio_original = datos.get('precio') if datos.get('precio') is not None else datos.get('price')
        try:
            precio_numero = float(precio_original)
            if precio_numero <= 0:
                return False, "El precio debe ser un número mayor a 0.", {}
            precio_final = round(precio_numero, 2)
        except (ValueError, TypeError):
            return False, "El precio proporcionado no es un número válido.", {}

        # 5. Validación de Stock
        stock_original = datos.get('stock')
        try:
            stock_entero = int(stock_original)
            if stock_entero < 0:
                return False, "El stock no puede ser un número negativo.", {}
        except (ValueError, TypeError):
            return False, "El stock debe ser un número entero mayor o igual a 0.", {}

        # 6. Descripción e Imagen
        descripcion_original = datos.get('descripcion') or datos.get('description') or ''
        descripcion = SanitizadorEntradas.limpiar_cadena(descripcion_original, longitud_maxima=500)

        imagen_original = datos.get('imagen_url') or datos.get('image_url') or ''
        imagen_url = SanitizadorEntradas.limpiar_cadena(imagen_original, longitud_maxima=255)

        datos_limpios = {
            'codigo_sku': codigo_sku,
            'nombre': nombre,
            'categoria': categoria,
            'precio': precio_final,
            'stock': stock_entero,
            'descripcion': descripcion,
            'imagen_url': imagen_url
        }

        return True, "", datos_limpios

    @staticmethod
    def validar_datos_usuario(datos: dict) -> tuple[bool, str, dict]:
        """
        Valida y sanitiza las credenciales de registro/login de usuario.
        """
        if not isinstance(datos, dict):
            return False, "El cuerpo de la solicitud debe ser un objeto JSON válido.", {}

        usuario_raw = datos.get('nombre_usuario') or datos.get('username') or ''
        nombre_usuario = SanitizadorEntradas.limpiar_cadena(usuario_raw, longitud_maxima=50)

        correo_raw = datos.get('correo') or datos.get('email') or ''
        correo = SanitizadorEntradas.limpiar_cadena(correo_raw, longitud_maxima=120).lower()

        clave = str(datos.get('clave') or datos.get('password') or datos.get('contrasena') or '').strip()

        if len(nombre_usuario) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres.", {}

        patron_correo = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(patron_correo, correo):
            return False, "El formato del correo electrónico no es válido.", {}

        if len(clave) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres.", {}

        return True, "", {
            'nombre_usuario': nombre_usuario,
            'correo': correo,
            'clave': clave
        }

    # Alias para compatibilidad
    sanitize_string = limpiar_cadena
    validate_product_payload = validar_datos_producto
    validate_user_payload = validar_datos_usuario


# Alias de clase
InputSanitizer = SanitizadorEntradas
