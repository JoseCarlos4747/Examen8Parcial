/**
 * Módulo de Comunicación Asíncrona (Semana 4)
 * Implementa consumo de API REST usando Fetch API y async/await.
 * Manejo completo de promesas, serialización JSON y gestión de errores de red.
 */

// Detección dinámica de la URL base del Backend
const BASE_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') && window.location.port === '5000'
    ? '/api'
    : 'http://127.0.0.1:5000/api';

export const ApiService = {
    /**
     * Verifica la disponibilidad del servidor backend.
     */
    async checkHealth() {
        try {
            const response = await fetch(`${BASE_URL}/auth/status`, {
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });
            return response.ok;
        } catch (error) {
            console.warn('[ApiService] Backend no accesible:', error.message);
            return false;
        }
    },

    /**
     * Obtiene el listado de útiles escolares con filtros opcionales.
     * @param {string} search Término de búsqueda
     * @param {string} category Categoría seleccionada
     */
    async getProducts(search = '', category = '') {
        try {
            const params = new URLSearchParams();
            if (search) params.append('search', search.trim());
            if (category && category !== 'Todas') params.append('category', category.trim());

            const url = `${BASE_URL}/products${params.toString() ? '?' + params.toString() : ''}`;
            const response = await fetch(url, {
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || `Error del servidor (${response.status})`);
            }

            return data.data || [];
        } catch (error) {
            console.error('[ApiService.getProducts] Error:', error);
            throw error;
        }
    },

    /**
     * Obtiene los datos de un único producto por ID.
     * @param {number|string} id 
     */
    async getProductById(id) {
        try {
            const response = await fetch(`${BASE_URL}/products/${id}`, {
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Error al obtener el producto.');
            }

            return data.data;
        } catch (error) {
            console.error('[ApiService.getProductById] Error:', error);
            throw error;
        }
    },

    /**
     * Registra un nuevo útil escolar en el backend.
     * @param {object} productData Datos del nuevo producto
     */
    async createProduct(productData) {
        try {
            const response = await fetch(`${BASE_URL}/products`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(productData)
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Error al registrar el producto.');
            }

            return data;
        } catch (error) {
            console.error('[ApiService.createProduct] Error:', error);
            throw error;
        }
    },

    /**
     * Actualiza un producto existente en el backend.
     * @param {number|string} id ID del producto
     * @param {object} productData Datos actualizados
     */
    async updateProduct(id, productData) {
        try {
            const response = await fetch(`${BASE_URL}/products/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(productData)
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Error al actualizar el producto.');
            }

            return data;
        } catch (error) {
            console.error('[ApiService.updateProduct] Error:', error);
            throw error;
        }
    },

    /**
     * Elimina un producto por ID.
     * @param {number|string} id ID del producto
     */
    async deleteProduct(id) {
        try {
            const response = await fetch(`${BASE_URL}/products/${id}`, {
                method: 'DELETE',
                headers: { 'Accept': 'application/json' }
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Error al eliminar el producto.');
            }

            return data;
        } catch (error) {
            console.error('[ApiService.deleteProduct] Error:', error);
            throw error;
        }
    },

    /**
     * Autenticación de usuario / administrador con verificación bcrypt.
     * @param {object} credentials { identifier, password }
     */
    async login(credentials) {
        try {
            const response = await fetch(`${BASE_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(credentials)
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Credenciales incorrectas.');
            }

            return data.data;
        } catch (error) {
            console.error('[ApiService.login] Error:', error);
            throw error;
        }
    }
};

