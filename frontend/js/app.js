/**
 * Archivo Principal de la Aplicación Frontend EduPapel
 * Implementa el flujo de control, gestión de eventos del usuario,
 * asincronía con Fetch API y manipulación pura del DOM con Vanilla JS.
 * Nombres de variables, estados y funciones en español.
 */
import { ServicioApi } from './api.js';
import {
    renderizarTarjetas,
    renderizarTabla,
    renderizarEstadisticas,
    mostrarToast,
    abrirModal,
    cerrarModal,
    mostrarErrorCampo,
    limpiarErroresCampos
} from './dom.js';

// ================= ESTADO DE LA APLICACIÓN =================
const estadoAplicacion = {
    listaProductos: [],
    categoriaSeleccionada: 'Todas',
    textoBusqueda: '',
    ordenActual: 'nombre_asc',
    vistaActual: 'tarjetas', // 'tarjetas' | 'tabla'
    usuarioActual: JSON.parse(localStorage.getItem('usuario_edupapel') || 'null'),
    productoAEliminar: null // { id, nombre }
};

// ================= SELECTORES DEL DOM =================
const elementosInterfaz = {
    // Cabecera y Estado API
    insigniaEstadoApi: document.getElementById('apiStatusBadge'),
    botonAutenticacion: document.getElementById('btnOpenAuth'),
    textoEstadoAutenticacion: document.getElementById('authStatusText'),
    botonNuevoProducto: document.getElementById('btnOpenNewProduct'),

    // Filtros y Búsqueda
    contenedorPillsCategorias: document.getElementById('categoryPillsContainer'),
    campoBusqueda: document.getElementById('searchInput'),
    botonLimpiarBusqueda: document.getElementById('btnClearSearch'),
    selectorOrden: document.getElementById('sortSelect'),
    botonVistaTarjetas: document.getElementById('btnViewGrid'),
    botonVistaTabla: document.getElementById('btnViewTable'),

    // Contenedores del Catálogo
    indicadorCarga: document.getElementById('loadingState'),
    cuadriculaProductos: document.getElementById('productsGrid'),
    contenedorTablaProductos: document.getElementById('productsTableContainer'),
    cuerpoTablaProductos: document.getElementById('productsTableBody'),

    // Modal de Producto
    modalProducto: document.getElementById('productModal'),
    tituloModalProducto: document.getElementById('productModalTitle'),
    formularioProducto: document.getElementById('productForm'),
    campoIdProducto: document.getElementById('formProductId'),
    campoCodigoSku: document.getElementById('formSku'),
    campoCategoria: document.getElementById('formCategory'),
    campoNombre: document.getElementById('formName'),
    campoPrecio: document.getElementById('formPrice'),
    campoStock: document.getElementById('formStock'),
    campoImagenUrl: document.getElementById('formImageUrl'),
    campoDescripcion: document.getElementById('formDescription'),
    botonCancelarProducto: document.getElementById('btnCancelProductModal'),
    botonCerrarModalProducto: document.getElementById('btnCloseProductModal'),
    botonGuardarProducto: document.getElementById('btnSaveProduct'),

    // Modal de Eliminación
    modalEliminar: document.getElementById('deleteModal'),
    nombreProductoAEliminar: document.getElementById('deleteProductName'),
    botonCancelarEliminar: document.getElementById('btnCancelDelete'),
    botonConfirmarEliminar: document.getElementById('btnConfirmDelete'),

    // Modal de Autenticación
    modalAutenticacion: document.getElementById('authModal'),
    formularioAutenticacion: document.getElementById('authForm'),
    campoIdentificador: document.getElementById('authIdentifier'),
    campoClave: document.getElementById('authPassword'),
    botonCerrarModalAuth: document.getElementById('btnCloseAuthModal'),
    botonEnviarAuth: document.getElementById('btnSubmitAuth')
};

// ================= INICIALIZACIÓN =================
document.addEventListener('DOMContentLoaded', () => {
    iniciarAplicacion();
});

async function iniciarAplicacion() {
    actualizarInterfazUsuario();
    registrarManejadoresEventos();
    await verificarEstadoServidor();
    await cargarProductos();
}

/**
 * Verifica si el backend está activo y en línea.
 */
async function verificarEstadoServidor() {
    const servidorActivo = await ServicioApi.verificarConexion();
    if (elementosInterfaz.insigniaEstadoApi) {
        if (servidorActivo) {
            elementosInterfaz.insigniaEstadoApi.className = 'hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200';
            elementosInterfaz.insigniaEstadoApi.innerHTML = '<span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span><span>API Online</span>';
        } else {
            elementosInterfaz.insigniaEstadoApi.className = 'hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200';
            elementosInterfaz.insigniaEstadoApi.innerHTML = '<span class="w-2 h-2 rounded-full bg-rose-500"></span><span>API Desconectada</span>';
        }
    }
}

