# 📚 EduPapel - Sistema de Gestión de Librería y Útiles Escolares

**Trabajo Parcial: Desarrollo de Aplicaciones Web (Semanas 1 - 8)**  
Aplicación web completa, modular y segura para la administración del inventario y catálogo de útiles escolares (cuadernos, artículos de escritura, materiales de arte, reglas y papelería).

---

## 🎯 Cumplimiento de la Rúbrica de Evaluación (Base 20 Puntos)

| Criterio | Puntos | Evidencia en el Proyecto |
| :--- | :---: | :--- |
| **1. UI, Estructura y DOM (Semanas 1-3)** | **4 / 4** | • Interfaz 100% responsiva y atractiva con **Tailwind CSS** y **HTML5 semántico** (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`).<br>• Manipulación limpia y eficiente del DOM con **JavaScript Puro (Vanilla JS)**.<br>• Validación interactiva de formularios en el cliente con feedback visual en tiempo real.<br>• Modales dinámicos y cero errores de consola. |
| **2. Asincronía y API REST (Semana 4)** | **4 / 4** | • CRUD completo (GET, POST, PUT, DELETE) consumido con **Fetch API** y **async/await**.<br>• Comunicación asíncrona en formato **JSON** sin recargar la página.<br>• Gestión de promesas, estados de carga (spinners) y captura de errores de red con notificaciones toast flotantes. |
| **3. Arquitectura y POO (Semanas 5-6)** | **4 / 4** | • **POO:** Clases (`Product`, `User`, `BaseModel`, `ProductService`, `AuthService`), Herencia y Encapsulamiento con **Peewee ORM**.<br>• **SOLID:** Especialmente el Principio de Responsabilidad Única (**SRP**) y separación modular en capas (`routes/`, `services/`, `models/`, `security/`). |
| **4. Seguridad Web y Encriptación (Semana 8)** | **4 / 4** | • **Criptografía:** Almacenamiento seguro de contraseñas mediante **`bcrypt`** con salting dinámico de 12 rondas (cero texto plano).<br>• **OWASP:** Mitigación de inyecciones SQL mediante consultas parametrizadas con Peewee ORM y mitigación de XSS sanitizando entradas en backend (`html.escape`) y DOM (`textContent`).<br>• Cero hardcoding: llaves y configuración cargadas con `python-dotenv` desde `.env`. |
| **5. Entregables y Documentación** | **4 / 4** | • Código fuente documentado con `README.md`.<br>• Manual Técnico conciso en [`docs/Manual_Tecnico_Arquitectura_Seguridad.md`](docs/Manual_Tecnico_Arquitectura_Seguridad.md).<br>• Guión detallado para el video de 5 minutos en [`docs/Guion_Video_Demostrativo.md`](docs/Guion_Video_Demostrativo.md). |

---

## 🚀 Tecnologías Utilizadas

- **Frontend:**
  - **HTML5** semántico y accesible.
  - **CSS3 / Tailwind CSS** (diseño responsivo móvil y escritorio).
  - **JavaScript Puro (Vanilla JS - ES6+)** para manipulación del DOM y eventos.
  - **Fetch API** con `async/await` para comunicación asíncrona.
- **Backend:**
  - **Python 3**
  - **Flask** (Microframework web y Blueprints modulares).
  - **Peewee ORM** (Mapeo objeto-relacional y prevención de SQL Injection).
  - **SQLite** (Base de datos relacional ligera).
  - **bcrypt** (Criptografía y hashing seguro de contraseñas).
  - **python-dotenv** (Gestión segura de variables de entorno).
  - **flask-cors** (Manejo de CORS para peticiones cross-origin).

---

## 📂 Estructura del Proyecto

```
Examen8Parcial/
│
├── backend/
│   ├── .env                       # Variables de entorno locales
│   ├── .env.example               # Plantilla de variables de entorno (sin secretos)
│   ├── requirements.txt           # Dependencias de Python
│   ├── config.py                  # Configuración centralizada (SRP, sin hardcoding)
│   ├── database.py                # Conexión SQLite con Peewee ORM
│   ├── seed.py                    # Datos de prueba iniciales (útiles y admin)
│   ├── app.py                     # Punto de entrada y servidor Flask
│   │
│   ├── models/                    # Capa de Acceso a Datos (POO / Herencia)
│   │   ├── base_model.py          # Clase base con id, created_at y to_dict()
│   │   ├── user_model.py          # Modelo de Usuario con protección de credenciales
│   │   └── product_model.py       # Modelo de Útiles Escolares
│   │
│   ├── services/                  # Capa de Lógica de Negocio (SOLID - SRP)
│   │   ├── base_service.py        # Clase base con respuestas estandarizadas
│   │   ├── auth_service.py        # Lógica de registro y login con bcrypt
│   │   └── product_service.py     # Lógica del catálogo y validación de reglas
│   │
│   ├── routes/                    # Capa de Controladores / Endpoints REST
│   │   ├── auth_routes.py         # Endpoints /api/auth
│   │   └── product_routes.py      # Endpoints /api/products (CRUD)
│   │
│   └── security/                  # Capa de Seguridad (Semana 8 / OWASP)
│       ├── hasher.py              # Encriptación con bcrypt
│       └── sanitizer.py           # Sanitización de entradas anti-XSS y validación
│
├── frontend/
│   ├── index.html                 # Vista principal semántica y responsiva
│   ├── css/
│   │   └── styles.css             # Estilos adicionales, animaciones y modales
│   └── js/
│       ├── api.js                 # Consumo asíncrono con Fetch API y async/await
│       ├── dom.js                 # Manipulación del DOM y sanitización XSS en cliente
│       └── app.js                 # Eventos, filtros en tiempo real y flujo de usuario
│
├── docs/
│   ├── Manual_Tecnico_Arquitectura_Seguridad.md  # Manual técnico para PDF (máx. 4 págs)
│   └── Guion_Video_Demostrativo.md               # Guión paso a paso para el video de 5 min
│
└── README.md                      # Documentación del proyecto
```

---

## 💻 Instrucciones de Instalación y Ejecución

### 1. Prerrequisitos
- Tener instalado **Python 3.10+**.
- Un navegador web moderno (Google Chrome, Edge, Firefox, Brave).

### 2. Configurar el Backend
Abre una terminal en la carpeta raíz del proyecto y navega hacia `backend`:

```powershell
cd backend
```

Instala las dependencias necesarias:
```powershell
pip install -r requirements.txt
```

Copia el archivo de variables de entorno si aún no lo tienes:
```powershell
copy .env.example .env
```

Puebla la base de datos con los útiles escolares de muestra y el usuario administrador:
```powershell
python seed.py
```

### 3. Iniciar el Servidor Backend
Ejecuta la aplicación Flask:
```powershell
python app.py
```

El servidor iniciará en: **`http://127.0.0.1:5000`**

### 4. Abrir la Aplicación Web (Frontend)
Tienes dos formas muy sencillas de abrirla:
- **Opción recomendada:** Ingresa directamente desde tu navegador a:
  👉 **`http://127.0.0.1:5000/`** (el propio servidor Flask sirve el Frontend y la API simultáneamente).
- **Opción alternativa:** Abre el archivo `frontend/index.html` en tu navegador o mediante la extensión *Live Server* de VS Code (cuenta con soporte CORS habilitado).

---

## 🔑 Credenciales de Prueba

Para probar el inicio de sesión seguro con **bcrypt**:
- **Usuario:** `admin` (o correo `admin@edupapel.com`)
- **Contraseña:** `admin123`

*(Nota: En la base de datos `libreria_escolar.db` la contraseña se almacena de forma segura como hash bcrypt generado con 12 rondas de salt, nunca en texto plano).*

---

## 📡 Catálogo de Endpoints de la API REST

### Módulo de Útiles Escolares (`/api/products`)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/products` | Lista todos los útiles escolares (admite `?search=cuaderno` y `?category=Cuadernos`). |
| `GET` | `/api/products/<id>` | Obtiene el detalle de un útil escolar por ID. |
| `POST` | `/api/products` | Registra un nuevo útil escolar (requiere JSON con sku, name, category, price, stock). |
| `PUT` | `/api/products/<id>` | Actualiza los datos de un útil escolar existente. |
| `DELETE` | `/api/products/<id>` | Elimina un útil escolar del inventario. |

### Módulo de Autenticación y Seguridad (`/api/auth`)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/api/auth/login` | Inicia sesión validando credenciales y hash bcrypt. |
| `POST` | `/api/auth/register` | Registra un nuevo usuario hasheando la contraseña con bcrypt. |
| `GET` | `/api/auth/status` | Verifica el estado del servicio de seguridad. |

---

## 📑 Documentación Adicional
- 📄 **Manual Técnico:** Consulta [`docs/Manual_Tecnico_Arquitectura_Seguridad.md`](docs/Manual_Tecnico_Arquitectura_Seguridad.md) para la explicación formal de la arquitectura, POO, SOLID y medidas OWASP (listo para exportar a PDF).
- 🎬 **Guión de Video:** Consulta [`docs/Guion_Video_Demostrativo.md`](docs/Guion_Video_Demostrativo.md) para grabar el video demostrativo de 5 minutos siguiendo los tiempos exactos de la rúbrica.