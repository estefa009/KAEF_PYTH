document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    
    menuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('active');
    });
    
    // Cerrar menú al hacer clic fuera
    document.addEventListener('click', function(event) {
        if (!sidebar.contains(event.target) && event.target !== menuToggle) {
            sidebar.classList.remove('active');
        }
    });
});