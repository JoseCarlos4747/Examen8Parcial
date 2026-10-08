"""
Controlador / Rutas del Catálogo de Útiles Escolares.
Aplica SRP: Recibe peticiones HTTP (GET, POST, PUT, DELETE), delega en ProductService
y retorna respuestas JSON con los códigos de estado HTTP apropiados (200, 201, 400, 404, etc.).
"""
from flask import Blueprint, request, jsonify
from services.product_service import ProductService

product_bp = Blueprint('product_bp', __name__, url_prefix='/api/products')
product_service = ProductService()


@product_bp.route('', methods=['GET'])
def get_products():
    """
    Lista todos los útiles escolares con soporte opcional de búsqueda y filtro por categoría.
    GET /api/products?search=cuaderno&category=Cuadernos
    """
    search = request.args.get('search', default='', type=str)
    category = request.args.get('category', default='', type=str)
    response_data, status_code = product_service.get_all(search=search, category=category)
    return jsonify(response_data), status_code


@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id: int):
    """
    Obtiene el detalle de un útil escolar específico por ID.
    GET /api/products/1
    """
    response_data, status_code = product_service.get_by_id(product_id)
    return jsonify(response_data), status_code


@product_bp.route('', methods=['POST'])
def create_product():
    """
    Crea un nuevo útil escolar en el sistema.
    POST /api/products
    """
    payload = request.get_json(silent=True) or {}
    response_data, status_code = product_service.create(payload)
    return jsonify(response_data), status_code


@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id: int):
    """
    Actualiza la información de un útil escolar existente.
    PUT /api/products/1
    """
    payload = request.get_json(silent=True) or {}
    response_data, status_code = product_service.update(product_id, payload)
    return jsonify(response_data), status_code


@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int):
    """
    Elimina un útil escolar del sistema.
    DELETE /api/products/1
    """
    response_data, status_code = product_service.delete(product_id)
    return jsonify(response_data), status_code

