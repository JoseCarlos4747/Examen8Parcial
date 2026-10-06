"""Paquete de Rutas / Controladores."""
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp

__all__ = ['auth_bp', 'product_bp']

