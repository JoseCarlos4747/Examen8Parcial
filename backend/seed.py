"""
Script de Semillado para la base de datos de EduPapel.
Inserta productos escolares de prueba y un usuario administrador con contraseña hasheada (bcrypt).
Nombres de variables, funciones y estructuras en español.
"""
from database import inicializar_base_datos
from models.user_model import Usuario
from models.product_model import Producto
from security.hasher import EncriptadorClaves

PRODUCTOS_INICIALES = [
    {
        "codigo_sku": "CUAD-001",
        "nombre": "Cuaderno Standford Cuadriculado 100 Hojas",
        "categoria": "Cuadernos",
        "precio": 5.50,
        "stock": 80,
        "descripcion": "Cuaderno espiral tamaño A4 con hojas cuadriculadas de 75g y carátula plastificada gruesa.",
        "imagen_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&auto=format&fit=crop&q=80"
    },
    {
        "codigo_sku": "CUAD-002",
        "nombre": "Cuaderno Loro Rayado 100 Hojas",
        "categoria": "Cuadernos",
        "precio": 4.80,
        "stock": 65,
        "descripcion": "Cuaderno grapado con margen rojo, ideal para nivel primario y secundario.",
        "imagen_url": "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400&auto=format&fit=crop&q=80"
    },
    {
        "codigo_sku": "ESC-001",
        "nombre": "Lapiceros Faber-Castell Trilux 032 Caja x12",
        "categoria": "Escritura",
        "precio": 14.00,
        "stock": 40,
        "descripcion": "Caja de 12 bolígrafos ergonómicos color azul punta media 1.0mm.",
        "imagen_url": "https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=400&auto=format&fit=crop&q=80"
    },
    {
        "codigo_sku": "ESC-002",
        "nombre": "Lápices de Grafito 2B Artesco Blíster x4",
        "categoria": "Escritura",
        "precio": 3.50,
        "stock": 120,
        "descripcion": "Lápices hexagonales de grafito suave con borrador libre de látex incorporado.",
        "imagen_url": "https://images.unsplash.com/photo-1516962215378-7fa2e137ae93?w=400&auto=format&fit=crop&q=80"
    },
    {
        "codigo_sku": "ART-001",
        "nombre": "Ecolápices de Color Faber-Castell x24 Colores",
        "categoria": "Arte y Dibujo",
        "precio": 22.90,
        "stock": 35,
        "descripcion": "Lápices de madera reforestada con mina super resistente y colores vivos.",
        "imagen_url": "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=400&auto=format&fit=crop&q=80"
    },
    {
        "codigo_sku": "ART-002",
        "nombre": "Témperas Vinifan Set 6 Frascos + Pincel",
        "categoria": "Arte y Dibujo",
        "precio": 8.50,
        "stock": 50,
        "descripcion": "Pintura lavable no tóxica con excelente cobertura para proyectos escolares.",
        "imagen_url": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=400&auto=format&fit=crop&q=80"
    },
    {
        "codigo_sku": "GEO-001",
        "nombre": "Juego de Reglas Geométricas 30cm Cristal",
        "categoria": "Geometría",
        "precio": 7.20,
        "stock": 60,
        "descripcion": "Kit de regla 30cm, escuadra 45°, cartabón 60° y transportador 180° de plástico flexible.",
        "imagen_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400&auto=format&fit=crop&q=80"
    },
    {
        "codigo_sku": "GEO-002",
        "nombre": "Compás Escolar de Precisión Metálico",
        "categoria": "Geometría",
        "precio": 9.50,
        "stock": 30,
        "descripcion": "Compás con adaptador universal y minas de repuesto en estuche rígido protector.",
        "imagen_url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=400&auto=format&fit=crop&q=80"
    },
    {
        "codigo_sku": "MOC-001",
        "nombre": "Mochila Escolar Ergonómica Reforzada",
        "categoria": "Mochilas y Cartucheras",
        "precio": 89.90,
        "stock": 15,
        "descripcion": "Mochila con soporte lumbar acolchado, repelente al agua y compartimento para laptop/tablet.",
        "imagen_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&auto=format&fit=crop&q=80"
    },
    {
        "codigo_sku": "MOC-002",
        "nombre": "Cartuchera Doble Compartimiento Escolar",
        "categoria": "Mochilas y Cartucheras",
        "precio": 18.00,
        "stock": 45,
        "descripcion": "Cartuchera de lona lavable de alta capacidad con cierres reforzados.",
        "imagen_url": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400&auto=format&fit=crop&q=80"
    },
    {
        "codigo_sku": "PAP-001",
        "nombre": "Papel Bond A4 75g Paquete 500 Hojas",
        "categoria": "Papelería General",
        "precio": 17.50,
        "stock": 55,
        "descripcion": "Resma de papel blanco de alta blancura y excelente desempeño en impresoras y fotocopias.",
        "imagen_url": "https://images.unsplash.com/photo-1586075010923-2dd4570fb338?w=400&auto=format&fit=crop&q=80"
    },
    {
        "codigo_sku": "PAP-002",
        "nombre": "Tijera Escolar Punta Roma 5 Pulgadas",
        "categoria": "Papelería General",
        "precio": 3.20,
        "stock": 90,
        "descripcion": "Hojas de acero inoxidable con punta roma de seguridad y mango ergonómico suave.",
        "imagen_url": "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400&auto=format&fit=crop&q=80"
    }
]


def sembrar_base_datos():
    """Ejecuta la inicialización de tablas y carga datos de prueba."""
    print("Iniciando creacion de tablas en SQLite...")
    inicializar_base_datos([Usuario, Producto])
    print("Tablas verificadas con exito.")

    # 1. Crear usuario administrador con contraseña hasheada (Semana 8: bcrypt)
    nombre_admin = "admin"
    correo_admin = "admin@edupapel.com"
    clave_admin = "admin123"

    usuario_existente = Usuario.get_or_none(Usuario.nombre_usuario == nombre_admin)
    if not usuario_existente:
        print("Creando usuario administrador con hash seguro bcrypt...")
        clave_hasheada = EncriptadorClaves.hashear_clave(clave_admin)
        Usuario.create(
            nombre_usuario=nombre_admin,
            correo=correo_admin,
            clave_hash=clave_hasheada,
            rol="admin"
        )
        print(f"Usuario '{nombre_admin}' creado exitosamente (clave: {clave_admin}).")
    else:
        print(f"El usuario '{nombre_admin}' ya existe en la base de datos.")

    # 2. Insertar productos de útiles escolares
    cantidad_creados = 0
    for datos_prod in PRODUCTOS_INICIALES:
        if not Producto.get_or_none(Producto.codigo_sku == datos_prod['codigo_sku']):
            Producto.create(**datos_prod)
            cantidad_creados += 1

    print(f"Semillado completado: {cantidad_creados} nuevos utiles escolares insertados.")


# Alias
INITIAL_PRODUCTS = PRODUCTOS_INICIALES
seed_database = sembrar_base_datos

if __name__ == '__main__':
    sembrar_base_datos()
