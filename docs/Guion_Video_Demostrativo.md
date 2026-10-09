# GUIÓN PARA EL VIDEO DEMOSTRATIVO (MÁXIMO 5 MINUTOS)
**Proyecto:** EduPapel – Sistema Web Seguro de Gestión de Útiles Escolares  
**Curso:** Desarrollo de Aplicaciones Web – Evaluación Parcial (Semanas 1 a 8)  
**Entregable 3 de la Rúbrica:** Video demostrativo de máx. 5 minutos subido a YouTube o Google Drive.

---

## ESTRUCTURA TEMPORAL DEL VIDEO

| Minuto | Sección | Objetivo en la Rúbrica |
| :--- | :--- | :--- |
| **0:00 - 0:45** | Introducción y Presentación del Caso Práctico | Presentar al estudiante, tema y alcance del proyecto. |
| **0:45 - 2:00** | Demostración Funcional en Vivo (Frontend + Asincronía) | Criterios 1 y 2: UI responsiva, DOM, Fetch API, CRUD en tiempo real. |
| **2:00 - 3:15** | Explicación del Frontend (HTML5, Vanilla JS, DOM en Español) | Criterios 1 y 2: Manipulación del DOM, validaciones y async/await. |
| **3:15 - 4:15** | Explicación del Backend (Arquitectura POO y SOLID) | Criterio 3: Clases, Herencia, Peewee ORM, capas y SRP. |
| **4:15 - 5:00** | Seguridad Web y Encriptación (Semana 8 / OWASP) | Criterio 4: Hashing con bcrypt, mitigación XSS y SQLi. Conclusión. |

---

## GUIÓN PASO A PASO CON DIÁLOGOS SUGERIDOS

### [0:00 - 0:45] Introducción
- **Acción en pantalla:** Mostrar la pantalla principal del sistema (`http://127.0.0.1:5000/`) y la carátula del proyecto.
- **Qué decir:**
  > *"Buenas tardes, profesor y compañeros. Mi nombre es [Tu Nombre] y a continuación presento mi proyecto para el Trabajo Parcial de Desarrollo de Aplicaciones Web.*  
  > *El caso práctico desarrollado es **EduPapel**, un sistema web seguro de gestión de inventario y catálogo para una librería de útiles escolares.*  
  > *La aplicación integra una interfaz visualmente atractiva y responsiva con HTML5 semántico, Tailwind CSS y JavaScript Puro (Vanilla JS), comunicada de forma asíncrona mediante Fetch API con un backend modular desarrollado en Python con Flask, el ORM Peewee, SQLite y seguridad con bcrypt.*  
  > *Todo el código fuente y las variables han sido estructurados de manera legible y en idioma español."*

---

### [0:45 - 2:00] Demostración Funcional en Vivo
- **Acción en pantalla:**
  1. Mostrar las tarjetas de métricas en la parte superior (Total Productos, Stock Total, Valor Inventario, Stock Crítico).
  2. Probar el filtro de categorías haciendo clic en las pestañas ("Cuadernos", "Escritura", "Arte y Dibujo", "Geometría").
  3. Probar la barra de búsqueda en tiempo real escribiendo "Faber" o "Cuaderno".
  4. Cambiar entre vista de Tarjetas y vista de Tabla con los botones de visualización.
  5. Clic en **"Nuevo Útil"**: intentar guardar con campos vacíos para mostrar las validaciones en rojo del cliente. Luego registrar un nuevo producto (ej. "Plumones Escolares x12", precio: 15.50, stock: 30) y observar cómo aparece en la interfaz sin recargar la página completa.
  6. Editar el producto recién creado (cambiar el precio o stock) y luego eliminarlo usando el modal de confirmación.
- **Qué decir:**
  > *"Como podemos observar en la interfaz, el sistema permite filtrar útiles escolares por categoría de forma dinámica y buscar en tiempo real sin recargar la página.*  
  > *Las métricas superiores se recalculan automáticamente con cada operación.*  
  > *Al abrir el modal para registrar un nuevo producto, el formulario valida en el cliente que el código SKU no esté vacío, el precio sea mayor a cero y el stock sea un número válido.*  
  > *Cuando guardamos o eliminamos un producto, el frontend emite peticiones asíncronas GET, POST, PUT y DELETE usando la Fetch API, reflejando el cambio al instante y mostrando notificaciones toast informativas."*

---

