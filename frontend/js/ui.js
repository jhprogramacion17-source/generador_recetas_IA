/* ==========================================
   SMARTRECIPE AI - UTILIDADES DE UI
   ========================================== */

const UI = (() => {

    // ---- VISTAS ----
    function showView(viewId) {
        document.querySelectorAll('.view').forEach(v => {
            v.classList.remove('active');
            v.classList.add('hidden');
        });

        const view = document.getElementById(viewId);
        if (view) {
            view.classList.remove('hidden');
            view.classList.add('active');
        }
    }

    // ---- TABS ----
    function switchTab(tabName) {
        // Actualizar botones de tab
        document.querySelectorAll('.tab').forEach(t => {
            t.classList.toggle('active', t.dataset.tab === tabName);
        });

        // Actualizar contenido
        document.querySelectorAll('.tab-content').forEach(tc => {
            tc.classList.remove('active');
            tc.classList.add('hidden');
        });

        const content = document.getElementById(`tab-${tabName}`);
        if (content) {
            content.classList.remove('hidden');
            content.classList.add('active');
        }
    }

    // ---- MODAL ----
    function openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }
    }

    function closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('hidden');
            document.body.style.overflow = '';
        }
    }

    function closeAllModals() {
        document.querySelectorAll('.modal').forEach(m => {
            m.classList.add('hidden');
        });
        document.body.style.overflow = '';
    }

    // ---- TOAST ----
    function toast(message, type = 'info', duration = 3500) {
        const container = document.getElementById('toast-container');

        const icons = {
            success: 'check_circle',
            error: 'error',
            info: 'info'
        };

        const toastEl = document.createElement('div');
        toastEl.className = `toast toast-${type}`;
        toastEl.innerHTML = `
            <span class="material-icons-round">${icons[type] || 'info'}</span>
            <span>${message}</span>
        `;

        container.appendChild(toastEl);

        setTimeout(() => {
            toastEl.classList.add('fade-out');
            setTimeout(() => toastEl.remove(), 300);
        }, duration);
    }

    // ---- NAVBAR ----
    function showNavbar(userName) {
        const navbar = document.getElementById('navbar');
        const nameEl = document.getElementById('nav-user-name');

        navbar.classList.remove('hidden');
        if (nameEl) nameEl.textContent = userName;
    }

    function hideNavbar() {
        const navbar = document.getElementById('navbar');
        navbar.classList.add('hidden');
    }

    // ---- SPLASH ----
    function hideSplash() {
        const splash = document.getElementById('splash-screen');
        if (splash) {
            splash.classList.add('fade-out');
            setTimeout(() => splash.remove(), 500);
        }
    }

    // ---- HELPERS ----
    function show(el) {
        if (typeof el === 'string') el = document.getElementById(el);
        if (el) el.classList.remove('hidden');
    }

    function hide(el) {
        if (typeof el === 'string') el = document.getElementById(el);
        if (el) el.classList.add('hidden');
    }

    function formatDate(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleDateString('es-ES', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        });
    }

    function formatTime(minutes) {
        if (minutes < 60) return `${minutes} min`;
        const hrs = Math.floor(minutes / 60);
        const mins = minutes % 60;
        return mins > 0 ? `${hrs}h ${mins}min` : `${hrs}h`;
    }

    function difficultyBadge(dificultad) {
        const classes = {
            'Fácil': 'badge-facil',
            'Media': 'badge-media',
            'Difícil': 'badge-dificil'
        };
        const cls = classes[dificultad] || 'badge-media';
        return `<span class="badge ${cls}">${dificultad}</span>`;
    }

    function starsHTML(puntuacion, interactive = false) {
        let html = '';
        for (let i = 1; i <= 5; i++) {
            if (interactive) {
                html += `<button type="button" class="star ${i <= puntuacion ? 'active' : ''}"
                          data-rating="${i}">star</button>`;
            } else {
                html += `<span class="material-icons-round ${i <= puntuacion ? 'filled' : ''}">
                          ${i <= puntuacion ? 'star' : 'star_border'}</span>`;
            }
        }
        return html;
    }

    function confirm(message) {
        return window.confirm(message);
    }


    // ---- INTERFAZ PÚBLICA ----
    return {
        showView,
        switchTab,
        openModal,
        closeModal,
        closeAllModals,
        toast,
        showNavbar,
        hideNavbar,
        hideSplash,
        show,
        hide,
        formatDate,
        formatTime,
        difficultyBadge,
        starsHTML,
        confirm
    };

})();
