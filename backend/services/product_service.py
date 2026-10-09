"""
Servicio de Productos / Útiles Escolares.
Aplica POO (Hereda de ServicioBase) y Principio de Responsabilidad Única (SRP).
Encapsula todas las reglas de negocio y operaciones sobre útiles escolares.
Variables, métodos y parámetros en español.
"""
from models.product_model import Producto
from services.base_service import ServicioBase
from security.sanitizer import SanitizadorEntradas


class ServicioProducto(ServicioBase):
    """
    Gestiona el ciclo de vida de los útiles escolares:
    obtener catálogo, búsquedas, filtrado por categoría, creación, edición y eliminación.
    """

    def obtener_todos(self, busqueda: str = "", categoria: str = ""):
        """
        Retorna la lista de productos disponibles con soporte opcional de búsqueda y categoría.
        """
        consulta = Producto.select().where(Producto.esta_activo == True)

        # Sanitizar parámetros de consulta
        busqueda_limpia = SanitizadorEntradas.limpiar_cadena(busqueda)
        categoria_limpia = SanitizadorEntradas.limpiar_cadena(categoria)

        if categoria_limpia and categoria_limpia.lower() != 'todas':
            consulta = consulta.where(Producto.categoria == categoria_limpia)

        if busqueda_limpia:
            # Búsqueda parametrizada segura en nombre, SKU o descripción
            consulta = consulta.where(
                (Producto.nombre.contains(busqueda_limpia)) |
                (Producto.codigo_sku.contains(busqueda_limpia)) |
                (Producto.descripcion.contains(busqueda_limpia))
            )

        lista_productos = [prod.a_diccionario() for prod in consulta.order_by(Producto.nombre.asc())]
        return self.respuesta_exitosa(
            datos=lista_productos,
            mensaje=f"Se obtuvieron {len(lista_productos)} útiles escolares exitosamente.",
            codigo_estado=200
        )

    def obtener_por_id(self, id_producto: int):
        """
        Retorna los detalles de un útil escolar por su ID numérico.
        """
        try:
            producto = Producto.get_or_none((Producto.id == id_producto) & (Producto.esta_activo == True))
            if not producto:
                return self.respuesta_error(mensaje="Útil escolar no encontrado.", codigo_estado=404)
            return self.respuesta_exitosa(datos=producto.a_diccionario(), codigo_estado=200)
        except Exception as error_excepcion:
            return self.respuesta_error(
                mensaje=f"Error al consultar producto: {str(error_excepcion)}",
                codigo_estado=500
            )

    def crear(self, datos: dict):
        """
        Valida, sanitiza y crea un nuevo útil escolar en el inventario.
        """
        es_valido, mensaje_error, datos_limpios = SanitizadorEntradas.validar_datos_producto(datos)
        if not es_valido:
            return self.respuesta_error(mensaje=mensaje_error, codigo_estado=400)

        # Verificar si el código SKU ya existe
        sku_a_verificar = datos_limpios['codigo_sku']
        if Producto.select().where(Producto.codigo_sku == sku_a_verificar).exists():
            return self.respuesta_error(
                mensaje=f"Ya existe un producto registrado con el código SKU '{sku_a_verificar}'.",
                codigo_estado=409
            )

        try:
            nuevo_producto = Producto.create(
                codigo_sku=datos_limpios['codigo_sku'],
                nombre=datos_limpios['nombre'],
                categoria=datos_limpios['categoria'],
                precio=datos_limpios['precio'],
                stock=datos_limpios['stock'],
                descripcion=datos_limpios['descripcion'],
                imagen_url=datos_limpios['imagen_url'],
                esta_activo=True
            )
            return self.respuesta_exitosa(
                datos=nuevo_producto.a_diccionario(),
                mensaje="Útil escolar registrado exitosamente.",
                codigo_estado=201
            )
        except Exception as error_excepcion:
            return self.respuesta_error(
                mensaje=f"Error al guardar el producto: {str(error_excepcion)}",
                codigo_estado=500
            )

    def actualizar(self, id_producto: int, datos: dict):
        """
        Valida, sanitiza y actualiza la información de un producto existente.
        """
        try:
            producto_existente = Producto.get_or_none((Producto.id == id_producto) & (Producto.esta_activo == True))
            if not producto_existente:
                return self.respuesta_error(mensaje="El producto a actualizar no existe.", codigo_estado=404)

            es_valido, mensaje_error, datos_limpios = SanitizadorEntradas.validar_datos_producto(datos)
            if not es_valido:
                return self.respuesta_error(mensaje=mensaje_error, codigo_estado=400)

            # Verificar si el código SKU cambió y colisiona con otro registro
            nuevo_sku = datos_limpios['codigo_sku']
            if nuevo_sku != producto_existente.codigo_sku:
                if Producto.select().where((Producto.codigo_sku == nuevo_sku) & (Producto.id != id_producto)).exists():
                    return self.respuesta_error(
                        mensaje=f"El código SKU '{nuevo_sku}' ya está asignado a otro producto.",
                        codigo_estado=409
                    )

            # Actualizar campos
            producto_existente.codigo_sku = datos_limpios['codigo_sku']
            producto_existente.nombre = datos_limpios['nombre']
            producto_existente.categoria = datos_limpios['categoria']
            producto_existente.precio = datos_limpios['precio']
            producto_existente.stock = datos_limpios['stock']
            producto_existente.descripcion = datos_limpios['descripcion']
            producto_existente.imagen_url = datos_limpios['imagen_url']
            producto_existente.save()

            return self.respuesta_exitosa(
                datos=producto_existente.a_diccionario(),
                mensaje="Útil escolar actualizado con éxito.",
                codigo_estado=200
            )
        except Exception as error_excepcion:
            return self.respuesta_error(
                mensaje=f"Error al actualizar el producto: {str(error_excepcion)}",
                codigo_estado=500
            )

    def eliminar(self, id_producto: int):
        """
        Elimina un útil escolar del inventario.
        """
        try:
            producto_a_borrar = Producto.get_or_none(Producto.id == id_producto)
            if not producto_a_borrar:
                return self.respuesta_error(mensaje="El producto no existe o ya fue eliminado.", codigo_estado=404)

            producto_a_borrar.delete_instance()
            return self.respuesta_exitosa(
                datos={'id': id_producto},
                mensaje="Útil escolar eliminado correctamente del sistema.",
                codigo_estado=200
            )
        except Exception as error_excepcion:
            return self.respuesta_error(
                mensaje=f"Error al eliminar el producto: {str(error_excepcion)}",
                codigo_estado=500
            )

    # Alias para compatibilidad
    get_all = obtener_todos
    get_by_id = obtener_por_id
    create = crear
    update = actualizar
    delete = eliminar


# Alias de clase
ProductService = ServicioProducto
