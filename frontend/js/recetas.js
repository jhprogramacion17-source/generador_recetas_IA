/* ==========================================
   SMARTRECIPE AI - MODULO DE RECETAS
   ========================================== */

const Recetas = (() => {

    // ---- INICIALIZAR ----
    function init() {
        const btnGenerar = document.getElementById('btn-generar-receta');
        const btnRetry = document.getElementById('btn-retry-generate');
        const modalReceta = document.getElementById('modal-receta');

        btnGenerar.addEventListener('click', generarReceta);
        btnRetry.addEventListener('click', generarReceta);

        // Cerrar modal receta
        modalReceta.querySelectorAll('.modal-close, .modal-overlay')
            .forEach(el => {
                el.addEventListener('click', () => {
                    UI.closeModal('modal-receta');
                });
            });
    }

    // ---- GENERAR RECETA ----
    async function generarReceta() {
        const ingredientes = Ingredientes.getLista();

        if (ingredientes.length === 0) {
            UI.toast('Agrega ingredientes antes de generar una receta', 'error');
            UI.switchTab('ingredientes');
            return;
        }

        // Mostrar estado de carga
        UI.show('generate-loading');
        UI.hide('generate-result');
        UI.hide('generate-error');
        UI.hide('generate-preview');

        const btnGenerar = document.getElementById('btn-generar-receta');
        btnGenerar.disabled = true;

        try {
            const receta = await API.generarReceta();

            UI.hide('generate-loading');
            btnGenerar.disabled = false;

            // Mostrar resultado
            mostrarRecetaGenerada(receta);

            UI.toast('¡Receta generada con éxito!', 'success');

        } catch (err) {
            UI.hide('generate-loading');
            btnGenerar.disabled = false;

            document.getElementById('generate-error-msg').textContent =
                err.message || 'Error al generar la receta';
            UI.show('generate-error');
        }
    }

    // ---- MOSTRAR RECETA GENERADA ----
    function mostrarRecetaGenerada(receta) {
        const container = document.getElementById('generate-result');

        container.innerHTML = `
            <div class="receta-detalle">
                <div class="detalle-header">
                    <h2>${escapeHTML(receta.nombre)}</h2>
                    <div class="detalle-meta">
                        <div class="detalle-meta-item">
                            <span class="material-icons-round">schedule</span>
                            ${UI.formatTime(receta.tiempo_estimado)}
                        </div>
                        <div class="detalle-meta-item">
                            <span class="material-icons-round">signal_cellular_alt</span>
                            ${UI.difficultyBadge(receta.dificultad)}
                        </div>
                        <div class="detalle-meta-item">
                            <span class="material-icons-round">restaurant</span>
                            ${receta.ingredientes_json.length} ingredientes
                        </div>
                    </div>
                </div>

                <div class="detalle-section">
                    <h3>
                        <span class="material-icons-round">shopping_cart</span>
                        Ingredientes
                    </h3>
                    <table class="ingredientes-tabla">
                        <thead>
                            <tr>
                                <th>Ingrediente</th>
                                <th>Cantidad</th>
                                <th>Unidad</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${receta.ingredientes_json.map(ing => `
                                <tr>
                                    <td>${escapeHTML(ing.nombre)}</td>
                                    <td>${ing.cantidad}</td>
                                    <td>${escapeHTML(ing.unidad)}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>

                <div class="detalle-section">
                    <h3>
                        <span class="material-icons-round">format_list_numbered</span>
                        Preparación
                    </h3>
                    <ol class="pasos-lista">
                        ${receta.pasos_json.map(paso => `
                            <li>${escapeHTML(paso)}</li>
                        `).join('')}
                    </ol>
                </div>

                <div class="detalle-actions">
                    <button class="btn btn-primary" onclick="Recetas.toggleFavorita(${receta.id}, true)">
                        <span class="material-icons-round">favorite</span>
                        Agregar a Favoritas
                    </button>
                    <button class="btn btn-secondary" onclick="UI.switchTab('historial'); Recetas.cargarHistorial();">
                        <span class="material-icons-round">history</span>
                        Ver Historial
                    </button>
                </div>
            </div>
        `;

        UI.show(container);
    }


    // ---- CARGAR PREVIEW DE INGREDIENTES ----
    function cargarPreview() {
        const ingredientes = Ingredientes.getLista();
        const container = document.getElementById('generate-ingredients-list');
        const preview = document.getElementById('generate-preview');

        if (ingredientes.length === 0) {
            UI.hide(preview);
            return;
        }

        container.innerHTML = ingredientes.map(ing =>
            `<span class="chip">${escapeHTML(ing.nombre)} · ${ing.cantidad} ${escapeHTML(ing.unidad)}</span>`
        ).join('');

        UI.show(preview);
    }


    // ---- CARGAR HISTORIAL ----
    async function cargarHistorial() {
        try {
            const recetas = await API.listarRecetas();
            renderizarRecetas(recetas, 'historial-list', 'historial-empty');
        } catch (err) {
            UI.toast('Error al cargar historial', 'error');
        }
    }


    // ---- CARGAR FAVORITAS ----
    async function cargarFavoritas() {
        try {
            const recetas = await API.listarFavoritas();
            renderizarRecetas(recetas, 'favoritas-list', 'favoritas-empty');
        } catch (err) {
            UI.toast('Error al cargar favoritas', 'error');
        }
    }


    // ---- RENDERIZAR LISTA DE RECETAS ----
    function renderizarRecetas(recetas, listId, emptyId) {
        const listEl = document.getElementById(listId);
        const emptyEl = document.getElementById(emptyId);

        if (recetas.length === 0) {
            listEl.innerHTML = '';
            UI.show(emptyEl);
            return;
        }

        UI.hide(emptyEl);

        listEl.innerHTML = recetas.map(receta => `
            <div class="receta-card" onclick="Recetas.verDetalle(${receta.id})">
                <div class="card-gradient">
                    <h3>${escapeHTML(receta.nombre)}</h3>
                    <span class="card-date">${UI.formatDate(receta.fecha_creacion)}</span>
                    <button class="favorite-btn ${receta.favorita ? 'active' : ''}"
                            onclick="event.stopPropagation(); Recetas.toggleFavorita(${receta.id}, ${!receta.favorita})"
                            title="${receta.favorita ? 'Quitar de favoritas' : 'Agregar a favoritas'}">
                        <span class="material-icons-round">
                            ${receta.favorita ? 'favorite' : 'favorite_border'}
                        </span>
                    </button>
                </div>
                <div class="card-body">
                    <div class="card-meta">
                        <div class="meta-item">
                            <span class="material-icons-round">schedule</span>
                            ${UI.formatTime(receta.tiempo_estimado)}
                        </div>
                        <div class="meta-item">
                            <span class="material-icons-round">restaurant</span>
                            ${receta.ingredientes_json.length} ing.
                        </div>
                        <div class="meta-item">
                            ${UI.difficultyBadge(receta.dificultad)}
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }


    // ---- VER DETALLE ----
    async function verDetalle(id) {
        try {
            const receta = await API.obtenerReceta(id);

            // Intentar obtener calificación
            let calificacion = 0;
            try {
                const cal = await API.obtenerCalificacion(id);
                calificacion = cal.puntuacion;
            } catch (e) {
                // Sin calificación aún
            }

            const body = document.getElementById('modal-receta-body');
            document.getElementById('modal-receta-title').textContent = receta.nombre;

            body.innerHTML = `
                <div class="receta-detalle">
                    <div class="detalle-header">
                        <h2>${escapeHTML(receta.nombre)}</h2>
                        <div class="detalle-meta">
                            <div class="detalle-meta-item">
                                <span class="material-icons-round">schedule</span>
                                ${UI.formatTime(receta.tiempo_estimado)}
                            </div>
                            <div class="detalle-meta-item">
                                <span class="material-icons-round">signal_cellular_alt</span>
                                ${UI.difficultyBadge(receta.dificultad)}
                            </div>
                            <div class="detalle-meta-item">
                                <span class="material-icons-round">calendar_today</span>
                                ${UI.formatDate(receta.fecha_creacion)}
                            </div>
                        </div>
                    </div>

                    <div class="rating-section">
                        <h4>Tu calificación</h4>
                        <div class="rating-stars" data-receta-id="${receta.id}"
                             data-current="${calificacion}">
                            ${UI.starsHTML(calificacion, true)}
                        </div>
                    </div>

                    <div class="detalle-section">
                        <h3>
                            <span class="material-icons-round">shopping_cart</span>
                            Ingredientes
                        </h3>
                        <table class="ingredientes-tabla">
                            <thead>
                                <tr>
                                    <th>Ingrediente</th>
                                    <th>Cantidad</th>
                                    <th>Unidad</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${receta.ingredientes_json.map(ing => `
                                    <tr>
                                        <td>${escapeHTML(ing.nombre)}</td>
                                        <td>${ing.cantidad}</td>
                                        <td>${escapeHTML(ing.unidad)}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>

                    <div class="detalle-section">
                        <h3>
                            <span class="material-icons-round">format_list_numbered</span>
                            Preparación
                        </h3>
                        <ol class="pasos-lista">
                            ${receta.pasos_json.map(paso => `
                                <li>${escapeHTML(paso)}</li>
                            `).join('')}
                        </ol>
                    </div>

                    <div class="detalle-actions">
                        <button class="btn ${receta.favorita ? 'btn-secondary' : 'btn-primary'}"
                                onclick="Recetas.toggleFavorita(${receta.id}, ${!receta.favorita}); UI.closeModal('modal-receta');">
                            <span class="material-icons-round">
                                ${receta.favorita ? 'heart_broken' : 'favorite'}
                            </span>
                            ${receta.favorita ? 'Quitar de Favoritas' : 'Agregar a Favoritas'}
                        </button>
                        <button class="btn btn-danger"
                                onclick="Recetas.eliminar(${receta.id}, '${escapeHTML(receta.nombre)}')">
                            <span class="material-icons-round">delete</span>
                            Eliminar
                        </button>
                    </div>
                </div>
            `;

            // Configurar estrellas interactivas
            configurarEstrellas(body, receta.id, calificacion);

            UI.openModal('modal-receta');

        } catch (err) {
            UI.toast('Error al cargar la receta', 'error');
        }
    }


    // ---- CONFIGURAR ESTRELLAS ----
    function configurarEstrellas(container, recetaId, calificacionActual) {
        const stars = container.querySelectorAll('.rating-stars .star');

        stars.forEach(star => {
            star.addEventListener('click', async () => {
                const rating = parseInt(star.dataset.rating);

                try {
                    if (calificacionActual > 0) {
                        await API.actualizarCalificacion(recetaId, rating);
                    } else {
                        await API.calificarReceta(recetaId, rating);
                    }

                    // Actualizar estrellas visualmente
                    stars.forEach(s => {
                        const r = parseInt(s.dataset.rating);
                        s.classList.toggle('active', r <= rating);
                    });

                    calificacionActual = rating;

                    UI.toast(`Calificación: ${rating} estrella${rating > 1 ? 's' : ''}`, 'success');

                } catch (err) {
                    UI.toast(err.message || 'Error al calificar', 'error');
                }
            });
        });
    }


    // ---- TOGGLE FAVORITA ----
    async function toggleFavorita(id, favorita) {
        try {
            await API.toggleFavorita(id, favorita);
            UI.toast(
                favorita ? 'Agregada a favoritas' : 'Removida de favoritas',
                'success'
            );

            // Recargar listas
            cargarHistorial();
            cargarFavoritas();

        } catch (err) {
            UI.toast('Error al actualizar favorita', 'error');
        }
    }


    // ---- ELIMINAR RECETA ----
    async function eliminar(id, nombre) {
        if (!UI.confirm(`¿Eliminar la receta "${nombre}"?`)) return;

        try {
            await API.eliminarReceta(id);
            UI.closeModal('modal-receta');
            UI.toast('Receta eliminada', 'success');

            cargarHistorial();
            cargarFavoritas();

        } catch (err) {
            UI.toast('Error al eliminar la receta', 'error');
        }
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
        cargarPreview,
        cargarHistorial,
        cargarFavoritas,
        verDetalle,
        toggleFavorita,
        eliminar
    };

})();
