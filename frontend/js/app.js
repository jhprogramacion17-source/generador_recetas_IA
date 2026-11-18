/* ==========================================
   SMARTRECIPE AI - INICIALIZACIÓN
   ========================================== */

document.addEventListener('DOMContentLoaded', async () => {

    // Inicializar módulos
    Auth.init();
    Ingredientes.init();
    Recetas.init();

    // Configurar tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.dataset.tab;
            UI.switchTab(tabName);

            // Cargar datos según el tab seleccionado
            switch (tabName) {
                case 'ingredientes':
                    Ingredientes.cargar();
                    break;
                case 'generar':
                    Recetas.cargarPreview();
                    break;
                case 'historial':
                    Recetas.cargarHistorial();
                    break;
                case 'favoritas':
                    Recetas.cargarFavoritas();
                    break;
            }
        });
    });

    // Cerrar modales con Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            UI.closeAllModals();
        }
    });

    // Verificar sesión existente
    const hasSession = await Auth.checkSession();

    if (!hasSession) {
        UI.showView('view-auth');
    }

    // Ocultar splash
    setTimeout(() => {
        UI.hideSplash();
    }, 800);
});
