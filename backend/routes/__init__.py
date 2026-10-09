"""Paquete de Rutas / Controladores en Español."""
from routes.auth_routes import rutas_autenticacion, auth_bp
from routes.product_routes import rutas_productos, product_bp

__all__ = ['rutas_autenticacion', 'auth_bp', 'rutas_productos', 'product_bp']