/**
 * Carga los productos desde el servidor de forma asíncrona (Fetch API con async/await).
 */
async function cargarProductos() {
    try {
        establecerEstadoCarga(true);
        const datosRecibidos = await ServicioApi.obtenerProductos(
            estadoAplicacion.textoBusqueda,
            estadoAplicacion.categoriaSeleccionada
        );
        estadoAplicacion.listaProductos = datosRecibidos;
        renderizarCatalogo();
        renderizarEstadisticas(estadoAplicacion.listaProductos);
    } catch (errorCapturado) {
        mostrarToast(`Error al cargar catálogo: ${errorCapturado.message}`, 'error');
    } finally {
        establecerEstadoCarga(false);
    }
}

/**
 * Muestra u oculta el spinner de carga en el DOM.
 * @param {boolean} estaCargando 
 */
function establecerEstadoCarga(estaCargando) {
    if (estaCargando) {
        elementosInterfaz.indicadorCarga.classList.remove('hidden');
        elementosInterfaz.cuadriculaProductos.classList.add('hidden');
        elementosInterfaz.contenedorTablaProductos.classList.add('hidden');
    } else {
        elementosInterfaz.indicadorCarga.classList.add('hidden');
        if (estadoAplicacion.vistaActual === 'tarjetas') {
            elementosInterfaz.cuadriculaProductos.classList.remove('hidden');
            elementosInterfaz.contenedorTablaProductos.classList.add('hidden');
        } else {
            elementosInterfaz.cuadriculaProductos.classList.add('hidden');
            elementosInterfaz.contenedorTablaProductos.classList.remove('hidden');
        }
    }
}

/**
 * Aplica ordenamiento a la lista de productos y la renderiza en el DOM.
 */
function renderizarCatalogo() {
    let productosOrdenados = [...estadoAplicacion.listaProductos];

    switch (estadoAplicacion.ordenActual) {
        case 'name_asc':
            productosOrdenados.sort((a, b) => (a.nombre || a.name || '').localeCompare(b.nombre || b.name || ''));
            break;
        case 'name_desc':
            productosOrdenados.sort((a, b) => (b.nombre || b.name || '').localeCompare(a.nombre || a.name || ''));
            break;
        case 'price_asc':
            productosOrdenados.sort((a, b) => (a.precio ?? a.price) - (b.precio ?? b.price));
            break;
        case 'price_desc':
            productosOrdenados.sort((a, b) => (b.precio ?? b.price) - (a.precio ?? a.price));
            break;
        case 'stock_asc':
            productosOrdenados.sort((a, b) => a.stock - b.stock);
            break;
        case 'stock_desc':
            productosOrdenados.sort((a, b) => b.stock - a.stock);
            break;
    }

    if (estadoAplicacion.vistaActual === 'tarjetas') {
        renderizarTarjetas(productosOrdenados, elementosInterfaz.cuadriculaProductos);
    } else {
        renderizarTabla(productosOrdenados, elementosInterfaz.cuerpoTablaProductos);
    }
}