### [2:00 - 3:15] Explicación del Frontend (Vanilla JS y DOM)
- **Acción en pantalla:** Abrir el editor de código y mostrar la carpeta `frontend/js/`.
- **Archivos a mostrar:**
  - `frontend/js/dom.js`: Mostrar las funciones `renderizarTarjetas`, `escaparHTML` y los eventos `addEventListener`.
  - `frontend/js/api.js`: Mostrar el objeto `ServicioApi` y los métodos `obtenerProductos`, `crearProducto`, `actualizarProducto`, `eliminarProducto` con `fetch()` y `async/await`.
  - `frontend/js/app.js`: Mostrar el objeto `estadoAplicacion` y los manejadores de eventos.
- **Qué decir:**
  > *"Para cumplir con los requerimientos de las Semanas 1 a 4, el Frontend se construyó utilizando JavaScript Puro (Vanilla JS) con todas las variables y funciones nombradas en español.*  
  > *En `dom.js` manipulamos directamente el DOM mediante `document.createElement` y `addEventListener`, aplicando la función `escaparHTML` para prevenir inyecciones de código malicioso XSS.*  
  > *En `api.js` centralizamos el consumo del API REST mediante la Fetch API con `async/await`, gestionando correctamente los estados de carga, la serialización de JSON y la captura de errores de red con bloques `try...catch`."*

---

### [3:15 - 4:15] Explicación del Backend (POO y Principios SOLID)
- **Acción en pantalla:** Mostrar la estructura de carpetas en `backend/`:
  - `models/base_model.py` (`ModeloBase`) y `models/product_model.py` (`Producto`).
  - `services/base_service.py` (`ServicioBase`) y `services/product_service.py` (`ServicioProducto`).
  - `routes/product_routes.py` (`rutas_productos`).
- **Qué decir:**
  > *"En el Backend aplicamos los fundamentos de la Programación Orientada a Objetos y una arquitectura limpia modular.*  
  > *En la capa de modelos, `Producto` y `Usuario` heredan de `ModeloBase`, demostrando herencia y encapsulamiento al utilizar Peewee ORM.*  
  > *Respecto a los Principios SOLID, aplicamos rigurosamente el Principio de Responsabilidad Única (SRP): las rutas en `routes/` únicamente manejan las peticiones HTTP y códigos de estado; los servicios en `services/` encapsulan las reglas de negocio; y los modelos gestionan la persistencia en la base de datos SQLite."*

---

### [4:15 - 5:00] Seguridad Web y Encriptación (Semana 8)
- **Acción en pantalla:**
  - Mostrar `backend/security/hasher.py` (código de `EncriptadorClaves` con `bcrypt.hashpw` y `bcrypt.gensalt`).
  - Mostrar `backend/config.py` (`Configuracion`) y el archivo `.env` para evidenciar que no hay llaves hardcodeadas.
  - Volver a la web, hacer clic en "Admin (Login)" e iniciar sesión con `admin` / `admin123`.
- **Qué decir:**
  > *"Finalmente, para cumplir con el criterio de Seguridad Web de la Semana 8 y las guías de OWASP Top 10:*  
  > *1. Las contraseñas nunca se guardan en texto plano: usamos la librería `bcrypt` con 12 rondas de salt criptográfico en `EncriptadorClaves.hashear_clave`.*  
  > *2. Mitigamos SQL Injection utilizando consultas parametrizadas a través del ORM Peewee.*  
  > *3. Mitigamos XSS sanitizando todas las entradas en el backend con `SanitizadorEntradas` y en el cliente con `escaparHTML`.*  
  > *4. Y evitamos el hardcoding leyendo las llaves secretas y la configuración desde variables de entorno con `python-dotenv`.*  
  > *Con esto, el proyecto cumple al 100% con todos los requerimientos de la rúbrica. Muchas gracias por su atención."*

---

### CONSEJOS PARA LA GRABACIÓN
1. **Resolución:** Graba a 1080p (Full HD) usando OBS Studio, Clipchamp o la barra de juegos de Windows (`Win + G`).
2. **Audio:** Habla con tono claro y pausado; prueba el micrófono antes de empezar.
3. **Tiempo:** Cronometra el video para que esté entre 3:30 y 4:45 minutos (la rúbrica fija un máximo estricto de 5 minutos).
4. **Enlace:** Súbelo a YouTube como "No listado" (Unlisted) o a Google Drive con acceso "Cualquiera con el enlace puede ver".
