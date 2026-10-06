"""
Script de Semillado (Seeder) para la base de datos de EduPapel.
Inserta productos escolares de prueba y un usuario administrador con contraseña hasheada (bcrypt).
"""
from database import init_db, db
from models.user_model import User
from models.product_model import Product
from security.hasher import PasswordHasher

INITIAL_PRODUCTS = [
    {
        "sku": "CUAD-001",
        "name": "Cuaderno Standford Cuadriculado 100 Hojas",
        "category": "Cuadernos",
        "price": 5.50,
        "stock": 80,
        "description": "Cuaderno espiral tamaño A4 con hojas cuadriculadas de 75g y carátula plastificada gruesa.",
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&auto=format&fit=crop&q=80"
    },
    {
        "sku": "CUAD-002",
        "name": "Cuaderno Loro Rayado 100 Hojas",
        "category": "Cuadernos",
        "price": 4.80,
        "stock": 65,
        "description": "Cuaderno grapado con margen rojo, ideal para nivel primario y secundario.",
        "image_url": "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400&auto=format&fit=crop&q=80"
    },
    {
        "sku": "ESC-001",
        "name": "Lapiceros Faber-Castell Trilux 032 Caja x12",
        "category": "Escritura",
        "price": 14.00,
        "stock": 40,
        "description": "Caja de 12 bolígrafos ergonómicos color azul punta media 1.0mm.",
        "image_url": "https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=400&auto=format&fit=crop&q=80"
    },
    {
        "sku": "ESC-002",
        "name": "Lápices de Grafito 2B Artesco Blíster x4",
        "category": "Escritura",
        "price": 3.50,
        "stock": 120,
        "description": "Lápices hexagonales de grafito suave con borrador libre de látex incorporado.",
        "image_url": "https://images.unsplash.com/photo-1516962215378-7fa2e137ae93?w=400&auto=format&fit=crop&q=80"
    },
    {
        "sku": "ART-001",
        "name": "Ecolápices de Color Faber-Castell x24 Colores",
        "category": "Arte y Dibujo",
        "price": 22.90,
        "stock": 35,
        "description": "Lápices de madera reforestada con mina super resistente y colores vivos.",
        "image_url": "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=400&auto=format&fit=crop&q=80"
    },
    {
        "sku": "ART-002",
        "name": "Témperas Vinifan Set 6 Frascos + Pincel",
        "category": "Arte y Dibujo",
        "price": 8.50,
        "stock": 50,
        "description": "Pintura lavable no tóxica con excelente cobertura para proyectos escolares.",
        "image_url": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=400&auto=format&fit=crop&q=80"
    },
    {
        "sku": "GEO-001",
        "name": "Juego de Reglas Geométricas 30cm Cristal",
        "category": "Geometría",
        "price": 7.20,
        "stock": 60,
        "description": "Kit de regla 30cm, escuadra 45°, cartabón 60° y transportador 180° de plástico flexible.",
        "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400&auto=format&fit=crop&q=80"
    },
    {
        "sku": "GEO-002",
        "name": "Compás Escolar de Precisión Metálico",
        "category": "Geometría",
        "price": 9.50,
        "stock": 30,
        "description": "Compás con adaptador universal y minas de repuesto en estuche rígido protector.",
        "image_url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=400&auto=format&fit=crop&q=80"
    },
    {
        "sku": "MOC-001",
        "name": "Mochila Escolar Ergonómica Reforzada",
        "category": "Mochilas y Cartucheras",
        "price": 89.90,
        "stock": 15,
        "description": "Mochila con soporte lumbar acolchado, repelente al agua y compartimento para laptop/tablet.",
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&auto=format&fit=crop&q=80"
    },
    {
        "sku": "MOC-002",
        "name": "Cartuchera Doble Compartimiento Escolar",
        "category": "Mochilas y Cartucheras",
        "price": 18.00,
        "stock": 45,
        "description": "Cartuchera de lona lavable de alta capacidad con cierres reforzados.",
        "image_url": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400&auto=format&fit=crop&q=80"
    },
    {
        "sku": "PAP-001",
        "name": "Papel Bond A4 75g Paquete 500 Hojas",
        "category": "Papelería General",
        "price": 17.50,
        "stock": 55,
        "description": "Resma de papel blanco de alta blancura y excelente desempeño en impresoras y fotocopias.",
        "image_url": "https://images.unsplash.com/photo-1586075010923-2dd4570fb338?w=400&auto=format&fit=crop&q=80"
    },
    {
        "sku": "PAP-002",
        "name": "Tijera Escolar Punta Roma 5 Pulgadas",
        "category": "Papelería General",
        "price": 3.20,
        "stock": 90,
        "description": "Hojas de acero inoxidable con punta roma de seguridad y mango ergonómico suave.",
        "image_url": "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400&auto=format&fit=crop&q=80"
    }
]


def seed_database():
    """Ejecuta la inicialización de tablas y carga datos de prueba."""
    print("Iniciando creación de tablas...")
    init_db([User, Product])
    print("Tablas verificadas con éxito.")

    # 1. Crear usuario administrador con contraseña hasheada (Semana 8: bcrypt)
    admin_username = "admin"
    admin_email = "admin@edupapel.com"
    admin_password = "admin123"

    user = User.get_or_none(User.username == admin_username)
    if not user:
        print(f"Creando usuario administrador seguro con hash bcrypt...")
        hashed_pwd = PasswordHasher.hash_password(admin_password)
        User.create(
            username=admin_username,
            email=admin_email,
            password_hash=hashed_pwd,
            role="admin"
        )
        print(f"Usuario '{admin_username}' creado exitosamente (password: {admin_password}).")
    else:
        print(f"El usuario '{admin_username}' ya existe en la base de datos.")

    # 2. Insertar productos de útiles escolares
    created_count = 0
    for p_data in INITIAL_PRODUCTS:
        if not Product.get_or_none(Product.sku == p_data['sku']):
            Product.create(**p_data)
            created_count += 1

    print(f"Semillado completado: {created_count} nuevos útiles escolares insertados.")


if __name__ == '__main__':
    seed_database()