// ================= GESTIÓN DE EVENTOS DEL DOM (SEMANAS 1 A 3) =================
function registrarManejadoresEventos() {
    // 1. Filtro por categoría (Pills interactivos)
    elementosInterfaz.contenedorPillsCategorias.addEventListener('click', (evento) => {
        const botonObjetivo = evento.target.closest('button[data-category]');
        if (!botonObjetivo) return;

        elementosInterfaz.contenedorPillsCategorias.querySelectorAll('.category-pill').forEach(boton => {
            boton.classList.remove('active', 'bg-brand-600', 'text-white', 'shadow-sm');
            boton.classList.add('text-slate-600', 'hover:text-slate-900', 'hover:bg-slate-100');
        });

        botonObjetivo.classList.add('active', 'bg-brand-600', 'text-white', 'shadow-sm');
        botonObjetivo.classList.remove('text-slate-600', 'hover:text-slate-900', 'hover:bg-slate-100');

        estadoAplicacion.categoriaSeleccionada = botonObjetivo.dataset.category;
        cargarProductos();
    });

    // 2. Búsqueda en tiempo real (Input con debounce)
    let temporizadorDebounce = null;
    elementosInterfaz.campoBusqueda.addEventListener('input', (evento) => {
        const textoIngresado = evento.target.value.trim();
        elementosInterfaz.botonLimpiarBusqueda.classList.toggle('hidden', textoIngresado === '');

        clearTimeout(temporizadorDebounce);
        temporizadorDebounce = setTimeout(() => {
            estadoAplicacion.textoBusqueda = textoIngresado;
            cargarProductos();
        }, 300);
    });

    elementosInterfaz.botonLimpiarBusqueda.addEventListener('click', () => {
        elementosInterfaz.campoBusqueda.value = '';
        elementosInterfaz.botonLimpiarBusqueda.classList.add('hidden');
        estadoAplicacion.textoBusqueda = '';
        cargarProductos();
    });

    // 3. Ordenación
    elementosInterfaz.selectorOrden.addEventListener('change', (evento) => {
        estadoAplicacion.ordenActual = evento.target.value;
        renderizarCatalogo();
    });

    // 4. Cambiar entre Vista Tarjetas y Vista Tabla
    elementosInterfaz.botonVistaTarjetas.addEventListener('click', () => {
        estadoAplicacion.vistaActual = 'tarjetas';
        elementosInterfaz.botonVistaTarjetas.classList.add('text-brand-600', 'bg-brand-50');
        elementosInterfaz.botonVistaTarjetas.classList.remove('text-slate-400');
        elementosInterfaz.botonVistaTabla.classList.remove('text-brand-600', 'bg-brand-50');
        elementosInterfaz.botonVistaTabla.classList.add('text-slate-400');
        establecerEstadoCarga(false);
        renderizarCatalogo();
    });

    elementosInterfaz.botonVistaTabla.addEventListener('click', () => {
        estadoAplicacion.vistaActual = 'tabla';
        elementosInterfaz.botonVistaTabla.classList.add('text-brand-600', 'bg-brand-50');
        elementosInterfaz.botonVistaTabla.classList.remove('text-slate-400');
        elementosInterfaz.botonVistaTarjetas.classList.remove('text-brand-600', 'bg-brand-50');
        elementosInterfaz.botonVistaTarjetas.classList.add('text-slate-400');
        establecerEstadoCarga(false);
        renderizarCatalogo();
    });

    // 5. Modal de Creación de Producto
    elementosInterfaz.botonNuevoProducto.addEventListener('click', () => {
        restablecerFormularioProducto();
        elementosInterfaz.tituloModalProducto.textContent = 'Nuevo Útil Escolar';
        abrirModal('productModal');
    });

    elementosInterfaz.botonCancelarProducto.addEventListener('click', () => cerrarModal('productModal'));
    elementosInterfaz.botonCerrarModalProducto.addEventListener('click', () => cerrarModal('productModal'));

    // 6. Envío del Formulario de Producto (Submit con validación del cliente)
    elementosInterfaz.formularioProducto.addEventListener('submit', procesarFormularioProducto);

    // 7. Delegación de Eventos en Tarjetas y Tabla (Editar y Eliminar)
    const despachadorAcciones = (evento) => {
        const botonEditar = evento.target.closest('button[data-action="edit"]');
        const botonEliminar = evento.target.closest('button[data-action="delete"]');

        if (botonEditar) {
            const idProducto = botonEditar.dataset.id;
            prepararEdicionProducto(idProducto);
        } else if (botonEliminar) {
            const idProducto = botonEliminar.dataset.id;
            const nombreProducto = botonEliminar.dataset.name || 'este producto';
            prepararEliminacionProducto(idProducto, nombreProducto);
        }
    };

    elementosInterfaz.cuadriculaProductos.addEventListener('click', despachadorAcciones);
    elementosInterfaz.contenedorTablaProductos.addEventListener('click', despachadorAcciones);

    // 8. Confirmación de Eliminación
    elementosInterfaz.botonCancelarEliminar.addEventListener('click', () => cerrarModal('deleteModal'));
    elementosInterfaz.botonConfirmarEliminar.addEventListener('click', confirmarEliminarProducto);

    // 9. Autenticación / Login
    elementosInterfaz.botonAutenticacion.addEventListener('click', () => {
        if (estadoAplicacion.usuarioActual) {
            const nombreMostrado = estadoAplicacion.usuarioActual.nombre_usuario || estadoAplicacion.usuarioActual.username;
            if (confirm(`¿Deseas cerrar la sesión de @${nombreMostrado}?`)) {
                localStorage.removeItem('usuario_edupapel');
                estadoAplicacion.usuarioActual = null;
                actualizarInterfazUsuario();
                mostrarToast('Sesión finalizada con éxito.', 'info');
            }
        } else {
            limpiarErroresCampos(elementosInterfaz.formularioAutenticacion);
            elementosInterfaz.formularioAutenticacion.reset();
            abrirModal('authModal');
        }
    });

    elementosInterfaz.botonCerrarModalAuth.addEventListener('click', () => cerrarModal('authModal'));
    elementosInterfaz.formularioAutenticacion.addEventListener('submit', procesarFormularioAutenticacion);
}

