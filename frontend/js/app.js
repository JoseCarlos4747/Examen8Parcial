/**
 * Archivo Principal de la Aplicación Frontend EduPapel
 * Implementa el flujo de control, gestión de eventos del usuario,
 * coordinación de asincronía (Fetch API) y manipulación del DOM en Vanilla JS.
 */
import { ApiService } from './api.js';
import {
    renderProductCards,
    renderProductTable,
    renderStats,
    showToast,
    openModal,
    closeModal,
    showFieldError,
    clearFieldErrors
} from './dom.js';

// ================= ESTADO DE LA APLICACIÓN =================
const state = {
    products: [],
    selectedCategory: 'Todas',
    searchQuery: '',
    currentSort: 'name_asc',
    currentView: 'grid', // 'grid' | 'table'
    currentUser: JSON.parse(localStorage.getItem('edupapel_user') || 'null'),
    pendingDelete: null // { id, name }
};

// ================= SELECTORES DEL DOM =================
const DOM = {
    // Badges y Botones de cabecera
    apiStatusBadge: document.getElementById('apiStatusBadge'),
    btnOpenAuth: document.getElementById('btnOpenAuth'),
    authStatusText: document.getElementById('authStatusText'),
    btnOpenNewProduct: document.getElementById('btnOpenNewProduct'),

    // Filtros y Búsqueda
    categoryPillsContainer: document.getElementById('categoryPillsContainer'),
    searchInput: document.getElementById('searchInput'),
    btnClearSearch: document.getElementById('btnClearSearch'),
    sortSelect: document.getElementById('sortSelect'),
    btnViewGrid: document.getElementById('btnViewGrid'),
    btnViewTable: document.getElementById('btnViewTable'),

    // Contenedores del catálogo
    loadingState: document.getElementById('loadingState'),
    productsGrid: document.getElementById('productsGrid'),
    productsTableContainer: document.getElementById('productsTableContainer'),
    productsTableBody: document.getElementById('productsTableBody'),

    // Modal Producto
    productModal: document.getElementById('productModal'),
    productModalTitle: document.getElementById('productModalTitle'),
    productForm: document.getElementById('productForm'),
    formProductId: document.getElementById('formProductId'),
    formSku: document.getElementById('formSku'),
    formCategory: document.getElementById('formCategory'),
    formName: document.getElementById('formName'),
    formPrice: document.getElementById('formPrice'),
    formStock: document.getElementById('formStock'),
    formImageUrl: document.getElementById('formImageUrl'),
    formDescription: document.getElementById('formDescription'),
    btnCancelProductModal: document.getElementById('btnCancelProductModal'),
    btnCloseProductModal: document.getElementById('btnCloseProductModal'),
    btnSaveProduct: document.getElementById('btnSaveProduct'),

    // Modal Eliminar
    deleteModal: document.getElementById('deleteModal'),
    deleteProductName: document.getElementById('deleteProductName'),
    btnCancelDelete: document.getElementById('btnCancelDelete'),
    btnConfirmDelete: document.getElementById('btnConfirmDelete'),

    // Modal Auth
    authModal: document.getElementById('authModal'),
    authForm: document.getElementById('authForm'),
    authIdentifier: document.getElementById('authIdentifier'),
    authPassword: document.getElementById('authPassword'),
    btnCloseAuthModal: document.getElementById('btnCloseAuthModal'),
    btnSubmitAuth: document.getElementById('btnSubmitAuth')
};

// ================= INICIALIZACIÓN =================
document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

async function initApp() {
    updateAuthUI();
    registerEventListeners();
    await checkApiStatus();
    await loadProducts();
}

/**
 * Verifica si el backend está respondiendo adecuadamente.
 */
async function checkApiStatus() {
    const isOnline = await ApiService.checkHealth();
    if (DOM.apiStatusBadge) {
        if (isOnline) {
            DOM.apiStatusBadge.className = 'hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200';
            DOM.apiStatusBadge.innerHTML = '<span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span><span>API Online</span>';
        } else {
            DOM.apiStatusBadge.className = 'hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200';
            DOM.apiStatusBadge.innerHTML = '<span class="w-2 h-2 rounded-full bg-rose-500"></span><span>API Desconectada</span>';
        }
    }
}

/**
 * Carga productos desde el Backend de forma asíncrona (Semana 4: Fetch API).
 */
