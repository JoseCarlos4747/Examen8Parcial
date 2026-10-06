"""
Módulo de Seguridad: Sanitización y Validación de Entradas (OWASP Top 10).
Semana 8: Mitiga vulnerabilidades de Cross-Site Scripting (XSS) e inyecciones
mediante limpieza estricta y validación de tipos antes de procesar cualquier dato.
"""
import re
import html


class InputSanitizer:
    """
    Clase para la sanitización y validación defensiva de datos ingresados por el usuario.
    Aplica el Principio de Responsabilidad Única (SRP).
    """

    @staticmethod
    def sanitize_string(text: str, max_length: int = 255) -> str:
        """
        Limpia un texto eliminando espacios sobrantes y escapando caracteres peligrosos
        para neutralizar inyecciones XSS (Cross-Site Scripting).
        """
        if text is None:
            return ""
        # Convertir a cadena y eliminar espacios en los extremos
        cleaned = str(text).strip()
        # Truncar si excede la longitud permitida
        cleaned = cleaned[:max_length]
        # Escapar caracteres HTML especiales (&, <, >, ", ') para evitar ejecución de scripts
        return html.escape(cleaned)

    @staticmethod
    def validate_product_payload(data: dict) -> tuple[bool, str, dict]:
        """
        Valida y sanitiza los campos de un producto antes de guardarlo en la base de datos.
        :param data: Diccionario con los datos recibidos del cliente.
        :return: Tupla (es_valido: bool, mensaje_error: str, datos_limpios: dict)
        """
        if not isinstance(data, dict):
            return False, "El cuerpo de la solicitud debe ser un objeto JSON válido.", {}

        # 1. Validación de SKU
        sku_raw = data.get('sku', '')
        sku = InputSanitizer.sanitize_string(sku_raw, max_length=30).upper()
        if not sku:
            return False, "El campo 'sku' (código de producto) es obligatorio.", {}

        # 2. Validación de Nombre
        name_raw = data.get('name', '')
        name = InputSanitizer.sanitize_string(name_raw, max_length=150)
        if len(name) < 3:
            return False, "El nombre del útil escolar debe tener al menos 3 caracteres.", {}

        # 3. Validación de Categoría
        category_raw = data.get('category', '')
        category = InputSanitizer.sanitize_string(category_raw, max_length=60)
        if not category:
            return False, "La categoría es obligatoria.", {}

        # 4. Validación de Precio
        price_raw = data.get('price')
        try:
            price = float(price_raw)
            if price <= 0:
                return False, "El precio debe ser un número mayor a 0.", {}
            price = round(price, 2)
        except (ValueError, TypeError):
            return False, "El precio proporcionado no es un número válido.", {}

        # 5. Validación de Stock
        stock_raw = data.get('stock')
        try:
            stock = int(stock_raw)
            if stock < 0:
                return False, "El stock no puede ser un número negativo.", {}
        except (ValueError, TypeError):
            return False, "El stock debe ser un número entero mayor o igual a 0.", {}

        # 6. Descripción e imagen
        description = InputSanitizer.sanitize_string(data.get('description', ''), max_length=500)
        image_url = InputSanitizer.sanitize_string(data.get('image_url', ''), max_length=255)

        cleaned_data = {
            'sku': sku,
            'name': name,
            'category': category,
            'price': price,
            'stock': stock,
            'description': description,
            'image_url': image_url
        }

        return True, "", cleaned_data

    @staticmethod
    def validate_user_payload(data: dict) -> tuple[bool, str, dict]:
        """
        Valida y sanitiza las credenciales de registro/login de usuario.
        """
        if not isinstance(data, dict):
            return False, "El cuerpo de la solicitud debe ser un objeto JSON válido.", {}

        username = InputSanitizer.sanitize_string(data.get('username', ''), max_length=50)
        email = InputSanitizer.sanitize_string(data.get('email', ''), max_length=120).lower()
        password = str(data.get('password', '')).strip()

        if len(username) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres.", {}

        # Validación simple de formato de correo
        email_regex = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(email_regex, email):
            return False, "El formato del correo electrónico no es válido.", {}

        if len(password) < 6:
            return False, "La contraseña debe tener un mínimo de 6 caracteres.", {}

        return True, "", {
            'username': username,
            'email': email,
            'password': password
        }