// ================= ACCIONES DE PRODUCTO =================

/**
 * Carga los datos de un producto en el formulario para edición.
 * @param {number|string} idProducto 
 */
async function prepararEdicionProducto(idProducto) {
    try {
        const productoEncontrado = estadoAplicacion.listaProductos.find(p => p.id == idProducto) 
            || await ServicioApi.obtenerProductoPorId(idProducto);

        if (!productoEncontrado) throw new Error('Producto no encontrado.');

        restablecerFormularioProducto();
        elementosInterfaz.campoIdProducto.value = productoEncontrado.id;
        elementosInterfaz.campoCodigoSku.value = productoEncontrado.codigo_sku || productoEncontrado.sku || '';
        elementosInterfaz.campoCategoria.value = productoEncontrado.categoria || productoEncontrado.category || '';
        elementosInterfaz.campoNombre.value = productoEncontrado.nombre || productoEncontrado.name || '';
        elementosInterfaz.campoPrecio.value = productoEncontrado.precio !== undefined ? productoEncontrado.precio : productoEncontrado.price;
        elementosInterfaz.campoStock.value = productoEncontrado.stock;
        elementosInterfaz.campoImagenUrl.value = productoEncontrado.imagen_url || productoEncontrado.image_url || '';
        elementosInterfaz.campoDescripcion.value = productoEncontrado.descripcion || productoEncontrado.description || '';

        elementosInterfaz.tituloModalProducto.textContent = 'Editar Útil Escolar';
        abrirModal('productModal');
    } catch (errorCapturado) {
        mostrarToast(errorCapturado.message, 'error');
    }
}

/**
 * Prepara el modal de confirmación antes de borrar un producto.
 */
function prepararEliminacionProducto(idProducto, nombreProducto) {
    estadoAplicacion.productoAEliminar = { id: idProducto, nombre: nombreProducto };
    elementosInterfaz.nombreProductoAEliminar.textContent = `"${nombreProducto}"`;
    abrirModal('deleteModal');
}

/**
 * Ejecuta la llamada asíncrona DELETE al servidor.
 */
async function confirmarEliminarProducto() {
    if (!estadoAplicacion.productoAEliminar) return;

    try {
        elementosInterfaz.botonConfirmarEliminar.disabled = true;
        elementosInterfaz.botonConfirmarEliminar.textContent = 'Eliminando...';

        await ServicioApi.eliminarProducto(estadoAplicacion.productoAEliminar.id);
        mostrarToast(`"${estadoAplicacion.productoAEliminar.nombre}" eliminado exitosamente.`, 'success');
        cerrarModal('deleteModal');
        await cargarProductos();
    } catch (errorCapturado) {
        mostrarToast(`Error al eliminar: ${errorCapturado.message}`, 'error');
    } finally {
        elementosInterfaz.botonConfirmarEliminar.disabled = false;
        elementosInterfaz.botonConfirmarEliminar.textContent = 'Eliminar';
        estadoAplicacion.productoAEliminar = null;
    }
}

/**
 * Valida y envía el formulario de producto (POST / PUT).
 */