async function loadProducts() {
    try {
        setLoading(true);
        const data = await ApiService.getProducts(state.searchQuery, state.selectedCategory);
        state.products = data;
        renderCatalog();
        renderStats(state.products);
    } catch (error) {
        showToast(`Error al cargar catálogo: ${error.message}`, 'error');
    } finally {
        setLoading(false);
    }
}

/**
 * Muestra o esconde el estado de carga en el DOM.
 */
function setLoading(isLoading) {
    if (isLoading) {
        DOM.loadingState.classList.remove('hidden');
        DOM.productsGrid.classList.add('hidden');
        DOM.productsTableContainer.classList.add('hidden');
    } else {
        DOM.loadingState.classList.add('hidden');
        if (state.currentView === 'grid') {
            DOM.productsGrid.classList.remove('hidden');
            DOM.productsTableContainer.classList.add('hidden');
        } else {
            DOM.productsGrid.classList.add('hidden');
            DOM.productsTableContainer.classList.remove('hidden');
        }
    }
}

/**
 * Aplica ordenación en memoria y renderiza en la vista seleccionada.
 */
function renderCatalog() {
    let sorted = [...state.products];

    // Ordenamiento dinámico
    switch (state.currentSort) {
        case 'name_asc':
            sorted.sort((a, b) => a.name.localeCompare(b.name));
            break;
        case 'name_desc':
            sorted.sort((a, b) => b.name.localeCompare(a.name));
            break;
        case 'price_asc':
            sorted.sort((a, b) => a.price - b.price);
            break;
        case 'price_desc':
            sorted.sort((a, b) => b.price - a.price);
            break;
        case 'stock_asc':
            sorted.sort((a, b) => a.stock - b.stock);
            break;
        case 'stock_desc':
            sorted.sort((a, b) => b.stock - a.stock);
            break;
    }

    if (state.currentView === 'grid') {
        renderProductCards(sorted, DOM.productsGrid);
    } else {
        renderProductTable(sorted, DOM.productsTableBody);
    }
}

