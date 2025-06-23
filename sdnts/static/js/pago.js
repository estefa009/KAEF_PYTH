// JavaScript para la página de pago
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM completamente cargado - Iniciando configuración de pago');
    
    // Verificar que todos los elementos críticos estén presentes
    const elementosRequeridos = [
        'fecha_entrega',
        'resumen-productos', 
        'btn-finalizar-compra',
        'confirmar-compra',
        'modalConfirmacion',
        'modalCompraExitosa'
    ];
    
    elementosRequeridos.forEach(id => {
        const elemento = document.getElementById(id);
        if (!elemento) {
            console.error(`Elemento no encontrado: ${id}`);
        } else {
            console.log(`Elemento encontrado: ${id}`);
        }
    });
    
    // Configurar fecha mínima (hoy + 3 días)
    const fechaInput = document.getElementById('fecha_entrega');
    const hoy = new Date();
    const fechaMinima = new Date(hoy.getFullYear(), hoy.getMonth(), hoy.getDate() + 3);
    const fechaMinimaStr = fechaMinima.toISOString().split('T')[0];
    fechaInput.setAttribute('min', fechaMinimaStr);

    // Cargar resumen del carrito
    cargarResumenCarrito();

    // Configurar cambio de método de pago
    configurarMetodosPago();

    // Configurar botón de finalizar compra
    configurarFinalizarCompra();

    // Configurar modal de compra exitosa
    configurarModalCompraExitosa();

    // Debug adicional: agregar listeners de prueba para todos los botones
    document.querySelectorAll('button, .btn, .nav-link-custom').forEach(elemento => {
        elemento.addEventListener('click', function(e) {
            console.log('Click detectado en:', this.className, this.id, this.textContent.trim());
        });
    });
    
    // Verificar que jQuery esté disponible
    if (typeof $ !== 'undefined') {
        console.log('jQuery disponible, versión:', $.fn.jquery);
    } else {
        console.error('jQuery no está disponible');
    }
});

function cargarResumenCarrito() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const resumenContainer = document.getElementById('resumen-productos');
    
    if (cart.length === 0) {
        resumenContainer.innerHTML = `
            <div class="empty-cart-message">
                <i class="fas fa-shopping-cart empty-cart-icon"></i>
                <h5>Tu carrito está vacío</h5>
                <p>Agrega algunos productos deliciosos a tu carrito</p>
                <a href="/catalogocliente/" class="btn btn-primary">Ver Catálogo</a>
            </div>
        `;
        document.getElementById('subtotal-display').textContent = '$0.00';
        document.getElementById('iva-display').textContent = '$0.00';
        document.getElementById('total-display').textContent = '$0.00';
        return;
    }

    let subtotal = 0;
    let productosHTML = '';

    cart.forEach(item => {
        const itemSubtotal = item.precio * item.quantity;
        subtotal += itemSubtotal;

        productosHTML += `
            <div class="producto-item">
                <div class="producto-info">
                    <div class="producto-titulo">${item.titulo}</div>
                    <div class="producto-descripcion">${item.descripcion || ''}</div>
                    <div class="producto-cantidad">Cantidad: ${item.quantity}</div>
                </div>
                <div class="producto-precio">$${itemSubtotal.toFixed(2)}</div>
            </div>
        `;
    });

    resumenContainer.innerHTML = productosHTML;

    // Calcular totales
    const iva = subtotal * 0.19;
    const total = subtotal + iva;

    document.getElementById('subtotal-display').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('iva-display').textContent = `$${iva.toFixed(2)}`;
    document.getElementById('total-display').textContent = `$${total.toFixed(2)}`;
}

function configurarMetodosPago() {
    const radioNequi = document.getElementById('nequi');
    const radioDaviplata = document.getElementById('daviplata');
    const detallesNequi = document.getElementById('detalles-nequi');
    const detallesDaviplata = document.getElementById('detalles-daviplata');

    if (!radioNequi || !radioDaviplata || !detallesNequi || !detallesDaviplata) {
        console.error('No se encontraron todos los elementos de métodos de pago');
        return;
    }

    console.log('Configurando métodos de pago...');

    radioNequi.addEventListener('change', function() {
        console.log('Nequi seleccionado');
        if (this.checked) {
            detallesNequi.style.display = 'block';
            detallesDaviplata.style.display = 'none';
        }
    });

    radioDaviplata.addEventListener('change', function() {
        console.log('DaviPlata seleccionado');
        if (this.checked) {
            detallesNequi.style.display = 'none';
            detallesDaviplata.style.display = 'block';
        }
    });
}

function configurarFinalizarCompra() {
    const btnFinalizar = document.getElementById('btn-finalizar-compra');
    const btnConfirmar = document.getElementById('confirmar-compra');

    if (!btnFinalizar || !btnConfirmar) {
        console.error('No se encontraron los botones de finalizar compra');
        return;
    }

    btnFinalizar.addEventListener('click', function() {
        console.log('Botón finalizar clickeado');
        if (validarFormulario()) {
            $('#modalConfirmacion').modal('show');
        }
    });

    btnConfirmar.addEventListener('click', function() {
        console.log('Confirmar compra clickeado');
        $('#modalConfirmacion').modal('hide');
        procesarCompra();
    });
}

