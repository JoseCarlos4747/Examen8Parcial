/**
 * Módulo de Manipulación del DOM e Interfaz de Usuario (Semanas 1 a 3)
 * Implementa JavaScript Puro (Vanilla JS) para el control del Document Object Model,
 * validación visual de formularios y renderizado dinámico seguro (Mitigación XSS).
 * Nombres de funciones y variables en español.
 */

/**
 * Escapa caracteres HTML para prevenir inyección XSS al manipular el DOM.
 * @param {string} cadenaTexto Texto a sanitizar
 */
export function escaparHTML(cadenaTexto) {
    if (cadenaTexto === null || cadenaTexto === undefined) return '';
    return String(cadenaTexto)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

/**
 * Muestra una notificación flotante (Toast) en la pantalla.
 * @param {string} mensaje Mensaje a mostrar
 * @param {'success'|'error'|'warning'|'info'} tipo Tipo de notificación
 */
export function mostrarToast(mensaje, tipo = 'info') {
    const contenedorNotificaciones = document.getElementById('contenedorNotificaciones') || document.getElementById('toastContainer');
    if (!contenedorNotificaciones) return;

    const mapaColores = {
        success: 'bg-emerald-600 text-white border-emerald-700',
        error: 'bg-rose-600 text-white border-rose-700',
        warning: 'bg-amber-600 text-white border-amber-700',
        info: 'bg-indigo-600 text-white border-indigo-700'
    };

    const mapaIconos = {
        success: '<svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>',
        error: '<svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>',
        warning: '<svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>',
        info: '<svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
    };

    const elementoToast = document.createElement('div');
    elementoToast.className = `flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg border text-sm font-medium toast-in ${mapaColores[tipo] || mapaColores.info}`;
    elementoToast.innerHTML = `
        ${mapaIconos[tipo] || mapaIconos.info}
        <span class="flex-1">${escaparHTML(mensaje)}</span>
        <button class="text-white/80 hover:text-white ml-2 focus:outline-none">&times;</button>
    `;

    elementoToast.querySelector('button').addEventListener('click', () => {
        elementoToast.classList.remove('toast-in');
        elementoToast.classList.add('toast-out');
        setTimeout(() => elementoToast.remove(), 300);
    });

    contenedorNotificaciones.appendChild(elementoToast);

    // Cierre automático después de 4 segundos
    setTimeout(() => {
        if (elementoToast.parentElement) {
            elementoToast.classList.remove('toast-in');
            elementoToast.classList.add('toast-out');
            setTimeout(() => elementoToast.remove(), 300);
        }
    }, 4000);
}

/**
 * Abre un modal por su ID aplicando estilos y accesibilidad.
 * @param {string} idModal 
 */
export function abrirModal(idModal) {
    const elementoModal = document.getElementById(idModal);
    if (elementoModal) {
        elementoModal.classList.remove('hidden');
        elementoModal.classList.add('flex');
        document.body.classList.add('overflow-hidden');
    }
}

/**
 * Cierra un modal por su ID.
 * @param {string} idModal 
 */
export function cerrarModal(idModal) {
    const elementoModal = document.getElementById(idModal);
    if (elementoModal) {
        elementoModal.classList.add('hidden');
        elementoModal.classList.remove('flex');
        document.body.classList.remove('overflow-hidden');
    }
}

/**
 * Actualiza las estadísticas del catálogo en el DOM en tiempo real.
 * @param {Array} listaProductos 
 */
export function renderizarEstadisticas(listaProductos) {
    const elTotalProductos = document.getElementById('statTotalProducts');
    const elUnidadesTotales = document.getElementById('statTotalUnits');
    const elValorTotal = document.getElementById('statTotalValue');
    const elStockBajo = document.getElementById('statLowStock');

    if (!elTotalProductos) return;

    const totalProductos = listaProductos.length;
    let unidadesTotales = 0;
    let valorMonetarioTotal = 0;
    let cantidadStockBajo = 0;

    listaProductos.forEach(producto => {
        const stockActual = Number(producto.stock) || 0;
        const precioUnitario = Number(producto.precio !== undefined ? producto.precio : producto.price) || 0;
        unidadesTotales += stockActual;
        valorMonetarioTotal += (stockActual * precioUnitario);
        if (stockActual < 20) cantidadStockBajo++;
    });

    elTotalProductos.textContent = totalProductos;
    elUnidadesTotales.textContent = unidadesTotales;
    elValorTotal.textContent = `S/ ${valorMonetarioTotal.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    elStockBajo.textContent = cantidadStockBajo;
}

/**
 * Renderiza los productos en formato cuadrícula de tarjetas (Cards).
 * @param {Array} listaProductos 
 * @param {HTMLElement} contenedorDestino 
 */
export function renderizarTarjetas(listaProductos, contenedorDestino) {
    contenedorDestino.innerHTML = '';

    if (!listaProductos || listaProductos.length === 0) {
        contenedorDestino.innerHTML = `
            <div class="col-span-full py-16 text-center bg-white rounded-2xl border border-dashed border-slate-300 p-8">
                <div class="w-16 h-16 mx-auto mb-4 bg-indigo-50 text-indigo-500 rounded-full flex items-center justify-center">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/></svg>
                </div>
                <h3 class="text-lg font-bold text-slate-700">No se encontraron útiles escolares</h3>
                <p class="text-sm text-slate-500 mt-1 max-w-sm mx-auto">No hay productos que coincidan con la búsqueda o categoría elegida.</p>
            </div>
        `;
        return;
    }

    listaProductos.forEach(producto => {
        const elementoTarjeta = document.createElement('article');
        elementoTarjeta.className = 'bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden flex flex-col card-hover';

        // Badge de stock dinámico según disponibilidad
        let claseBadgeStock = 'bg-emerald-50 text-emerald-700 border-emerald-200';
        let textoStock = `${producto.stock} en stock`;
        if (producto.stock === 0) {
            claseBadgeStock = 'bg-rose-50 text-rose-700 border-rose-200';
            textoStock = 'Agotado';
        } else if (producto.stock < 20) {
            claseBadgeStock = 'bg-amber-50 text-amber-700 border-amber-200';
            textoStock = `Bajo stock (${producto.stock})`;
        }

        const skuProducto = producto.codigo_sku || producto.sku || '';
        const nombreProducto = producto.nombre || producto.name || '';
        const categoriaProducto = producto.categoria || producto.category || '';
        const precioProducto = producto.precio !== undefined ? producto.precio : producto.price;
        const descripcionProducto = producto.descripcion || producto.description || '';
        const imagenUrl = producto.imagen_url || producto.image_url || 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&auto=format&fit=crop&q=80';

        elementoTarjeta.innerHTML = `
            <div class="relative h-44 bg-slate-100 overflow-hidden group">
                <img src="${escaparHTML(imagenUrl)}" alt="${escaparHTML(nombreProducto)}" class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105" onerror="this.src='https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&auto=format&fit=crop&q=80'">
                <div class="absolute top-3 left-3 bg-white/90 backdrop-blur-sm text-xs font-semibold px-2.5 py-1 rounded-md text-slate-700 shadow-sm">
                    ${escaparHTML(categoriaProducto)}
                </div>
                <div class="absolute top-3 right-3 text-xs font-mono font-medium px-2 py-0.5 rounded bg-slate-900/75 text-white backdrop-blur-sm">
                    ${escaparHTML(skuProducto)}
                </div>
            </div>

            <div class="p-5 flex-1 flex flex-col">
                <h4 class="font-bold text-slate-800 text-base line-clamp-1 mb-1.5" title="${escaparHTML(nombreProducto)}">
                    ${escaparHTML(nombreProducto)}
                </h4>
                <p class="text-xs text-slate-500 line-clamp-2 mb-4 flex-1">
                    ${escaparHTML(descripcionProducto || 'Sin descripción disponible.')}
                </p>

                <div class="flex items-center justify-between pt-3 border-t border-slate-100 mb-4">
                    <div>
                        <span class="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">Precio Unitario</span>
                        <span class="text-xl font-extrabold text-indigo-600">S/ ${Number(precioProducto).toFixed(2)}</span>
                    </div>
                    <span class="text-xs font-semibold px-2.5 py-1 rounded-full border ${claseBadgeStock}">
                        ${textoStock}
                    </span>
                </div>

                <div class="flex items-center gap-2 pt-1">
                    <button data-action="edit" data-id="${producto.id}" class="flex-1 py-2 px-3 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 hover:text-slate-900 rounded-lg transition-colors flex items-center justify-center gap-1.5">
                        <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/></svg>
                        Editar
                    </button>
                    <button data-action="delete" data-id="${producto.id}" data-name="${escaparHTML(nombreProducto)}" class="py-2 px-3 text-xs font-semibold text-rose-600 bg-rose-50 hover:bg-rose-100 rounded-lg transition-colors flex items-center justify-center">
                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                    </button>
                </div>
            </div>
        `;

        contenedorDestino.appendChild(elementoTarjeta);
    });
}

/**
 * Renderiza los productos en formato tabla tabular semántica.
 * @param {Array} listaProductos 
 * @param {HTMLElement} contenedorDestino 
 */
export function renderizarTabla(listaProductos, contenedorDestino) {
    contenedorDestino.innerHTML = '';

    if (!listaProductos || listaProductos.length === 0) {
        contenedorDestino.innerHTML = `<tr><td colspan="6" class="text-center py-10 text-slate-400">No hay productos que mostrar</td></tr>`;
        return;
    }

    listaProductos.forEach(producto => {
        const filaTabla = document.createElement('tr');
        filaTabla.className = 'hover:bg-slate-50/80 transition-colors border-b border-slate-100';

        let badgeStock = 'text-emerald-700 bg-emerald-50 border-emerald-200';
        if (producto.stock === 0) badgeStock = 'text-rose-700 bg-rose-50 border-rose-200';
        else if (producto.stock < 20) badgeStock = 'text-amber-700 bg-amber-50 border-amber-200';

        const skuProducto = producto.codigo_sku || producto.sku || '';
        const nombreProducto = producto.nombre || producto.name || '';
        const categoriaProducto = producto.categoria || producto.category || '';
        const precioProducto = producto.precio !== undefined ? producto.precio : producto.price;

        filaTabla.innerHTML = `
            <td class="py-3.5 px-4 font-mono text-xs font-semibold text-slate-600">${escaparHTML(skuProducto)}</td>
            <td class="py-3.5 px-4 font-medium text-slate-800">${escaparHTML(nombreProducto)}</td>
            <td class="py-3.5 px-4 text-xs text-slate-600"><span class="px-2 py-0.5 rounded bg-slate-100">${escaparHTML(categoriaProducto)}</span></td>
            <td class="py-3.5 px-4 font-bold text-indigo-600">S/ ${Number(precioProducto).toFixed(2)}</td>
            <td class="py-3.5 px-4"><span class="px-2 py-0.5 rounded-full text-xs font-semibold border ${badgeStock}">${producto.stock} unids.</span></td>
            <td class="py-3.5 px-4 text-right">
                <div class="flex items-center justify-end gap-1.5">
                    <button data-action="edit" data-id="${producto.id}" class="p-1.5 text-slate-500 hover:text-indigo-600 hover:bg-indigo-50 rounded transition-colors" title="Editar">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/></svg>
                    </button>
                    <button data-action="delete" data-id="${producto.id}" data-name="${escaparHTML(nombreProducto)}" class="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded transition-colors" title="Eliminar">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                    </button>
                </div>
            </td>
        `;

        contenedorDestino.appendChild(filaTabla);
    });
}

/**
 * Muestra error visual en un campo específico de formulario (DOM).
 * @param {HTMLInputElement} elementoInput 
 * @param {string} mensajeError 
 */
export function mostrarErrorCampo(elementoInput, mensajeError) {
    if (!elementoInput) return;
    elementoInput.classList.add('border-rose-500', 'focus:ring-rose-500');
    elementoInput.classList.remove('border-slate-200', 'focus:ring-indigo-500');

    let etiquetaError = elementoInput.parentElement.querySelector('.form-error-msg');
    if (!etiquetaError) {
        etiquetaError = document.createElement('span');
        etiquetaError.className = 'form-error-msg text-[11px] text-rose-500 font-medium mt-1 block';
        elementoInput.parentElement.appendChild(etiquetaError);
    }
    etiquetaError.textContent = mensajeError;
}

/**
 * Limpia los estilos de error de todos los campos de formulario.
 * @param {HTMLFormElement} elementoFormulario 
 */
export function limpiarErroresCampos(elementoFormulario) {
    if (!elementoFormulario) return;
    elementoFormulario.querySelectorAll('.form-error-msg').forEach(el => el.remove());
    elementoFormulario.querySelectorAll('input, select, textarea').forEach(el => {
        el.classList.remove('border-rose-500', 'focus:ring-rose-500');
        el.classList.add('border-slate-200');
    });
}

// Alias para compatibilidad
export const escapeHTML = escaparHTML;
export const showToast = mostrarToast;
export const openModal = abrirModal;
export const closeModal = cerrarModal;
export const renderStats = renderizarEstadisticas;
export const renderProductCards = renderizarTarjetas;
export const renderProductTable = renderizarTabla;
export const showFieldError = mostrarErrorCampo;
export const clearFieldErrors = limpiarErroresCampos;
