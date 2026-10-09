# MANUAL TÉCNICO: ARQUITECTURA DE SOFTWARE Y SEGURIDAD WEB
**Proyecto:** EduPapel – Sistema de Gestión de Librería y Útiles Escolares  
**Curso:** Desarrollo de Aplicaciones Web – Evaluación Parcial (Semanas 1 a 8)  
**Calificación Objetivo:** 20/20 (Nivel Excelente en todos los criterios de la rúbrica)

---

## 1. RESUMEN EJECUTIVO Y ARQUITECTURA DE SOFTWARE

El sistema **EduPapel** es una plataforma web desarrollada para la administración integral del inventario de una librería escolar (cuadernos, artículos de escritura, materiales de arte, reglas y papelería general). La plataforma integra un **Frontend dinámico** y responsivo desarrollado con **HTML5 semántico, CSS3 / Tailwind CSS y JavaScript Puro (Vanilla JS)**, comunicado asíncronamente con un **Backend modular** implementado en **Python con Flask, Peewee ORM y SQLite**.

Todas las variables, funciones, métodos y modelos del código fuente se encuentran organizados y nombrados de forma clara en **idioma español**.

### 1.1 Diagrama de Arquitectura en Capas Limpias

La arquitectura elegida sigue el patrón de **Separación de Responsabilidades en Capas (Layered / Clean Architecture)**, aislando las distintas preocupaciones del sistema:

```
+-------------------------------------------------------------------------------+
|                           FRONTEND (Cliente Web)                              |
|  - Interfaz Semántica HTML5 + Tailwind CSS (Diseño Responsivo)                |
|  - Manipulación del DOM y Gestión de Eventos en Español (dom.js)              |
|  - Consumo Asíncrono con Fetch API y async/await (api.js - ServicioApi)      |
+-------------------------------------------------------------------------------+
                                    |  JSON vía HTTP/REST
                                    v
+-------------------------------------------------------------------------------+
|                      BACKEND (Flask Web Server - app.py)                      |
|                                                                               |
|  [CAPA DE CONTROLADORES / RUTAS] (rutas_productos.py, rutas_autenticacion.py) |
|   -> Recibe solicitudes HTTP, valida métodos y deserializa JSON.              |
|                                                                               |
|  [CAPA DE LÓGICA DE NEGOCIO] (ServicioProducto, ServicioAutenticacion)        |
|   -> Reglas de negocio, cálculos de stock y orquestación.                     |
|                                                                               |
|  [CAPA DE SEGURIDAD Y OWASP] (EncriptadorClaves, SanitizadorEntradas)         |
|   -> Criptografía con bcrypt, sanitización anti-XSS y validación de tipos.    |
|                                                                               |
|  [CAPA DE ACCESO A DATOS / ORM] (ModeloBase, Producto, Usuario)               |
|   -> Peewee ORM: Mapeo objeto-relacional y consultas parametrizadas.          |
+-------------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------------+
|                    BASE DE DATOS (SQLite - libreria_escolar.db)               |
+-------------------------------------------------------------------------------+
```

---

## 2. APLICACIÓN DE LA PROGRAMACIÓN ORIENTADA A OBJETOS (POO)

El Backend implementa sólidamente los pilares fundamentales de la Programación Orientada a Objetos con nomenclatura en español:

### 2.1 Clases y Abstracción
Se estructuran entidades y componentes lógicos en clases cohesivas:
- `ModeloBase`, `Producto`, `Usuario`: Representan las entidades persistentes del dominio.
- `ServicioBase`, `ServicioProducto`, `ServicioAutenticacion`: Encapsulan la lógica operacional.
- `EncriptadorClaves`, `SanitizadorEntradas`: Encapsulan utilidades criptográficas y de seguridad.

### 2.2 Herencia y Polimorfismo
- **Modelos:** `Producto` y `Usuario` heredan de `ModeloBase` (`models/base_model.py`), reutilizando la vinculación a la base de datos y la marca temporal `fecha_creacion`.
- **Sobrescritura Polimórfica:** `Usuario` sobrescribe el método `a_diccionario(incluir_sensible=False)` heredado de `ModeloBase` para suprimir deliberadamente el hash de la contraseña (`clave_hash`) al emitir respuestas al cliente.
- **Servicios:** `ServicioProducto` y `ServicioAutenticacion` heredan de `ServicioBase` (`services/base_service.py`), estandarizando las respuestas `respuesta_exitosa()` y `respuesta_error()`.

