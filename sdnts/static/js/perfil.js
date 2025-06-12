document.addEventListener('DOMContentLoaded', function() {
    // Manejar las pestañas
    const tabs = document.querySelectorAll('.settings-tabs .tab');
    const contents = document.querySelectorAll('.settings-content .content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remover active de todas las pestañas
            tabs.forEach(t => t.classList.remove('active'));
            
            // Remover active de todos los contenidos
            contents.forEach(c => c.classList.remove('active'));
            
            // Activar la pestaña clickeada
            this.classList.add('active');
            
            // Activar el contenido correspondiente
            const targetId = this.getAttribute('href').substring(1);
            document.getElementById(targetId).classList.add('active');
        });
    });

    // Funciones del carrito
    window.actualizarCantidad = function(itemId, cantidad) {
        fetch('/actualizar-carrito/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                item_id: itemId,
                cantidad: cantidad
            })
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    };

    window.eliminarDelCarrito = function(itemId) {
        if(confirm('¿Estás seguro de eliminar este producto?')) {
            fetch(`/eliminar-del-carrito/${itemId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    location.reload();
                }
            })
            .catch(error => console.error('Error:', error));
        }
    };

    window.verDetalleVenta = function(ventaId) {
        const detalleRow = document.querySelector(`.detalle-venta-${ventaId}`);
        if (detalleRow) {
            if (detalleRow.style.display === 'none') {
                detalleRow.style.display = 'table-row';
            } else {
                detalleRow.style.display = 'none';
            }
        }
    }
});
