document.querySelectorAll('.settings-tabs .tab').forEach(tab => {
    tab.addEventListener('click', function (e) {
        e.preventDefault();

        // Quitar clase "active" de todas las pestañas y contenidos
        document.querySelectorAll('.settings-tabs .tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.settings-content .content').forEach(c => c.classList.remove('active'));

        // Agregar clase "active" al tab clickeado y mostrar su contenido
        this.classList.add('active');
        const target = document.querySelector(this.getAttribute('href'));
        if (target) target.classList.add('active');
    });
});