// ================= GESTIÓN DE EVENTOS (SEMANAS 1 A 3) =================
function registerEventListeners() {
    // 1. Filtro por categoría (Pills)
    DOM.categoryPillsContainer.addEventListener('click', (e) => {
        const targetBtn = e.target.closest('button[data-category]');
        if (!targetBtn) return;

        DOM.categoryPillsContainer.querySelectorAll('.category-pill').forEach(btn => {
            btn.classList.remove('active', 'bg-brand-600', 'text-white', 'shadow-sm');
            btn.classList.add('text-slate-600', 'hover:text-slate-900', 'hover:bg-slate-100');
        });

        targetBtn.classList.add('active', 'bg-brand-600', 'text-white', 'shadow-sm');
        targetBtn.classList.remove('text-slate-600', 'hover:text-slate-900', 'hover:bg-slate-100');

        state.selectedCategory = targetBtn.dataset.category;
        loadProducts();
    });

    // 2. Búsqueda en tiempo real (Input con debounce)
    let searchDebounceTimeout = null;
    DOM.searchInput.addEventListener('input', (e) => {
        const val = e.target.value.trim();
        DOM.btnClearSearch.classList.toggle('hidden', val === '');

        clearTimeout(searchDebounceTimeout);
        searchDebounceTimeout = setTimeout(() => {
            state.searchQuery = val;
            loadProducts();
        }, 300);
    });

    DOM.btnClearSearch.addEventListener('click', () => {
        DOM.searchInput.value = '';
        DOM.btnClearSearch.classList.add('hidden');
        state.searchQuery = '';
        loadProducts();
    });

    // 3. Ordenación
    DOM.sortSelect.addEventListener('change', (e) => {
        state.currentSort = e.target.value;
        renderCatalog();
    });

    // 4. Conmutar Vistas (Grid vs Tabla)
    DOM.btnViewGrid.addEventListener('click', () => {
        state.currentView = 'grid';
        DOM.btnViewGrid.classList.add('text-brand-600', 'bg-brand-50');
        DOM.btnViewGrid.classList.remove('text-slate-400');
        DOM.btnViewTable.classList.remove('text-brand-600', 'bg-brand-50');
        DOM.btnViewTable.classList.add('text-slate-400');
        setLoading(false);
        renderCatalog();
    });

    DOM.btnViewTable.addEventListener('click', () => {
        state.currentView = 'table';
        DOM.btnViewTable.classList.add('text-brand-600', 'bg-brand-50');
        DOM.btnViewTable.classList.remove('text-slate-400');
        DOM.btnViewGrid.classList.remove('text-brand-600', 'bg-brand-50');
        DOM.btnViewGrid.classList.add('text-slate-400');
        setLoading(false);
        renderCatalog();
    });

    // 5. Botón Abrir Modal Nuevo Producto
    DOM.btnOpenNewProduct.addEventListener('click', () => {
        resetProductForm();
        DOM.productModalTitle.textContent = 'Nuevo Útil Escolar';
        openModal('productModal');
    });

    DOM.btnCancelProductModal.addEventListener('click', () => closeModal('productModal'));
    DOM.btnCloseProductModal.addEventListener('click', () => closeModal('productModal'));

    // 6. Envío del Formulario de Producto (Submit con validación estricta)
    DOM.productForm.addEventListener('submit', handleProductFormSubmit);

    // 7. Delegación de Eventos en Tarjetas y Tabla (Editar y Eliminar)
    const handleProductAction = (e) => {
        const editBtn = e.target.closest('button[data-action="edit"]');
        const deleteBtn = e.target.closest('button[data-action="delete"]');

        if (editBtn) {
            const productId = editBtn.dataset.id;
            handleEditClick(productId);
        } else if (deleteBtn) {
            const productId = deleteBtn.dataset.id;
            const productName = deleteBtn.dataset.name || 'este producto';
            handleDeleteClick(productId, productName);
        }
    };

    DOM.productsGrid.addEventListener('click', handleProductAction);
    DOM.productsTableContainer.addEventListener('click', handleProductAction);

    // 8. Confirmación de Eliminación
    DOM.btnCancelDelete.addEventListener('click', () => closeModal('deleteModal'));
    DOM.btnConfirmDelete.addEventListener('click', confirmDeleteProduct);

    // 9. Login / Sesión de Administrador
    DOM.btnOpenAuth.addEventListener('click', () => {
        if (state.currentUser) {
            // Si ya tiene sesión, dar opción de cerrar sesión
            if (confirm(`¿Deseas cerrar la sesión de @${state.currentUser.username}?`)) {
                localStorage.removeItem('edupapel_user');
                state.currentUser = null;
                updateAuthUI();
                showToast('Sesión finalizada.', 'info');
            }
        } else {
            clearFieldErrors(DOM.authForm);
            DOM.authForm.reset();
            openModal('authModal');
        }
    });

    DOM.btnCloseAuthModal.addEventListener('click', () => closeModal('authModal'));
    DOM.authForm.addEventListener('submit', handleAuthSubmit);
}

// ================= ACCIONES DE PRODUCTO =================

/**
 * Prepara y abre el formulario para editar un producto.
 */
