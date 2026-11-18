/* ==========================================
   SMARTRECIPE AI - CAPA DE API
   ========================================== */

const API = (() => {

    const BASE_URL = window.location.origin;

    // ---- TOKEN ----
    function getToken() {
        return localStorage.getItem('smartrecipe_token');
    }

    function setToken(token) {
        localStorage.setItem('smartrecipe_token', token);
    }

    function removeToken() {
        localStorage.removeItem('smartrecipe_token');
    }

    function isLoggedIn() {
        return !!getToken();
    }

    // ---- HEADERS ----
    function authHeaders() {
        return {
            'Authorization': `Bearer ${getToken()}`,
            'Content-Type': 'application/json'
        };
    }

    // ---- FETCH HELPER ----
    async function request(method, path, body = null, auth = true) {
        const options = {
            method: method,
            headers: auth ? authHeaders() : { 'Content-Type': 'application/json' }
        };

        if (body !== null) {
            options.body = JSON.stringify(body);
        }

        const response = await fetch(`${BASE_URL}${path}`, options);

        // 204 No Content
        if (response.status === 204) {
            return null;
        }

        // Si no es OK, lanzar error con detalle
        if (!response.ok) {
            let detail = 'Error desconocido';
            try {
                const data = await response.json();
                detail = data.detail || detail;
            } catch (e) {
                // sin JSON
            }

            const error = new Error(detail);
            error.status = response.status;
            throw error;
        }

        return await response.json();
    }


    // ==========================================
    // AUTENTICACIÓN
    // ==========================================

    async function registro(nombre, correo, password) {
        return request('POST', '/auth/registro', {
            nombre, correo, password
        }, false);
    }

    async function login(correo, password) {
        // El endpoint login usa OAuth2PasswordRequestForm
        // que espera form-data con username y password
        const formData = new URLSearchParams();
        formData.append('username', correo);
        formData.append('password', password);

        const response = await fetch(`${BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });

        if (!response.ok) {
            let detail = 'Correo o contraseña incorrectos';
            try {
                const data = await response.json();
                detail = data.detail || detail;
            } catch (e) { /* sin JSON */ }

            const error = new Error(detail);
            error.status = response.status;
            throw error;
        }

        const data = await response.json();
        setToken(data.access_token);
        return data;
    }

    async function perfil() {
        return request('GET', '/auth/perfil');
    }

    function logout() {
        removeToken();
    }


    // ==========================================
    // INGREDIENTES
    // ==========================================

    async function listarIngredientes() {
        return request('GET', '/ingredientes/');
    }

    async function obtenerIngrediente(id) {
        return request('GET', `/ingredientes/${id}`);
    }

    async function crearIngrediente(datos) {
        return request('POST', '/ingredientes/', datos);
    }

    async function actualizarIngrediente(id, datos) {
        return request('PUT', `/ingredientes/${id}`, datos);
    }

    async function eliminarIngrediente(id) {
        return request('DELETE', `/ingredientes/${id}`);
    }


    // ==========================================
    // RECETAS
    // ==========================================

    async function generarReceta() {
        return request('POST', '/recetas/generar');
    }

    async function listarRecetas() {
        return request('GET', '/recetas/');
    }

    async function listarFavoritas() {
        return request('GET', '/recetas/favoritas');
    }

    async function obtenerReceta(id) {
        return request('GET', `/recetas/${id}`);
    }

    async function toggleFavorita(id, favorita) {
        return request('PATCH', `/recetas/${id}/favorita`, {
            favorita
        });
    }

    async function eliminarReceta(id) {
        return request('DELETE', `/recetas/${id}`);
    }


    // ==========================================
    // CALIFICACIONES
    // ==========================================

    async function calificarReceta(recetaId, puntuacion) {
        return request('POST', `/recetas/${recetaId}/calificaciones`, {
            puntuacion
        });
    }

    async function actualizarCalificacion(recetaId, puntuacion) {
        return request('PUT', `/recetas/${recetaId}/calificaciones`, {
            puntuacion
        });
    }

    async function obtenerCalificacion(recetaId) {
        return request('GET', `/recetas/${recetaId}/calificacion`);
    }


    // ---- INTERFAZ PÚBLICA ----
    return {
        getToken,
        setToken,
        removeToken,
        isLoggedIn,

        registro,
        login,
        perfil,
        logout,

        listarIngredientes,
        obtenerIngrediente,
        crearIngrediente,
        actualizarIngrediente,
        eliminarIngrediente,

        generarReceta,
        listarRecetas,
        listarFavoritas,
        obtenerReceta,
        toggleFavorita,
        eliminarReceta,

        calificarReceta,
        actualizarCalificacion,
        obtenerCalificacion
    };

})();
