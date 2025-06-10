// Selección de elementos del DOM
const btnCart = document.querySelector('.carrito');
const containerCartProducts = document.querySelector('.container-cart-products');
const rowProduct = document.querySelector('.row-product');
let allProducts = JSON.parse(localStorage.getItem('cart')) || [];
const valorTotal = document.querySelector('.total-pagar');
const countProducts = document.querySelector('#contador-productos');
const emptyCartMessage = '<p class="empty-cart-message">Tu carrito está vacío</p>';

// Configuración inicial de colores
const colores = {
    masa: {
        'vainilla': '#efd091',
        'chocolate': '#8B4513',
        'red-velvet': '#952d30'
    },
    cobertura: {
        'chocolate-blanco': '#f0e0c0',
        'chocolate-oscuro': '#5C4033',
        'arequipe': '#D4A76A'
    },
    toppings: {
        chispas: "url('/static/image/pepitasPatron.png')",
        oreo: "url('/static/image/oreoPatron.png')",
        mym: "url('/static/image/mymPatron.png')",
        chips: "url('/static/image/chipsPatron.png')",
        ninguno: 'none'
    }
};

// Mapeo de nombres para mostrar
const nombresParaMostrar = {
    masa: {
        'vainilla': 'Vainilla',
        'chocolate': 'Chocolate',
        'red-velvet': 'Red Velvet'
    },
    cobertura: {
        'chocolate-blanco': 'Chocolate Blanco',
        'chocolate-oscuro': 'Chocolate Oscuro',
        'arequipe': 'Arequipe'
    },
    topping: {
        'chispas': 'Chispas',
        'oreo': 'Oreo',
        'mym': 'M&M\'s',
        'chips': 'Chips'
    }
};

// Función para inicializar modales de manera genérica
function initModal(modalId, openButtonId, closeButtonClass, addToCartBtnId = null, size = null) {
    const modal = document.getElementById(modalId);
    const openButton = openButtonId ? document.getElementById(openButtonId) : null;
    const closeButton = closeButtonClass ? document.querySelector(`.${closeButtonClass}`) : null;
    const addToCartBtn = addToCartBtnId ? document.getElementById(addToCartBtnId) : null;

    if (!modal) return;

    // Configurar apertura del modal
    if (openButton) {
        openButton.addEventListener('click', (e) => {
            e.preventDefault();
            modal.classList.remove('hidden');
        });
    }

    // Configurar cierre del modal
    if (closeButton) {
        closeButton.addEventListener('click', () => {
            modal.classList.add('hidden');
        });
    }

    // Configurar botón de agregar al carrito si existe
    if (addToCartBtn && size) {
        addToCartBtn.addEventListener('click', () => {
            agregarProductoAlCarrito(size);
            modal.classList.add('hidden');
        });
    }

    // Cerrar al hacer clic fuera del modal
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
        }
    });

      // Configurar selección de sabores para modales de combos
    if (size && ['S', 'M', 'L', 'XL'].includes(size)) {
        // Inicializar la vista previa con valores por defecto
        setTimeout(() => {
            configurarSeleccionSabores(modal, size);
            actualizarVistaPrevia(size); // Actualizar vista previa al abrir el modal
        }, 100);}
}

function obtenerSeleccionesActuales(talla) {
    const modal = document.getElementById(`modal${talla}`);
    if (!modal) {
        console.error('Modal no encontrado para talla:', talla);
        return null;
    }
    
    // Buscar las opciones activas de manera más robusta
    const opcionesSeleccion = modal.querySelectorAll('.opcion-seleccion');
    let masaActive, coberturaActive, toppingActive;

    opcionesSeleccion.forEach(opcion => {
        const titulo = opcion.querySelector('h4')?.textContent.toLowerCase();
        if (titulo.includes('masa')) {
            masaActive = opcion.querySelector('.sabor-option.active');
        } else if (titulo.includes('cobertura')) {
            coberturaActive = opcion.querySelector('.sabor-option.active');
        } else if (titulo.includes('toppings')) {
            toppingActive = opcion.querySelector('.sabor-option.active');
        }
    });

    if (!masaActive || !coberturaActive || !toppingActive) {
        console.error('No se encontraron todas las selecciones:', {masaActive, coberturaActive, toppingActive});
        return null;
    }

    return {
        masa: {
            valor: masaActive.dataset.value,
            nombre: nombresParaMostrar.masa[masaActive.dataset.value]
        },
        cobertura: {
            valor: coberturaActive.dataset.value,
            nombre: nombresParaMostrar.cobertura[coberturaActive.dataset.value]
        },
        topping: {
            valor: toppingActive.dataset.value,
            nombre: nombresParaMostrar.topping[toppingActive.dataset.value]
        }
    };
}

