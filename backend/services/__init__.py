"""Paquete de Servicios de Lógica de Negocio con Nombres en Español."""
from services.base_service import ServicioBase, BaseService
from services.auth_service import ServicioAutenticacion, AuthService
from services.product_service import ServicioProducto, ProductService

__all__ = [
    'ServicioBase', 'BaseService',
    'ServicioAutenticacion', 'AuthService',
    'ServicioProducto', 'ProductService'
]
