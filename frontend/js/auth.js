/* ==========================================
   SMARTRECIPE AI - MODULO DE AUTENTICACIÓN
   ========================================== */

const Auth = (() => {

    let currentUser = null;

    function getCurrentUser() {
        return currentUser;
    }

    // ---- INICIALIZAR ----
    function init() {
        const formLogin = document.getElementById('form-login');
        const formRegistro = document.getElementById('form-registro');
        const showRegistro = document.getElementById('show-registro');
        const showLogin = document.getElementById('show-login');
        const btnLogout = document.getElementById('btn-logout');

        // Toggle entre formularios
        showRegistro.addEventListener('click', (e) => {
            e.preventDefault();
            UI.hide('form-login');
            UI.show('form-registro');
            UI.hide('login-error');
        });

        showLogin.addEventListener('click', (e) => {
            e.preventDefault();
            UI.show('form-login');
            UI.hide('form-registro');
            UI.hide('registro-error');
        });

        // Enviar login
        formLogin.addEventListener('submit', async (e) => {
            e.preventDefault();
            await handleLogin();
        });

        // Enviar registro
        formRegistro.addEventListener('submit', async (e) => {
            e.preventDefault();
            await handleRegistro();
        });

        // Logout
        btnLogout.addEventListener('click', () => {
            handleLogout();
        });
    }

    // ---- LOGIN ----
    async function handleLogin() {
        const correo = document.getElementById('login-correo').value.trim();
        const password = document.getElementById('login-password').value;
        const errorEl = document.getElementById('login-error');

        UI.hide(errorEl);

        try {
            await API.login(correo, password);

            // Obtener perfil
            currentUser = await API.perfil();

            // Ir al dashboard
            showDashboard();

            UI.toast(`¡Bienvenido, ${currentUser.nombre}!`, 'success');

            // Limpiar formulario
            document.getElementById('form-login').reset();

        } catch (err) {
            errorEl.textContent = err.message;
            UI.show(errorEl);
        }
    }

    // ---- REGISTRO ----
    async function handleRegistro() {
        const nombre = document.getElementById('reg-nombre').value.trim();
        const correo = document.getElementById('reg-correo').value.trim();
        const password = document.getElementById('reg-password').value;
        const errorEl = document.getElementById('registro-error');

        UI.hide(errorEl);

        try {
            await API.registro(nombre, correo, password);

            UI.toast('¡Cuenta creada! Ahora inicia sesión', 'success');

            // Volver al login
            UI.show('form-login');
            UI.hide('form-registro');

            // Pre-llenar correo
            document.getElementById('login-correo').value = correo;
            document.getElementById('login-password').focus();

            // Limpiar formulario de registro
            document.getElementById('form-registro').reset();

        } catch (err) {
            errorEl.textContent = err.message;
            UI.show(errorEl);
        }
    }

    // ---- LOGOUT ----
    function handleLogout() {
        API.logout();
        currentUser = null;

        UI.hideNavbar();
        UI.showView('view-auth');

        UI.toast('Sesión cerrada', 'info');
    }

    // ---- MOSTRAR DASHBOARD ----
    function showDashboard() {
        UI.showNavbar(currentUser.nombre);
        UI.showView('view-dashboard');
        UI.switchTab('ingredientes');

        // Cargar datos iniciales
        Ingredientes.cargar();
    }

    // ---- VERIFICAR SESIÓN AL INICIO ----
    async function checkSession() {
        if (!API.isLoggedIn()) return false;

        try {
            currentUser = await API.perfil();
            showDashboard();
            return true;
        } catch (err) {
            // Token inválido o expirado
            API.removeToken();
            return false;
        }
    }


    // ---- INTERFAZ PÚBLICA ----
    return {
        init,
        checkSession,
        getCurrentUser,
        handleLogout
    };

})();
