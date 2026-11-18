/* ==========================================
   SMARTRECIPE AI - MODULO DE INGREDIENTES
   ========================================== */

const Ingredientes = (() => {

    let ingredientes = [];

    // ---- INICIALIZAR ----
    function init() {
        const btnAdd = document.getElementById('btn-add-ingrediente');
        const form = document.getElementById('form-ingrediente');
        const modal = document.getElementById('modal-ingrediente');

        // Abrir modal para agregar
        btnAdd.addEventListener('click', () => {
            abrirFormulario();
        });

        // Enviar formulario
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await guardarIngrediente();
        });

        // Cerrar modales con overlay o botón
        modal.querySelectorAll('.modal-close, .modal-overlay')
            .forEach(el => {
                el.addEventListener('click', () => {
                    UI.closeModal('modal-ingrediente');
                });
            });
    }

    // ---- CARGAR INGREDIENTES ----
    async function cargar() {
        try {
            ingredientes = await API.listarIngredientes();
            renderizar();
        } catch (err) {
            UI.toast('Error al cargar ingredientes', 'error');
        }
    }

    // ---- RENDERIZAR LISTA ----
    function renderizar() {
        const listEl = document.getElementById('ingredientes-list');
        const emptyEl = document.getElementById('ingredientes-empty');

        if (ingredientes.length === 0) {
            listEl.innerHTML = '';
            UI.show(emptyEl);
            return;
        }

        UI.hide(emptyEl);

        listEl.innerHTML = ingredientes.map(ing => `
            <div class="ingrediente-card" data-id="${ing.id}">
                <div class="card-header">
                    <span class="card-name">${escapeHTML(ing.nombre)}</span>
                    <div class="card-actions">
                        <button class="btn-icon" title="Editar"
                                onclick="Ingredientes.editar(${ing.id})">
                            <span class="material-icons-round">edit</span>
                        </button>
                        <button class="btn-icon" title="Eliminar"
                                onclick="Ingredientes.eliminar(${ing.id}, '${escapeHTML(ing.nombre)}')">
                            <span class="material-icons-round">delete</span>
                        </button>
                    </div>
                </div>
                <div class="card-info">
                    <span class="cantidad">${ing.cantidad}</span>
                    <span class="unidad">${escapeHTML(ing.unidad)}</span>
                </div>
            </div>
        `).join('');
    }

    // ---- ABRIR FORMULARIO (NUEVO) ----
    function abrirFormulario(ingrediente = null) {
        const titulo = document.getElementById('modal-ingrediente-title');
        const idInput = document.getElementById('ingrediente-id');
        const nombre = document.getElementById('ingrediente-nombre');
        const cantidad = document.getElementById('ingrediente-cantidad');
        const unidad = document.getElementById('ingrediente-unidad');

        UI.hide('ingrediente-error');

        if (ingrediente) {
            titulo.textContent = 'Editar Ingrediente';
            idInput.value = ingrediente.id;
            nombre.value = ingrediente.nombre;
            cantidad.value = ingrediente.cantidad;
            unidad.value = ingrediente.unidad;
        } else {
            titulo.textContent = 'Agregar Ingrediente';
            idInput.value = '';
            document.getElementById('form-ingrediente').reset();
        }

        UI.openModal('modal-ingrediente');
        nombre.focus();
    }

    // ---- EDITAR ----
    async function editar(id) {
        const ingrediente = ingredientes.find(i => i.id === id);
        if (ingrediente) {
            abrirFormulario(ingrediente);
        }
    }

    // ---- GUARDAR (CREAR O ACTUALIZAR) ----
    async function guardarIngrediente() {
        const id = document.getElementById('ingrediente-id').value;
        const nombre = document.getElementById('ingrediente-nombre').value.trim();
        const cantidad = parseFloat(document.getElementById('ingrediente-cantidad').value);
        const unidad = document.getElementById('ingrediente-unidad').value;
        const errorEl = document.getElementById('ingrediente-error');

        UI.hide(errorEl);

        if (!nombre || !cantidad || !unidad) {
            errorEl.textContent = 'Completa todos los campos';
            UI.show(errorEl);
            return;
        }

        const datos = { nombre, cantidad, unidad };

        try {
            if (id) {
                await API.actualizarIngrediente(parseInt(id), datos);
                UI.toast('Ingrediente actualizado', 'success');
            } else {
                await API.crearIngrediente(datos);
                UI.toast('Ingrediente agregado', 'success');
            }

            UI.closeModal('modal-ingrediente');
            await cargar();

        } catch (err) {
            errorEl.textContent = err.message;
            UI.show(errorEl);
        }
    }

    // ---- ELIMINAR ----
    async function eliminar(id, nombre) {
        if (!UI.confirm(`¿Eliminar "${nombre}" de tu inventario?`)) return;

        try {
            await API.eliminarIngrediente(id);
            UI.toast('Ingrediente eliminado', 'success');
            await cargar();
        } catch (err) {
            UI.toast('Error al eliminar ingrediente', 'error');
        }
    }

    // ---- OBTENER LISTA ----
    function getLista() {
        return ingredientes;
    }

    // ---- HELPER ----
    function escapeHTML(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }


    // ---- INTERFAZ PÚBLICA ----
    return {
        init,
        cargar,
        editar,
        eliminar,
        getLista
    };

})();
