
    document.addEventListener('DOMContentLoaded', function() {
        const menuToggle = document.getElementById('menuToggle');
        const sidebar = document.getElementById('sidebar');

        if (menuToggle && sidebar) {
            menuToggle.addEventListener('click', function() {
                sidebar.classList.toggle('active');
                this.classList.toggle('open');
                const icon = this.querySelector('i');
                if (icon) {
                    icon.classList.toggle('bi-list');
                    icon.classList.toggle('bi-x');
                }
            });
        } else {
            console.error("No se encontraron el botón de menú o el menú lateral.");
        }
    });