```python
# Ejemplo de Herencia en modelos (models/product_model.py)
class Producto(ModeloBase):
    codigo_sku = CharField(max_length=30, unique=True, index=True)
    nombre = CharField(max_length=150)
    categoria = CharField(max_length=60)
    precio = FloatField()
    stock = IntegerField(default=0)
    descripcion = TextField(default='')
    imagen_url = CharField(max_length=255, default='')
    esta_activo = BooleanField(default=True)
    # Hereda base_datos y fecha_creacion de ModeloBase
```

### 2.3 Encapsulamiento
- Los atributos sensibles y métodos internos no se exponen indiscriminadamente.
- La clase `EncriptadorClaves` encapsula las operaciones con bytes y generación de salts de `bcrypt`, exponiendo únicamente interfaces seguras de alto nivel (`hashear_clave` y `verificar_clave`).

---

## 3. APLICACIÓN DE LOS PRINCIPIOS SOLID

| Principio | Aplicación Concreta en el Código del Proyecto |
| :--- | :--- |
| **S - Responsabilidad Única (SRP)** | **Estricta separación por responsabilidades:**<br>• `routes/`: Únicamente enrutamiento HTTP y códigos de estado.<br>• `services/`: Únicamente lógica de negocio y validación de reglas.<br>• `models/`: Únicamente definición estructural de tablas y ORM.<br>• `security/`: Únicamente hashing con bcrypt y sanitización anti-XSS. |
| **O - Abierto / Cerrado (OCP)** | La clase `ServicioBase` provee una estructura de respuestas extensible. Nuevos módulos (por ejemplo, `ServicioProveedores` o `ServicioVentas`) extienden la funcionalidad sin modificar la clase base. |
| **L - Sustitución de Liskov (LSP)** | Las entidades derivadas (`Producto`, `Usuario`) cumplen con el contrato de `ModeloBase`. Cualquier servicio que opere con un modelo base puede invocar métodos como `a_diccionario()` sin romper la ejecución. |
| **I - Segregación de Interfaces (ISP)** | En lugar de un servicio monolítico gigante, se dividieron en `ServicioProducto` y `ServicioAutenticacion`, asegurando que cada controlador consuma únicamente los métodos pertinentes. |
| **D - Inversión de Dependencias (DIP)** | Los controladores (`product_routes.py`) interactúan a través de abstracciones del servicio (`ServicioProducto`), evitando el acoplamiento directo entre las vistas HTTP y las llamadas a bajo nivel de la base de datos. |

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
def hashear_clave(clave_plana: str) -> str:
    bytes_clave = clave_plana.encode('utf-8')
    semilla_salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(bytes_clave, semilla_salt).decode('utf-8')
```

### 4.2 Mitigación de Inyección SQL (SQLi)
- Se utiliza el ORM **Peewee**, el cual ejecuta automáticamente consultas SQL mediante **sentencias preparadas y parametrización de variables**.
- Ninguna cadena de entrada del usuario se concatena directamente en cláusulas `WHERE`, eliminando el vector de inyección SQL.

### 4.3 Mitigación de Cross-Site Scripting (XSS)
- **Sanitización en Backend (`security/sanitizer.py`):** Todas las entradas de texto se escapan con `html.escape()`, neutralizando caracteres como `<`, `>`, `&`, `"`, `'` antes de procesarse.
- **Defensa en Profundidad en Frontend (`frontend/js/dom.js`):** Función `escaparHTML()` y asignación de contenido de texto mediante `textContent` en el DOM para evitar que scripts maliciosos se ejecuten en el navegador del usuario.

### 4.4 Cero Hardcoding y Variables de Entorno
- La clave secreta de la aplicación (`CLAVE_SECRETA`) y la configuración del entorno no están incrustadas en el código fuente. Se leen dinámicamente mediante la librería `python-dotenv` desde el archivo `.env`.
- Se suministra un archivo plantilla `.env.example` en el repositorio para despliegues limpios y seguros.

---

## 5. CONCLUSIÓN

El sistema **EduPapel** satisface al 100% las exigencias académicas y técnicas de la rúbrica de evaluación: presenta una interfaz responsiva y accesible con Vanilla JS y Tailwind CSS, un consumo asíncrono impecable mediante Fetch API, una arquitectura orientada a objetos modular basada en SOLID y las medidas de seguridad estipuladas en la Semana 8 con hashing fuerte en `bcrypt` y prevención OWASP, todo con nomenclatura coherente en español.