function configurarSeleccionSabores(modal, size) {
    // Configurar eventos para los botones de selección de sabores
    const saborOptions = modal.querySelectorAll('.sabor-option');
    
    saborOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Encontrar el contenedor padre de opciones
            const optionsContainer = this.closest('.sabor-options');
            
            // Remover clase active de todos los hermanos
            optionsContainer.querySelectorAll('.sabor-option').forEach(el => {
                el.classList.remove('active');
            });
            
            // Agregar clase active al seleccionado
            this.classList.add('active');
            
            // Actualizar vista previa
            actualizarVistaPrevia(size);
        });
    });

    // Actualizar vista previa con valores iniciales
    actualizarVistaPrevia(size);
}

function actualizarVistaPrevia(size) {
    const selecciones = obtenerSeleccionesActuales(size);
    if (!selecciones) return;

    // Actualizar masa
    const masaElement = document.getElementById(`dona-masa-${size}`);
    if (masaElement) {
        const colorMasa = colores.masa[selecciones.masa.valor];
        masaElement.style.backgroundColor = colorMasa;
        console.log(`Actualizando masa ${size} a color:`, colorMasa);
    }

    // Actualizar cobertura
    const coberturaElement = document.getElementById(`dona-cobertura-${size}`);
    if (coberturaElement) {
        const colorCobertura = colores.cobertura[selecciones.cobertura.valor];
        coberturaElement.style.backgroundColor = colorCobertura;
        console.log(`Actualizando cobertura ${size} a color:`, colorCobertura);
    }

     // Actualizar topping - PARTE CORREGIDA
    const toppingElement = document.getElementById(`dona-topping-${size}`);
    if (toppingElement) {
        const toppingValue = selecciones.topping.valor;
        
        // Resetear estilos primero
        toppingElement.style.backgroundImage = 'none';
        toppingElement.style.backgroundColor = 'transparent';
        
        if (toppingValue !== 'ninguno') {
            // Verificar si la imagen existe en el objeto colores
            if (colores.toppings[toppingValue]) {
                toppingElement.style.backgroundImage = colores.toppings[toppingValue];
                toppingElement.style.backgroundSize = 'cover';
                toppingElement.style.backgroundRepeat = 'no-repeat';
                toppingElement.style.backgroundPosition = 'center';
            } else {
                console.error(`No se encontró imagen para topping: ${toppingValue}`);
            }
        }
        console.log(`Topping actualizado (${size}):`, toppingValue, colores.toppings[toppingValue]);
    }
}



function agregarAlCarrito(producto) {
    if (!producto || !producto.id) {
        console.error('Producto inválido:', producto);
        return;
    }

    // Verificar si el producto ya está en el carrito
    const index = allProducts.findIndex(p => 
        p.tipo === producto.tipo &&
        p.talla === producto.talla &&
        p.masa.valor === producto.masa.valor &&
        p.cobertura.valor === producto.cobertura.valor &&
        p.topping.valor === producto.topping.valor
    );

    if (index !== -1) {
        // Producto existe, incrementar cantidad
        allProducts[index].quantity += 1;
        console.log('Incrementando cantidad del producto existente:', allProducts[index]);
    } else {
        // Producto nuevo, agregar al carrito
        allProducts.push(producto);
        console.log('Nuevo producto agregado:', producto);
    }

    // Actualizar localStorage
    localStorage.setItem('cart', JSON.stringify(allProducts));
    
    // Actualizar la vista
    showHTML();
    
    // Mostrar notificación con detalles
    alert(`¡Agregado al carrito!\n${producto.titulo}\n${producto.descripcion}`);
}

function showHTML() {
    if (!rowProduct) return;

    rowProduct.innerHTML = '';

    if (allProducts.length === 0) {
        rowProduct.innerHTML = emptyCartMessage;
        if (valorTotal) valorTotal.innerText = '$0.00';
        if (countProducts) countProducts.innerText = '0';
    } else {
        let total = 0;
        let totalOfProducts = 0;

        allProducts.forEach(product => {
            const containerProduct = document.createElement('div');
            containerProduct.classList.add('cart-product');

            containerProduct.innerHTML = `
                <div class="info-cart-product">
                    <span class="cantidad-producto-carrito">${product.quantity}</span>
                    <p class="titulo-producto-carrito">${product.titulo}</p>
                    <span class="precio-producto-carrito">$${(product.precio * product.quantity).toFixed(2)}</span>
                </div>
                <div class="detalles-producto-carrito">
                    <p>${product.descripcion}</p>
                </div>
                <div class="acciones-producto-carrito">
                    <button class="btn-eliminar" data-id="${product.id}">Eliminar</button>
                </div>`;

            rowProduct.append(containerProduct);
            total += product.quantity * product.precio;
            totalOfProducts += product.quantity;
        });

        if (valorTotal) valorTotal.innerText = `$${total.toFixed(2)}`;
        if (countProducts) countProducts.innerText = totalOfProducts;
    }
}