function validarFormulario() {
    let isValid = true;
    const campos = ['direccion', 'fecha_entrega'];
    
    // Validar campos básicos
    campos.forEach(campoId => {
        const campo = document.getElementById(campoId);
        const valor = campo.value.trim();
        
        if (!valor) {
            mostrarError(campo, 'Este campo es obligatorio');
            isValid = false;
        } else {
            limpiarError(campo);
        }
    });

    // Validar fecha mínima
    const fechaInput = document.getElementById('fecha_entrega');
    const fechaSeleccionada = new Date(fechaInput.value);
    const fechaMinima = new Date(fechaInput.getAttribute('min'));
    
    if (fechaSeleccionada < fechaMinima) {
        mostrarError(fechaInput, 'La fecha debe ser al menos 3 días a partir de hoy');
        isValid = false;
    }

    // Validar método de pago y referencia
    const metodoPago = document.querySelector('input[name="metodo_pago"]:checked').value;
    let referenciaInput;
    
    if (metodoPago === 'NEQUI') {
        referenciaInput = document.getElementById('referencia_nequi');
    } else {
        referenciaInput = document.getElementById('referencia_daviplata');
    }

    const referencia = referenciaInput.value.trim();
    if (!referencia || referencia.length < 4) {
        mostrarError(referenciaInput, 'Ingresa un número de referencia válido (mínimo 4 dígitos)');
        isValid = false;
    } else {
        limpiarError(referenciaInput);
    }

    // Validar que hay productos en el carrito
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    if (cart.length === 0) {
        alert('Tu carrito está vacío. Agrega productos antes de continuar.');
        isValid = false;
    }

    return isValid;
}

function mostrarError(campo, mensaje) {
    campo.classList.add('is-invalid');
    
    // Remover mensaje de error anterior si existe
    const errorAnterior = campo.parentNode.querySelector('.invalid-feedback');
    if (errorAnterior) {
        errorAnterior.remove();
    }

    // Crear nuevo mensaje de error
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = mensaje;
    campo.parentNode.appendChild(errorDiv);
}

function limpiarError(campo) {
    campo.classList.remove('is-invalid');
    const errorDiv = campo.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function procesarCompra() {
    // Mostrar overlay de carga
    document.getElementById('loading-overlay').style.display = 'flex';

    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const metodoPago = document.querySelector('input[name="metodo_pago"]:checked').value;
    
    let referencia;
    if (metodoPago === 'NEQUI') {
        referencia = document.getElementById('referencia_nequi').value.trim();
    } else {
        referencia = document.getElementById('referencia_daviplata').value.trim();
    }

    const payload = {
        carrito: cart,
        direccion: document.getElementById('direccion').value.trim(),
        fecha_entrega: document.getElementById('fecha_entrega').value,
        metodo_pago: metodoPago,
        transaccion_id: referencia
    };

    console.log('Enviando datos de compra:', payload);

    fetch('/procesar_compra/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(payload)
    })
    .then(async response => {
        console.log('Respuesta del servidor:', response);
        
        if (!response.ok) {
            const text = await response.text();
            throw new Error(`HTTP ${response.status}: ${text}`);
        }
        
        try {
            return await response.json();
        } catch (e) {
            throw new Error('Respuesta no válida del servidor');
        }
    })
    .then(data => {
        console.log('Datos de respuesta:', data);
        document.getElementById('loading-overlay').style.display = 'none';
          if (data.success) {
            // Limpiar carrito
            localStorage.removeItem('cart');
            
            // Mostrar modal de éxito
            $('#modalCompraExitosa').modal('show');
        } else {
            throw new Error(data.error || 'Error desconocido al procesar la compra');
        }
    })
    .catch(error => {
        console.error('Error al procesar compra:', error);
        document.getElementById('loading-overlay').style.display = 'none';
        
        alert('Error al procesar la compra: ' + error.message);
    });
}

function configurarModalCompraExitosa() {
    const btnVolverInicio = document.getElementById('btn-volver-inicio');
    
    btnVolverInicio.addEventListener('click', function() {
        // Redirigir al inicio después de un breve delay para la animación
        setTimeout(() => {
            window.location.href = '/vistacliente/';
        }, 300);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Funciones de utilidad adicionales
function formatearPrecio(precio) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 2
    }).format(precio);
}

function animarElemento(elemento, animacion = 'fadeIn') {
    elemento.style.opacity = '0';
    elemento.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        elemento.style.transition = 'all 0.5s ease';
        elemento.style.opacity = '1';
        elemento.style.transform = 'translateY(0)';
    }, 100);
}

// Event listeners adicionales para mejorar UX
document.addEventListener('DOMContentLoaded', function() {
    // Animación de entrada para las tarjetas
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            animarElemento(card);
        }, index * 150);
    });

    // Auto-focus en primer campo vacío
    const primerCampoVacio = document.querySelector('input:not([type="radio"]):not([type="checkbox"]):first-of-type');
    if (primerCampoVacio) {
        setTimeout(() => {
            primerCampoVacio.focus();
        }, 500);
    }

    // Validación en tiempo real
    const campos = ['direccion', 'fecha_entrega', 'referencia_nequi', 'referencia_daviplata'];
    campos.forEach(campoId => {
        const campo = document.getElementById(campoId);
        if (campo) {
            campo.addEventListener('blur', function() {
                if (this.value.trim()) {
                    limpiarError(this);
                }
            });
        }
    });
});