async function procesarFormularioProducto(evento) {
    evento.preventDefault();
    limpiarErroresCampos(elementosInterfaz.formularioProducto);

    let existenErrores = false;

    const codigoSku = elementosInterfaz.campoCodigoSku.value.trim().toUpperCase();
    if (!codigoSku) {
        mostrarErrorCampo(elementosInterfaz.campoCodigoSku, 'El código SKU es obligatorio.');
        existenErrores = true;
    }

    const categoria = elementosInterfaz.campoCategoria.value.trim();
    if (!categoria) {
        mostrarErrorCampo(elementosInterfaz.campoCategoria, 'Seleccione una categoría válida.');
        existenErrores = true;
    }

    const nombre = elementosInterfaz.campoNombre.value.trim();
    if (!nombre || nombre.length < 3) {
        mostrarErrorCampo(elementosInterfaz.campoNombre, 'El nombre debe tener al menos 3 caracteres.');
        existenErrores = true;
    }

    const precio = parseFloat(elementosInterfaz.campoPrecio.value);
    if (isNaN(precio) || precio <= 0) {
        mostrarErrorCampo(elementosInterfaz.campoPrecio, 'Ingrese un precio válido mayor a 0.');
        existenErrores = true;
    }

    const stock = parseInt(elementosInterfaz.campoStock.value, 10);
    if (isNaN(stock) || stock < 0) {
        mostrarErrorCampo(elementosInterfaz.campoStock, 'El stock debe ser un entero mayor o igual a 0.');
        existenErrores = true;
    }

    if (existenErrores) return;

    const datosProducto = {
        codigo_sku: codigoSku,
        sku: codigoSku,
        categoria: categoria,
        nombre: nombre,
        precio: precio,
        stock: stock,
        imagen_url: elementosInterfaz.campoImagenUrl.value.trim(),
        descripcion: elementosInterfaz.campoDescripcion.value.trim()
    };

    const esEdicion = Boolean(elementosInterfaz.campoIdProducto.value);
    const botonGuardar = elementosInterfaz.botonGuardarProducto;

    try {
        botonGuardar.disabled = true;
        botonGuardar.innerHTML = '<span>Guardando...</span>';

        if (esEdicion) {
            await ServicioApi.actualizarProducto(elementosInterfaz.campoIdProducto.value, datosProducto);
            mostrarToast('Útil escolar actualizado exitosamente.', 'success');
        } else {
            await ServicioApi.crearProducto(datosProducto);
            mostrarToast('Nuevo útil escolar registrado exitosamente.', 'success');
        }

        cerrarModal('productModal');
        await cargarProductos();
    } catch (errorCapturado) {
        mostrarToast(errorCapturado.message, 'error');
    } finally {
        botonGuardar.disabled = false;
        botonGuardar.innerHTML = '<span>Guardar</span>';
    }
}

function restablecerFormularioProducto() {
    limpiarErroresCampos(elementosInterfaz.formularioProducto);
    elementosInterfaz.formularioProducto.reset();
    elementosInterfaz.campoIdProducto.value = '';
}

// ================= ACCIONES DE AUTENTICACIÓN =================

async function procesarFormularioAutenticacion(evento) {
    evento.preventDefault();
    limpiarErroresCampos(elementosInterfaz.formularioAutenticacion);

    const identificador = elementosInterfaz.campoIdentificador.value.trim();
    const clave = elementosInterfaz.campoClave.value.trim();

    if (!identificador) {
        mostrarErrorCampo(elementosInterfaz.campoIdentificador, 'Ingrese su usuario o correo.');
        return;
    }
    if (!clave) {
        mostrarErrorCampo(elementosInterfaz.campoClave, 'Ingrese su contraseña.');
        return;
    }

    try {
        elementosInterfaz.botonEnviarAuth.disabled = true;
        elementosInterfaz.botonEnviarAuth.textContent = 'Verificando hash...';

        const resultado = await ServicioApi.iniciarSesion({ identificador, clave });
        const usuarioSesion = resultado.usuario || resultado.user;

        estadoAplicacion.usuarioActual = usuarioSesion;
        localStorage.setItem('usuario_edupapel', JSON.stringify(usuarioSesion));

        actualizarInterfazUsuario();
        cerrarModal('authModal');
        const nombreMostrado = usuarioSesion.nombre_usuario || usuarioSesion.username;
        mostrarToast(`¡Bienvenido, ${nombreMostrado}! Modo Administrador activo.`, 'success');
    } catch (errorCapturado) {
        mostrarToast(`Error de autenticación: ${errorCapturado.message}`, 'error');
    } finally {
        elementosInterfaz.botonEnviarAuth.disabled = false;
        elementosInterfaz.botonEnviarAuth.textContent = 'Iniciar Sesión';
    }
}

function actualizarInterfazUsuario() {
    if (estadoAplicacion.usuarioActual) {
        const nombreUsuario = estadoAplicacion.usuarioActual.nombre_usuario || estadoAplicacion.usuarioActual.username;
        elementosInterfaz.textoEstadoAutenticacion.textContent = `@${nombreUsuario} (Salir)`;
        elementosInterfaz.botonAutenticacion.classList.add('bg-emerald-50', 'text-emerald-700', 'border-emerald-300');
    } else {
        elementosInterfaz.textoEstadoAutenticacion.textContent = 'Admin (Login)';
        elementosInterfaz.botonAutenticacion.classList.remove('bg-emerald-50', 'text-emerald-700', 'border-emerald-300');
    }
}