// Evento para eliminar productos del carrito
if (rowProduct) {
    rowProduct.addEventListener('click', e => {
        if (e.target.classList.contains('btn-eliminar') || e.target.classList.contains('icon-close')) {
            const productId = e.target.getAttribute('data-id');
            allProducts = allProducts.filter(product => product.id !== productId);
            showHTML();
        }
    });
}

// Evento para mostrar/ocultar el carrito
if (btnCart && containerCartProducts) {
    btnCart.addEventListener('click', (e) => {
        e.stopPropagation();
        containerCartProducts.classList.toggle('visible');
    });

    // Cerrar el carrito al hacer clic fuera
    document.addEventListener('click', (event) => {
        if (!containerCartProducts.contains(event.target)) {
            containerCartProducts.classList.remove('visible');
        }
    });

    // Prevenir que el clic dentro del carrito lo cierre
    containerCartProducts.addEventListener('click', (e) => {
        e.stopPropagation();
    });
}

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
    // Modales de combos
    initModal('modalS', 'btnAgregar', 'closeS', 'btnCerrarModalS', 'S');
    initModal('modalM', 'btnAgregarM', 'closeM', 'btnCerrarModalM', 'M');
    initModal('modalL', 'btnAgregarL', 'closeL', 'btnCerrarModalL', 'L');
    initModal('modalXL', 'btnAgregarXL', 'closeXL', 'btnCerrarModalXL', 'XL');
    
    // Modales de información
    initModal('modalV', 'btnInfoV', 'closeV');
    initModal('modalC', 'btnInfoC', 'closeC');
    initModal('modalR', 'btnInfoR', 'closeR');
    initModal('modalB', 'btnInfoB', 'closeB');
    initModal('modalOS', 'btnInfoOS', 'closeOS');
    initModal('modalA', 'btnInfoA', 'closeA');
    initModal('modalT1', 'btnInfoT1', 'closeT1');
    initModal('modalT2', 'btnInfoT2', 'closeT2');
    initModal('modalT3', 'btnInfoT3', 'closeT3');
    initModal('modalT4', 'btnInfoT4', 'closeT4');
    initModal('modalP', 'btnPagar', 'closeP');

    // Configurar eventos para los botones de agregar al carrito
    document.getElementById('btnCerrarModalS')?.addEventListener('click', function() {
        const selecciones = obtenerSeleccionesActuales('S');
        if (!selecciones) {
            alert('Por favor selecciona masa, cobertura y topping antes de agregar al carrito');
            return;
        }

        const producto = {
            id: `S-${selecciones.masa.valor}-${selecciones.cobertura.valor}-${selecciones.topping.valor}`,
            tipo: 'combo-dona',
            talla: 'S',
            masa: selecciones.masa,
            cobertura: selecciones.cobertura,
            topping: selecciones.topping,
            precio: 10000,
            titulo: 'Donas Talla S',
            descripcion: `${selecciones.masa.nombre} | ${selecciones.cobertura.nombre} | ${selecciones.topping.nombre}`,
            quantity: 1,
            timestamp: Date.now()
        };

        agregarAlCarrito(producto);


        
// Evento para agregar Donas Talla M
document.getElementById('btnCerrarModalM')?.addEventListener('click', function() {
    const selecciones = obtenerSeleccionesActuales('M');
    if (!selecciones) {
        alert('Por favor selecciona masa, cobertura y topping antes de agregar al carrito');
        return;
    }

    const producto = {
        id: `M-${selecciones.masa.valor}-${selecciones.cobertura.valor}-${selecciones.topping.valor}`,
        tipo: 'combo-dona',
        talla: 'M',
        masa: selecciones.masa,
        cobertura: selecciones.cobertura,
        topping: selecciones.topping,
        precio: 18000,
        titulo: 'Donas Talla M',
        descripcion: `${selecciones.masa.nombre} | ${selecciones.cobertura.nombre} | ${selecciones.topping.nombre}`,
        quantity: 1,
        timestamp: Date.now()
    };

    agregarAlCarrito(producto);
});

// Evento para agregar Donas Talla L
document.getElementById('btnCerrarModalL')?.addEventListener('click', function() {
    const selecciones = obtenerSeleccionesActuales('L');
    if (!selecciones) {
        alert('Por favor selecciona masa, cobertura y topping antes de agregar al carrito');
        return;
    }

    const producto = {
        id: `L-${selecciones.masa.valor}-${selecciones.cobertura.valor}-${selecciones.topping.valor}`,
        tipo: 'combo-dona',
        talla: 'L',
        masa: selecciones.masa,
        cobertura: selecciones.cobertura,
        topping: selecciones.topping,
        precio: 25000,
        titulo: 'Donas Talla L',
        descripcion: `${selecciones.masa.nombre} | ${selecciones.cobertura.nombre} | ${selecciones.topping.nombre}`,
        quantity: 1,
        timestamp: Date.now()
    };

    agregarAlCarrito(producto);
});

// Evento para agregar Donas Talla XL
document.getElementById('btnCerrarModalXL')?.addEventListener('click', function() {
    const selecciones = obtenerSeleccionesActuales('XL');
    if (!selecciones) {
        alert('Por favor selecciona masa, cobertura y topping antes de agregar al carrito');
        return;
    }

    const producto = {
        id: `XL-${selecciones.masa.valor}-${selecciones.cobertura.valor}-${selecciones.topping.valor}`,
        tipo: 'combo-dona',
        talla: 'XL',
        masa: selecciones.masa,
        cobertura: selecciones.cobertura,
        topping: selecciones.topping,
        precio: 32000,
        titulo: 'Donas Talla XL',
        descripcion: `${selecciones.masa.nombre} | ${selecciones.cobertura.nombre} | ${selecciones.topping.nombre}`,
        quantity: 1,
        timestamp: Date.now()
    };

    agregarAlCarrito(producto);
});
    });

    // Mostrar estado inicial del carrito
    showHTML();
});

