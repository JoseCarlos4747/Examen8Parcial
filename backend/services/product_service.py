"""
Servicio de Productos / Útiles Escolares.
Aplica POO (Hereda de BaseService) y Principio de Responsabilidad Única (SRP).
Encapsula todas las reglas de negocio y operaciones de base de datos para el CRUD escolar.
"""
from models.product_model import Product
from services.base_service import BaseService
from security.sanitizer import InputSanitizer


class ProductService(BaseService):
    """
    Gestiona el ciclo de vida de los útiles escolares:
    obtener catálogo, búsquedas, filtrado por categoría, creación, edición y eliminación.
    """

    def get_all(self, search: str = "", category: str = ""):
        """
        Retorna la lista de productos disponibles con soporte opcional de búsqueda y categoría.
        """
        query = Product.select().where(Product.is_active == True)

        # Sanitizar parámetros de consulta
        search = InputSanitizer.sanitize_string(search)
        category = InputSanitizer.sanitize_string(category)

        if category and category.lower() != 'todas':
            query = query.where(Product.category == category)

        if search:
            # Búsqueda parametrizada segura en nombre o código SKU
            query = query.where(
                (Product.name.contains(search)) |
                (Product.sku.contains(search)) |
                (Product.description.contains(search))
            )

        products = [p.to_dict() for p in query.order_by(Product.name.asc())]
        return self.success_response(
            data=products,
            message=f"Se obtuvieron {len(products)} productos exitosamente.",
            status_code=200
        )

    def get_by_id(self, product_id: int):
        """
        Retorna los detalles de un útil escolar por su ID primario.
        """
        try:
            product = Product.get_or_none((Product.id == product_id) & (Product.is_active == True))
            if not product:
                return self.error_response(message="Útil escolar no encontrado.", status_code=404)
            return self.success_response(data=product.to_dict(), status_code=200)
        except Exception as ex:
            return self.error_response(message=f"Error al consultar producto: {str(ex)}", status_code=500)

    def create(self, payload: dict):
        """
        Valida, sanitiza y crea un nuevo útil escolar en el inventario.
        """
        is_valid, error_msg, clean_data = InputSanitizer.validate_product_payload(payload)
        if not is_valid:
            return self.error_response(message=error_msg, status_code=400)

        # Verificar unicidad del SKU (código de producto)
        sku = clean_data['sku']
        if Product.select().where(Product.sku == sku).exists():
            return self.error_response(
                message=f"Ya existe un producto registrado con el código SKU '{sku}'.",
                status_code=409
            )

        try:
            new_product = Product.create(
                sku=clean_data['sku'],
                name=clean_data['name'],
                category=clean_data['category'],
                price=clean_data['price'],
                stock=clean_data['stock'],
                description=clean_data['description'],
                image_url=clean_data['image_url'],
                is_active=True
            )
            return self.success_response(
                data=new_product.to_dict(),
                message="Útil escolar registrado exitosamente.",
                status_code=201
            )
        except Exception as ex:
            return self.error_response(
                message=f"Error al guardar el producto en la base de datos: {str(ex)}",
                status_code=500
            )

    def update(self, product_id: int, payload: dict):
        """
        Valida, sanitiza y actualiza la información de un producto existente.
        """
        try:
            product = Product.get_or_none((Product.id == product_id) & (Product.is_active == True))
            if not product:
                return self.error_response(message="El producto a actualizar no existe.", status_code=404)

            is_valid, error_msg, clean_data = InputSanitizer.validate_product_payload(payload)
            if not is_valid:
                return self.error_response(message=error_msg, status_code=400)

            # Verificar si el SKU cambió y si ya está en uso por otro producto
            new_sku = clean_data['sku']
            if new_sku != product.sku:
                if Product.select().where((Product.sku == new_sku) & (Product.id != product_id)).exists():
                    return self.error_response(
                        message=f"El código SKU '{new_sku}' ya está asignado a otro producto.",
                        status_code=409
                    )

            # Actualizar campos
            product.sku = clean_data['sku']
            product.name = clean_data['name']
            product.category = clean_data['category']
            product.price = clean_data['price']
            product.stock = clean_data['stock']
            product.description = clean_data['description']
            product.image_url = clean_data['image_url']
            product.save()

            return self.success_response(
                data=product.to_dict(),
                message="Útil escolar actualizado con éxito.",
                status_code=200
            )
        except Exception as ex:
            return self.error_response(
                message=f"Error al actualizar el producto: {str(ex)}",
                status_code=500
            )

    def delete(self, product_id: int):
        """
        Elimina un útil escolar del inventario.
        """
        try:
            product = Product.get_or_none(Product.id == product_id)
            if not product:
                return self.error_response(message="El producto no existe o ya fue eliminado.", status_code=404)

            # Eliminación física segura o soft-delete
            product.delete_instance()
            return self.success_response(
                data={'id': product_id},
                message="Útil escolar eliminado correctamente del sistema.",
                status_code=200
            )
        except Exception as ex:
            return self.error_response(
                message=f"Error al eliminar el producto: {str(ex)}",
                status_code=500
            )

