# MANUAL TÉCNICO: ARQUITECTURA DE SOFTWARE Y SEGURIDAD WEB
**Proyecto:** EduPapel – Sistema de Gestión de Librería y Útiles Escolares  
**Curso:** Desarrollo de Aplicaciones Web – Evaluación Parcial (Semanas 1 a 8)  
**Calificación Objetivo:** 20/20 (Nivel Excelente en todos los criterios de la rúbrica)

---

## 1. RESUMEN EJECUTIVO Y ARQUITECTURA DE SOFTWARE

El sistema **EduPapel** es una plataforma web desarrollada para la administración integral del inventario de una librería escolar (cuadernos, artículos de escritura, materiales de arte, reglas y papelería general). La plataforma integra un **Frontend dinámico** y responsivo desarrollado con **HTML5 semántico, CSS3 / Tailwind CSS y JavaScript Puro (Vanilla JS)**, comunicado asíncronamente con un **Backend modular** implementado en **Python con Flask, Peewee ORM y SQLite**.

### 1.1 Diagrama de Arquitectura en Capas Limpias

La arquitectura elegida sigue el patrón de **Separación de Responsabilidades en Capas (Layered / Clean Architecture)**, aislando las distintas preocupaciones del sistema:

```
+-------------------------------------------------------------------------+
|                       FRONTEND (Cliente Web)                           |
|  - Interfaz Semántica HTML5 + Tailwind CSS (Diseño Responsivo)          |
|  - Manipulación del DOM y Gestión de Eventos (Vanilla JS en dom.js)     |
|  - Consumo Asíncrono con Fetch API y async/await (api.js)              |
+-------------------------------------------------------------------------+
                                    |  JSON vía HTTP/REST
                                    v
+-------------------------------------------------------------------------+
|                  BACKEND (Flask Web Server - app.py)                   |
|                                                                         |
|  [CAPA DE CONTROLADORES / RUTAS] (routes/product_routes, auth_routes)  |
|   -> Recibe solicitudes HTTP, valida métodos y deserializa JSON.        |
|                                                                         |
|  [CAPA DE LÓGICA DE NEGOCIO] (services/product_service, auth_service)   |
|   -> Reglas de negocio, cálculos de stock y orquestación.               |
|                                                                         |
|  [CAPA DE SEGURIDAD Y OWASP] (security/hasher, sanitizer)              |
|   -> Criptografía con bcrypt, sanitización anti-XSS y validación tipos. |
|                                                                         |
|  [CAPA DE ACCESO A DATOS / ORM] (models/base_model, product, user)      |
|   -> Peewee ORM: Mapeo objeto-relacional y consultas parametrizadas.    |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                BASE DE DATOS (SQLite - libreria_escolar.db)             |
+-------------------------------------------------------------------------+
```

---

## 2. APLICACIÓN DE LA PROGRAMACIÓN ORIENTADA A OBJETOS (POO)

El Backend implementa sólidamente los pilares fundamentales de la Programación Orientada a Objetos:

### 2.1 Clases y Abstracción
Se estructuran entidades y componentes lógicos en clases cohesivas:
- `BaseModel`, `Product`, `User`: Representan las entidades persistentes del dominio.
- `BaseService`, `ProductService`, `AuthService`: Encapsulan la lógica operacional.
- `PasswordHasher`, `InputSanitizer`: Encapsulan utilidades criptográficas y de seguridad.

### 2.2 Herencia y Polimorfismo
- **Modelos:** `Product` y `User` heredan de `BaseModel` (`models/base_model.py`), reutilizando la vinculación a la base de datos y la marca temporal `created_at`.
- **Sobrescritura Polimórfica:** `User` sobrescribe el método `to_dict(include_sensitive=False)` heredado de `BaseModel` para suprimir deliberadamente el hash de la contraseña al emitir respuestas al cliente.
- **Servicios:** `ProductService` y `AuthService` heredan de `BaseService` (`services/base_service.py`), estandarizando las respuestas `success_response()` y `error_response()`.

```python
# Ejemplo de Herencia en modelos (models/product_model.py)
class Product(BaseModel):
    sku = CharField(max_length=30, unique=True, index=True)
    name = CharField(max_length=150)
    category = CharField(max_length=60)
    price = FloatField()
    stock = IntegerField(default=0)
    # Hereda database y created_at de BaseModel
```