// Funciones para los modales de métodos de pago
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = "block";
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = "none";
}

// Cerrar modales al hacer clic fuera
window.addEventListener('click', function(event) {
    const modals = document.querySelectorAll(".modal-nequi, .modal-davi");
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});


// ...existing code...

document.getElementById('btnAgregarProducto')?.addEventListener('click', function(e) {
    e.preventDefault();

    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    if (cart.length === 0) {
        alert('El carrito está vacío');
        return;
    }

    // Puedes pedir dirección y observaciones aquí si lo deseas
    const direccion = prompt('¿A qué dirección deseas el envío?');
    if (!direccion) return;

    fetch('/procesar_compra/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ carrito: cart, direccion: direccion })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            localStorage.removeItem('cart');
            showHTML();

            // Llenar la factura en el modal
            const venta = data.venta;
            let facturaHTML = `
                <h3>Factura de Compra</h3>
                <p><b>Fecha:</b> ${venta.fecha}</p>
                <p><b>Dirección:</b> ${venta.direccion}</p>
                <table style="width:100%;margin-bottom:10px;">
                    <thead>
                        <tr>
                            <th style="text-align:left;">Producto</th>
                            <th>Cant.</th>
                            <th>Unitario</th>
                            <th>Subtotal</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${venta.detalles.map(det => `
                            <tr>
                                <td>${det.producto}</td>
                                <td style="text-align:center;">${det.cantidad}</td>
                                <td style="text-align:right;">$${det.precio_unitario}</td>
                                <td style="text-align:right;">$${det.subtotal}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
                <p><b>Subtotal:</b> $${venta.subtotal}</p>
                <p><b>IVA (19%):</b> $${venta.iva}</p>
                <p><b>Total:</b> $${venta.total}</p>
            `;
            document.querySelector('.cajita').innerHTML = facturaHTML;

            // Mostrar el modal de compra exitosa
            document.getElementById('modalCompraExitosa').style.display = 'flex';
        } else {
            alert('Error al procesar la compra: ' + (data.error || ''));
        }
    })
    .catch(error => {
        alert('Ocurrió un error al procesar la compra');
        console.error(error);
    });
});

// Función para obtener el CSRF token de la cookie
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

// ...existing code...

// Cerrar el modal de compra exitosa
document.getElementById('cerrarModalCompra')?.addEventListener('click', function() {
    document.getElementById('modalCompraExitosa').style.display = 'none';
});