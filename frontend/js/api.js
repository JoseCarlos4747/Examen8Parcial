/**
 * Módulo de Comunicación Asíncrona (Semana 4)
 * Implementa consumo de API REST usando Fetch API y async/await.
 * Manejo completo de promesas, serialización JSON y gestión de errores de red.
 * Nombres de variables, funciones y métodos en español.
 */

// Detección dinámica de la URL base del Backend
const URL_BASE = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') && window.location.port === '5000'
    ? '/api'
    : 'http://127.0.0.1:5000/api';

export const ServicioApi = {
    /**
     * Verifica la disponibilidad del servidor backend.
     */
    async verificarConexion() {
        try {
            const respuesta = await fetch(`${URL_BASE}/auth/status`, {
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });
            return respuesta.ok;
        } catch (errorCapturado) {
            console.warn('[ServicioApi] Backend no accesible:', errorCapturado.message);
            return false;
        }
    },

    /**
     * Obtiene el listado de útiles escolares con filtros opcionales.
     * @param {string} busqueda Término de búsqueda
     * @param {string} categoria Categoría seleccionada
     */
    async obtenerProductos(busqueda = '', categoria = '') {
        try {
            const parametros = new URLSearchParams();
            if (busqueda) parametros.append('busqueda', busqueda.trim());
            if (categoria && categoria !== 'Todas') parametros.append('categoria', categoria.trim());

            const urlConsulta = `${URL_BASE}/products${parametros.toString() ? '?' + parametros.toString() : ''}`;
            const respuesta = await fetch(urlConsulta, {
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });

            const datosRespuesta = await respuesta.json();
            if (!respuesta.ok) {
                const mensajeError = datosRespuesta.mensaje || datosRespuesta.message || `Error del servidor (${respuesta.status})`;
                throw new Error(mensajeError);
            }

            return datosRespuesta.datos || datosRespuesta.data || [];
        } catch (errorCapturado) {
            console.error('[ServicioApi.obtenerProductos] Error:', errorCapturado);
            throw errorCapturado;
        }
    },

    /**
     * Obtiene los datos de un único producto por su ID.
     * @param {number|string} idProducto 
     */
    async obtenerProductoPorId(idProducto) {
        try {
            const respuesta = await fetch(`${URL_BASE}/products/${idProducto}`, {
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });

            const datosRespuesta = await respuesta.json();
            if (!respuesta.ok) {
                throw new Error(datosRespuesta.mensaje || datosRespuesta.message || 'Error al obtener el producto.');
            }

            return datosRespuesta.datos || datosRespuesta.data;
        } catch (errorCapturado) {
            console.error('[ServicioApi.obtenerProductoPorId] Error:', errorCapturado);
            throw errorCapturado;
        }
    },

    /**
     * Registra un nuevo útil escolar en el backend.
     * @param {object} datosProducto Datos del nuevo producto
     */
    async crearProducto(datosProducto) {
        try {
            const respuesta = await fetch(`${URL_BASE}/products`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(datosProducto)
            });

            const datosRespuesta = await respuesta.json();
            if (!respuesta.ok) {
                throw new Error(datosRespuesta.mensaje || datosRespuesta.message || 'Error al registrar el producto.');
            }

            return datosRespuesta.datos || datosRespuesta.data;
        } catch (errorCapturado) {
            console.error('[ServicioApi.crearProducto] Error:', errorCapturado);
            throw errorCapturado;
        }
    },

    /**
     * Actualiza un producto existente en el backend.
     * @param {number|string} idProducto ID del producto
     * @param {object} datosProducto Datos actualizados
     */
    async actualizarProducto(idProducto, datosProducto) {
        try {
            const respuesta = await fetch(`${URL_BASE}/products/${idProducto}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(datosProducto)
            });

            const datosRespuesta = await respuesta.json();
            if (!respuesta.ok) {
                throw new Error(datosRespuesta.mensaje || datosRespuesta.message || 'Error al actualizar el producto.');
            }

            return datosRespuesta.datos || datosRespuesta.data;
        } catch (errorCapturado) {
            console.error('[ServicioApi.actualizarProducto] Error:', errorCapturado);
            throw errorCapturado;
        }
    },

    /**
     * Elimina un producto por su ID.
     * @param {number|string} idProducto ID del producto
     */
    async eliminarProducto(idProducto) {
        try {
            const respuesta = await fetch(`${URL_BASE}/products/${idProducto}`, {
                method: 'DELETE',
                headers: { 'Accept': 'application/json' }
            });

            const datosRespuesta = await respuesta.json();
            if (!respuesta.ok) {
                throw new Error(datosRespuesta.mensaje || datosRespuesta.message || 'Error al eliminar el producto.');
            }

            return datosRespuesta.datos || datosRespuesta.data;
        } catch (errorCapturado) {
            console.error('[ServicioApi.eliminarProducto] Error:', errorCapturado);
            throw errorCapturado;
        }
    },

    /**
     * Autenticación de usuario / administrador con verificación bcrypt.
     * @param {object} credenciales { identificador, clave }
     */
    async iniciarSesion(credenciales) {
        try {
            const respuesta = await fetch(`${URL_BASE}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(credenciales)
            });

            const datosRespuesta = await respuesta.json();
            if (!respuesta.ok) {
                throw new Error(datosRespuesta.mensaje || datosRespuesta.message || 'Credenciales incorrectas.');
            }

            return datosRespuesta.datos || datosRespuesta.data;
        } catch (errorCapturado) {
            console.error('[ServicioApi.iniciarSesion] Error:', errorCapturado);
            throw errorCapturado;
        }
    }
};

// Alias para compatibilidad
export const ApiService = ServicioApi;