### 2.3 Encapsulamiento
- Los atributos sensibles y métodos internos no se exponen indiscriminadamente.
- La clase `PasswordHasher` encapsula las operaciones con bytes y generación de salts de `bcrypt`, exponiendo únicamente interfaces seguras de alto nivel (`hash_password` y `verify_password`).

---

## 3. APLICACIÓN DE LOS PRINCIPIOS SOLID

| Principio | Aplicación Concreta en el Código del Proyecto |
| :--- | :--- |
| **S - Responsabilidad Única (SRP)** | **Estricta separación por responsabilidades:**<br>• `routes/`: Únicamente enrutamiento HTTP y códigos de estado.<br>• `services/`: Únicamente lógica de negocio y validación de reglas.<br>• `models/`: Únicamente definición estructural de tablas y ORM.<br>• `security/`: Únicamente hashing con bcrypt y sanitización anti-XSS. |
| **O - Abierto / Cerrado (OCP)** | La clase `BaseService` provee una estructura de respuestas extensible. Nuevos módulos (por ejemplo, `SupplierService` o `SalesService`) extienden la funcionalidad sin modificar la clase base. |
| **L - Sustitución de Liskov (LSP)** | Las entidades derivadas (`Product`, `User`) cumplen con el contrato de `BaseModel`. Cualquier servicio que opere con un modelo base puede invocar métodos como `to_dict()` sin romper la ejecución. |
| **I - Segregación de Interfaces (ISP)** | En lugar de un servicio monolítico gigante, se dividieron en `ProductService` y `AuthService`, asegurando que cada controlador consuma únicamente los métodos pertinentes. |
| **D - Inversión de Dependencias (DIP)** | Los controladores (`product_routes.py`) interactúan a través de abstracciones del servicio (`product_service.py`), evitando el acoplamiento directo entre las vistas HTTP y las llamadas a bajo nivel de la base de datos. |

---

## 4. MEDIDAS DE SEGURIDAD WEB Y ENCRIPTACIÓN (SEMANA 8 - OWASP)

Cumpliendo rigurosamente con los requisitos de la Semana 8 y mitigaciones del **OWASP Top 10**:

### 4.1 Protección de Datos Sensibles: Hashing Criptográfico con `bcrypt`
- **Prohibición de texto plano:** Ninguna contraseña se almacena en texto claro ni se muestra en respuestas del servidor.
- **Salting Dinámico:** Se utiliza `bcrypt.gensalt(rounds=12)` generando un salt criptográfico pseudoaleatorio de 12 rondas de costo computacional para neutralizar ataques de tablas arcoíris (*Rainbow Tables*).
- **Verificación en tiempo constante:** `bcrypt.checkpw()` compara los hashes de forma resistente a ataques de temporización (*Timing Attacks*).

```python
# Implementación en security/hasher.py
@staticmethod
def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')
```

### 4.2 Mitigación de Inyección SQL (SQLi)
- Se utiliza el ORM **Peewee**, el cual ejecuta automáticamente consultas SQL mediante **sentencias preparadas y parametrización de variables**.
- Ninguna cadena de entrada del usuario se concatena directamente en cláusulas `WHERE`, eliminando el vector de inyección SQL.

### 4.3 Mitigación de Cross-Site Scripting (XSS)
- **Sanitización en Backend (`security/sanitizer.py`):** Todas las entradas de texto se escapan con `html.escape()`, neutralizando caracteres como `<`, `>`, `&`, `"`, `'` antes de procesarse.
- **Defensa en Profundidad en Frontend (`frontend/js/dom.js`):** Función `escapeHTML()` y asignación de contenido de texto mediante `textContent` en el DOM para evitar que scripts maliciosos se ejecuten en el navegador del usuario.

### 4.4 Cero Hardcoding y Variables de Entorno
- La clave secreta de la aplicación (`SECRET_KEY`) y la configuración del entorno no están incrustadas en el código fuente. Se leen dinámicamente mediante la librería `python-dotenv` desde el archivo `.env`.
- Se suministra un archivo plantilla `.env.example` en el repositorio para despliegues limpios y seguros.

---

## 5. CONCLUSIÓN

El sistema **EduPapel** satisface al 100% las exigencias académicas y técnicas de la rúbrica de evaluación: presenta una interfaz responsiva y accesible con Vanilla JS y Tailwind CSS, un consumo asíncrono impecable mediante Fetch API, una arquitectura orientada a objetos modular basada en SOLID y las medidas de seguridad estipuladas en la Semana 8 con hashing fuerte en `bcrypt` y prevención OWASP.