async function handleEditClick(productId) {
    try {
        const product = state.products.find(p => p.id == productId) || await ApiService.getProductById(productId);
        if (!product) throw new Error('Producto no encontrado');

        resetProductForm();
        DOM.formProductId.value = product.id;
        DOM.formSku.value = product.sku;
        DOM.formCategory.value = product.category;
        DOM.formName.value = product.name;
        DOM.formPrice.value = product.price;
        DOM.formStock.value = product.stock;
        DOM.formImageUrl.value = product.image_url || '';
        DOM.formDescription.value = product.description || '';

        DOM.productModalTitle.textContent = 'Editar Útil Escolar';
        openModal('productModal');
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/**
 * Abre el modal para confirmar la eliminación de un útil escolar.
 */
function handleDeleteClick(productId, productName) {
    state.pendingDelete = { id: productId, name: productName };
    DOM.deleteProductName.textContent = `"${productName}"`;
    openModal('deleteModal');
}

/**
 * Ejecuta la llamada DELETE asíncrona al backend.
 */
async function confirmDeleteProduct() {
    if (!state.pendingDelete) return;

    try {
        DOM.btnConfirmDelete.disabled = true;
        DOM.btnConfirmDelete.textContent = 'Eliminando...';

        await ApiService.deleteProduct(state.pendingDelete.id);
        showToast(`"${state.pendingDelete.name}" ha sido eliminado exitosamente.`, 'success');
        closeModal('deleteModal');
        await loadProducts();
    } catch (error) {
        showToast(`Error al eliminar: ${error.message}`, 'error');
    } finally {
        DOM.btnConfirmDelete.disabled = false;
        DOM.btnConfirmDelete.textContent = 'Eliminar';
        state.pendingDelete = null;
    }
}

/**
 * Procesa el envío del formulario (POST / PUT) con validación en el cliente.
 */
async function handleProductFormSubmit(e) {
    e.preventDefault();
    clearFieldErrors(DOM.productForm);

    // 1. Validación en el cliente (DOM & JS Puro)
    let hasErrors = false;

    const sku = DOM.formSku.value.trim().toUpperCase();
    if (!sku) {
        showFieldError(DOM.formSku, 'El código SKU es obligatorio.');
        hasErrors = true;
    }

    const category = DOM.formCategory.value.trim();
    if (!category) {
        showFieldError(DOM.formCategory, 'Seleccione una categoría válida.');
        hasErrors = true;
    }

    const name = DOM.formName.value.trim();
    if (!name || name.length < 3) {
        showFieldError(DOM.formName, 'El nombre debe tener al menos 3 caracteres.');
        hasErrors = true;
    }

    const price = parseFloat(DOM.formPrice.value);
    if (isNaN(price) || price <= 0) {
        showFieldError(DOM.formPrice, 'Ingrese un precio válido mayor a 0.');
        hasErrors = true;
    }

    const stock = parseInt(DOM.formStock.value, 10);
    if (isNaN(stock) || stock < 0) {
        showFieldError(DOM.formStock, 'El stock debe ser un entero mayor o igual a 0.');
        hasErrors = true;
    }

    if (hasErrors) return;

    const payload = {
        sku,
        category,
        name,
        price,
        stock,
        image_url: DOM.formImageUrl.value.trim(),
        description: DOM.formDescription.value.trim()
    };

    const isEditing = Boolean(DOM.formProductId.value);
    const saveBtn = DOM.btnSaveProduct;

    try {
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<span>Guardando...</span>';

        if (isEditing) {
            await ApiService.updateProduct(DOM.formProductId.value, payload);
            showToast('Útil escolar actualizado exitosamente.', 'success');
        } else {
            await ApiService.createProduct(payload);
            showToast('Nuevo útil escolar registrado exitosamente.', 'success');
        }

        closeModal('productModal');
        await loadProducts();
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        saveBtn.disabled = false;
        saveBtn.innerHTML = '<span>Guardar</span>';
    }
}

function resetProductForm() {
    clearFieldErrors(DOM.productForm);
    DOM.productForm.reset();
    DOM.formProductId.value = '';
}

// ================= ACCIONES DE AUTENTICACIÓN =================

async function handleAuthSubmit(e) {
    e.preventDefault();
    clearFieldErrors(DOM.authForm);

    const identifier = DOM.authIdentifier.value.trim();
    const password = DOM.authPassword.value.trim();

    if (!identifier) {
        showFieldError(DOM.authIdentifier, 'Ingrese su usuario o correo.');
        return;
    }
    if (!password) {
        showFieldError(DOM.authPassword, 'Ingrese su contraseña.');
        return;
    }

    try {
        DOM.btnSubmitAuth.disabled = true;
        DOM.btnSubmitAuth.textContent = 'Verificando hash...';

        const result = await ApiService.login({ identifier, password });
        state.currentUser = result.user;
        localStorage.setItem('edupapel_user', JSON.stringify(result.user));

        updateAuthUI();
        closeModal('authModal');
        showToast(`¡Bienvenido, ${result.user.username}! Modo Administrador activado.`, 'success');
    } catch (error) {
        showToast(`Error de autenticación: ${error.message}`, 'error');
    } finally {
        DOM.btnSubmitAuth.disabled = false;
        DOM.btnSubmitAuth.textContent = 'Iniciar Sesión';
    }
}

function updateAuthUI() {
    if (state.currentUser) {
        DOM.authStatusText.textContent = `@${state.currentUser.username} (Salir)`;
        DOM.btnOpenAuth.classList.add('bg-emerald-50', 'text-emerald-700', 'border-emerald-300');
    } else {
        DOM.authStatusText.textContent = 'Admin (Login)';
        DOM.btnOpenAuth.classList.remove('bg-emerald-50', 'text-emerald-700', 'border-emerald-300');
    }
}

