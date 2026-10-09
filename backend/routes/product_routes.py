"""
Controlador / Rutas del Catálogo de Útiles Escolares.
Aplica SRP: Recibe peticiones HTTP (GET, POST, PUT, DELETE), delega en ServicioProducto
y retorna respuestas JSON con los códigos de estado HTTP apropiados (200, 201, 400, 404, etc.).
Variables, funciones y parámetros en español.
"""
from flask import Blueprint, request, jsonify
from services.product_service import ServicioProducto

rutas_productos = Blueprint('rutas_productos', __name__, url_prefix='/api/products')
servicio_producto = ServicioProducto()


@rutas_productos.route('', methods=['GET'])
def listar_productos():
    """
    Lista todos los útiles escolares con soporte opcional de búsqueda y filtro por categoría.
    GET /api/products?search=cuaderno&category=Cuadernos
    GET /api/products?busqueda=cuaderno&categoria=Cuadernos
    """
    parametro_busqueda = request.args.get('busqueda') or request.args.get('search', default='', type=str)
    parametro_categoria = request.args.get('categoria') or request.args.get('category', default='', type=str)

    respuesta_datos, codigo_estado = servicio_producto.obtener_todos(
        busqueda=parametro_busqueda,
        categoria=parametro_categoria
    )
    return jsonify(respuesta_datos), codigo_estado


@rutas_productos.route('/<int:id_producto>', methods=['GET'])
def obtener_producto(id_producto: int):
    """
    Obtiene el detalle de un útil escolar específico por ID.
    GET /api/products/1
    """
    respuesta_datos, codigo_estado = servicio_producto.obtener_por_id(id_producto)
    return jsonify(respuesta_datos), codigo_estado


@rutas_productos.route('', methods=['POST'])
def crear_producto():
    """
    Crea un nuevo útil escolar en el sistema.
    POST /api/products
    """
    datos_recibidos = request.get_json(silent=True) or {}
    respuesta_datos, codigo_estado = servicio_producto.crear(datos_recibidos)
    return jsonify(respuesta_datos), codigo_estado


@rutas_productos.route('/<int:id_producto>', methods=['PUT'])
def actualizar_producto(id_producto: int):
    """
    Actualiza la información de un útil escolar existente.
    PUT /api/products/1
    """
    datos_recibidos = request.get_json(silent=True) or {}
    respuesta_datos, codigo_estado = servicio_producto.actualizar(id_producto, datos_recibidos)
    return jsonify(respuesta_datos), codigo_estado


@rutas_productos.route('/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto: int):
    """
    Elimina un útil escolar del sistema.
    DELETE /api/products/1
    """
    respuesta_datos, codigo_estado = servicio_producto.eliminar(id_producto)
    return jsonify(respuesta_datos), codigo_estado


# Alias para compatibilidad
product_bp = rutas_productos
