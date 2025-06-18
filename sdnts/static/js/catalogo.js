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
        'choc-blanco': '#f0e0c0',
        'choc-oscuro': '#5C4033',
        'arequipe': '#D4A76A'
    },
    toppings: {
        chispas: "url('/static/image/pepitasPatron.png')",
        oreo: "url('/static/image/oreoPatron.png')",
        mym: "url('/static/image/mmPatron.png')",
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
        'choc-blanco': 'Chocolate Blanco',
        'choc-oscuro': 'Chocolate Oscuro',
        'arequipe': 'Arequipe'
    },
    topping: {
        'chispas': 'Chispas',
        'oreo': 'Oreo',
        'mm': 'M&M',
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
        }, 100);
    }
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
        console.error('No se encontraron todas las selecciones:', { masaActive, coberturaActive, toppingActive });
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
        option.addEventListener('click', function () {
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
            // Si es mm (M&M), usa mmPatron.png
            let imgFile = toppingValue === 'mm' ? 'mmPatron.png' : `${toppingValue}Patron.png`;
            toppingElement.style.backgroundImage = `url('/static/image/${imgFile}')`;
            toppingElement.style.backgroundSize = '40px 40px'; // o el tamaño que prefieras
            toppingElement.style.backgroundRepeat = 'repeat';
            toppingElement.style.backgroundPosition = 'center';
        }
        console.log(`Topping actualizado (${size}):`, toppingValue);
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

    // Mostrar notificación con detalles usando modal personalizado
    mostrarModalAgregadoCarrito(producto);
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
                    <div class="info-cart-productx2">
                        <p class="titulo-producto-carrito">${product.titulo}</p>
                       <span class="precio-producto-carrito">$${(product.precio * product.quantity).toFixed(2)}</span>
                   </div>
                </div><div class="bottonesx2">
                  <div class="detalles-producto-carrito">
                    <i class="bi bi-trash-fill icon-trash" data-id="${product.id}" title="Eliminar"></i>
                </div>
                <div class="acciones-producto-carrito">
                    <span class="btn-decrementar icon-btn" data-id="${product.id}">-</span>
                    <span class="btn-incrementar icon-btn" data-id="${product.id}">+</span>
                </div>
                </div>
                `;

            // Animación y eliminación del producto
            const iconTrash = containerProduct.querySelector('.icon-trash');
            iconTrash.addEventListener('click', function () {
                containerProduct.style.height = containerProduct.offsetHeight + "px"; // Fija la altura antes de animar
                // Forzar reflow para que el cambio de clase sea animado
                void containerProduct.offsetWidth;
                containerProduct.classList.add('eliminando');
                setTimeout(() => {
                    const index = allProducts.findIndex(p => p.id == product.id);
                    if (index !== -1) {
                        allProducts.splice(index, 1);
                        localStorage.setItem('cart', JSON.stringify(allProducts));
                        showHTML();
                    }
                }, 500);
            });

            rowProduct.append(containerProduct);
            total += product.quantity * product.precio;
            totalOfProducts += product.quantity;
        });

        if (valorTotal) valorTotal.innerText = `$${total.toFixed(2)}`;
        if (countProducts) countProducts.innerText = totalOfProducts;
    }

    agregarListenersBotones();
}



function agregarListenersBotones() {
    document.querySelectorAll('.btn-incrementar').forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.dataset.id;
            const product = allProducts.find(p => p.id == productId);
            if (product) {
                product.quantity += 1;
                localStorage.setItem('cart', JSON.stringify(allProducts));
                showHTML();
            }
        });
    });

    document.querySelectorAll('.btn-decrementar').forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.dataset.id;
            const product = allProducts.find(p => p.id == productId);
            if (product) {
                if (product.quantity > 1) {
                    product.quantity -= 1;
                } else {
                    const index = allProducts.findIndex(p => p.id == productId);
                    allProducts.splice(index, 1);
                }
                localStorage.setItem('cart', JSON.stringify(allProducts));
                showHTML();
            }
        });
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
document.addEventListener('DOMContentLoaded', function () {
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
    document.getElementById('btnCerrarModalS')?.addEventListener('click', function () {
        const selecciones = obtenerSeleccionesActuales('S');
        if (!selecciones) {
            alert('Por favor selecciona masa, cobertura y topping antes de agregar al carrito');
            return;
        }

        // Toma los datos del botón
        const cod_producto = Number(this.dataset.codProducto);
        const precio = parseFloat(this.dataset.precio);

        const producto = {
            id: `S-${selecciones.masa.valor}-${selecciones.cobertura.valor}-${selecciones.topping.valor}`,
            cod_producto: cod_producto,
            tipo: 'combo-dona',
            talla: 'S',
            masa: selecciones.masa,
            cobertura: selecciones.cobertura,
            topping: selecciones.topping,
            precio: 8403.36,
            precio: precio,

            titulo: 'Donas Talla S',
            descripcion: `${selecciones.masa.nombre} | ${selecciones.cobertura.nombre} | ${selecciones.topping.nombre}`,
            quantity: 1,
            timestamp: Date.now()
        };

        agregarAlCarrito(producto);



        // Evento para agregar Donas Talla M
        document.getElementById('btnCerrarModalM')?.addEventListener('click', function () {
            const selecciones = obtenerSeleccionesActuales('M');
            if (!selecciones) {
                alert('Por favor selecciona masa, cobertura y topping antes de agregar al carrito');
                return;
            }

            const producto = {
                id: `M-${selecciones.masa.valor}-${selecciones.cobertura.valor}-${selecciones.topping.valor}`,
                cod_producto: "{{producto.cod_producto}}", // <-- este valor debe venir del backend
                tipo: 'combo-dona',
                talla: 'M',
                masa: selecciones.masa,
                cobertura: selecciones.cobertura,
                topping: selecciones.topping,
                precio: 16806.72,
                titulo: 'Donas Talla M',
                descripcion: `${selecciones.masa.nombre} | ${selecciones.cobertura.nombre} | ${selecciones.topping.nombre}`,
                quantity: 1,
                timestamp: Date.now()
            };

            agregarAlCarrito(producto);
        });

        // Evento para agregar Donas Talla L
        document.getElementById('btnCerrarModalL')?.addEventListener('click', function () {
            const selecciones = obtenerSeleccionesActuales('L');
            if (!selecciones) {
                alert('Por favor selecciona masa, cobertura y topping antes de agregar al carrito');
                return;
            }

            const producto = {
                id: `L-${selecciones.masa.valor}-${selecciones.cobertura.valor}-${selecciones.topping.valor}`,
                cod_producto: "{{producto.cod_producto}}", // <-- este valor debe venir del backend
                tipo: 'combo-dona',
                talla: 'L',
                masa: selecciones.masa,
                cobertura: selecciones.cobertura,
                topping: selecciones.topping,
                precio: 25210.08,
                titulo: 'Donas Talla L',
                descripcion: `${selecciones.masa.nombre} | ${selecciones.cobertura.nombre} | ${selecciones.topping.nombre}`,
                quantity: 1,
                timestamp: Date.now()
            };
            agregarAlCarrito(producto);
        });

        // Evento para agregar Donas Talla XL
        document.getElementById('btnCerrarModalXL')?.addEventListener('click', function () {
            const selecciones = obtenerSeleccionesActuales('XL');
            if (!selecciones) {
                alert('Por favor selecciona masa, cobertura y topping antes de agregar al carrito');
                return;
            }

            const producto = {
                id: `XL-${selecciones.masa.valor}-${selecciones.cobertura.valor}-${selecciones.topping.valor}`,
                cod_producto: "{{producto.cod_producto}}", // <-- este valor debe venir del backend
                tipo: 'combo-dona',
                talla: 'XL',
                masa: selecciones.masa,
                cobertura: selecciones.cobertura,
                topping: selecciones.topping,
                precio: 33613.45,
                titulo: 'Donas Talla XL',
                descripcion: `${selecciones.masa.nombre} | ${selecciones.cobertura.nombre} | ${selecciones.topping.nombre}`,
                quantity: 1,
                timestamp: Date.now()
            };

            agregarAlCarrito(producto);
        });
    });

    // Evento para agregar Donas Talla M
    document.getElementById('btnCerrarModalM')?.addEventListener('click', function () {
        const selecciones = obtenerSeleccionesActuales('M');
        if (!selecciones) {
            alert('Por favor selecciona masa, cobertura y topping antes de agregar al carrito');
            return;
        }

        const cod_producto = Number(this.dataset.codProducto);
        const precio = parseFloat(this.dataset.precio);

        const producto = {
            id: `M-${selecciones.masa.valor}-${selecciones.cobertura.valor}-${selecciones.topping.valor}`,
            cod_producto: cod_producto,
            tipo: 'combo-dona',
            talla: 'M',
            masa: selecciones.masa,
            cobertura: selecciones.cobertura,
            topping: selecciones.topping,
            precio: precio,
            titulo: 'Donas Talla M',
            descripcion: `${selecciones.masa.nombre} | ${selecciones.cobertura.nombre} | ${selecciones.topping.nombre}`,
            quantity: 1,
            timestamp: Date.now()
        };

        agregarAlCarrito(producto);
    });

    // Evento para agregar Donas Talla L
    document.getElementById('btnCerrarModalL')?.addEventListener('click', function () {
        const selecciones = obtenerSeleccionesActuales('L');
        if (!selecciones) {
            alert('Por favor selecciona masa, cobertura y topping antes de agregar al carrito');
            return;
        }

        const cod_producto = Number(this.dataset.codProducto);
        const precio = parseFloat(this.dataset.precio);

        const producto = {
            id: `L-${selecciones.masa.valor}-${selecciones.cobertura.valor}-${selecciones.topping.valor}`,
            cod_producto: cod_producto,
            tipo: 'combo-dona',
            talla: 'L',
            masa: selecciones.masa,
            cobertura: selecciones.cobertura,
            topping: selecciones.topping,
            precio: precio,
            titulo: 'Donas Talla L',
            descripcion: `${selecciones.masa.nombre} | ${selecciones.cobertura.nombre} | ${selecciones.topping.nombre}`,
            quantity: 1,
            timestamp: Date.now()
        };
        agregarAlCarrito(producto);
    });

    // Evento para agregar Donas Talla XL
    document.getElementById('btnCerrarModalXL')?.addEventListener('click', function () {
        const selecciones = obtenerSeleccionesActuales('XL');
        if (!selecciones) {
            alert('Por favor selecciona masa, cobertura y topping antes de agregar al carrito');
            return;
        }

        const cod_producto = Number(this.dataset.codProducto);
        const precio = parseFloat(this.dataset.precio);

        const producto = {
            id: `XL-${selecciones.masa.valor}-${selecciones.cobertura.valor}-${selecciones.topping.valor}`,
            cod_producto: cod_producto,
            tipo: 'combo-dona',
            talla: 'XL',
            masa: selecciones.masa,
            cobertura: selecciones.cobertura,
            topping: selecciones.topping,
            precio: precio,
            titulo: 'Donas Talla XL',
            descripcion: `${selecciones.masa.nombre} | ${selecciones.cobertura.nombre} | ${selecciones.topping.nombre}`,
            quantity: 1,
            timestamp: Date.now()
        };

        agregarAlCarrito(producto);
    });

    // Manejo de radio buttons para métodos de pago
    const radioNequi = document.getElementById('radioNequi');
    const radioDavi = document.getElementById('radioDavi');
    const contenedorNequi = document.getElementById('contenedorNequi');
    const contenedorDavi = document.getElementById('contenedorDavi');

    function toggleMetodoPago() {
        if (radioNequi.checked) {
            contenedorNequi.style.display = 'block';
            contenedorDavi.style.display = 'none';
        } else if (radioDavi.checked) {
            contenedorNequi.style.display = 'none';
            contenedorDavi.style.display = 'block';
        }
    }

    // Agregar eventos a los radio buttons
    if (radioNequi) radioNequi.addEventListener('change', toggleMetodoPago);
    if (radioDavi) radioDavi.addEventListener('change', toggleMetodoPago);

    // Manejo de modales específicos
    window.openModal = function (modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'block';
        }
    }

    window.closeModal = function (modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
        }
    }

    // Cerrar modales al hacer click fuera
    window.onclick = function (event) {
        if (event.target.classList.contains('modal-nequi')) {
            event.target.style.display = 'none';
        }
        if (event.target.classList.contains('modal-davi')) {
            event.target.style.display = 'none';
        }
    }
    // Seleccionamos el modal directamente por ID
    // Seleccionamos el modal correcto
    const modalCompraExitosa = document.getElementById('modalCompraExitosa');
    const btnOK = modalCompraExitosa.querySelector('button');
    const btnClose = modalCompraExitosa.querySelector('.close');

    function cerrarModalCompra() {
        modalCompraExitosa.classList.add('hidden');
        modalCompraExitosa.style.display = 'none';
        modalCompraExitosa.style.opacity = '0';
    }

    // Asignamos los listeners
    btnOK?.addEventListener('click', cerrarModalCompra);
    btnClose?.addEventListener('click', cerrarModalCompra);

    // Cerrar al hacer clic fuera del modal
    window.addEventListener('click', function (event) {
        if (event.target === modalCompraExitosa) {
            cerrarModalCompra();
        }
    });
    showHTML();



    // Esta función la llamas cada vez que quieras mostrar el resumen
    window.mostrarModalResumen = function (datos) {
        const contenidoDetalles = modalResumen.querySelector('.resumen-detalles');
        if (contenidoDetalles) {
            contenidoDetalles.innerHTML = datos;
        }
        modalResumen.classList.remove('hidden');
    };


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
window.addEventListener('click', function (event) {
    const modals = document.querySelectorAll(".modal-nequi, .modal-davi");
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});


document.getElementById('btnPagar')?.addEventListener('click', function () {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    let subtotal = cart.reduce((acc, item) => acc + item.precio * item.quantity, 0);
    let iva = subtotal * 0.19;
    let total = subtotal + iva;

    // Factura con estilos Bootstrap tipo lista alineada
    let productosHTML = '';
    if (cart.length === 0) {
        productosHTML = `<div class="alert alert-warning text-center">Tu carrito está vacío</div>`;
        document.getElementById('total-pagar-modal').textContent = '0.00';
    } else {
        productosHTML = `
        <div class="list-group mb-3">
            ${cart.map(item => `
                <div class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${item.titulo}</strong>
                        <div class="text-muted small">${item.descripcion || ''}</div>
                    </div>
                    <div class="text-right">
                        <div><b>Cant:</b> ${item.quantity}</div>
                        <div><b>Unitario:</b> $${item.precio.toFixed(2)}</div>
                        <div><b>Subtotal:</b> $${(item.precio * item.quantity).toFixed(2)}</div>
                    </div>
                </div>
            `).join('')}
        </div>
        <div class="text-left">
            <b>Subtotal:</b> $${subtotal.toFixed(2)}<br>
            <b>IVA (19%):</b> $${iva.toFixed(2)}<br>
            <b>Total:</b> $${total.toFixed(2)}
        </div>
        `;
        document.getElementById('total-pagar-modal').textContent = total.toFixed(2);
    }

    // Asegúrate de que el contenedor existe antes de asignar el HTML
    const cajita = document.querySelector('#modalP .productosPagar .cajita'); if (cajita) {
        cajita.innerHTML = productosHTML;
    }

    // Mostrar el modal solo si hay productos
    const modalP = document.getElementById('modalP');
    if (modalP) {
        if (cart.length > 0) {
            modalP.classList.remove('hidden');
            modalP.style.display = 'flex';
        } else {
            modalP.classList.add('hidden');
            modalP.style.display = 'none';
        }
    }
});

// Cerrar el modal de pago (puedes tener un botón o la X)
document.getElementById('equis')?.addEventListener('click', function () {
    document.getElementById('modalP').style.display = 'none';
});

// Helpers to show modals and get user input as Promise
function getDireccionFromModal() {
    return new Promise((resolve, reject) => {
        const modal = document.getElementById('modalDireccion');
        const input = document.getElementById('inputDireccion');
        const confirm = document.getElementById('confirmDireccion');
        const cancel = document.getElementById('cancelDireccion');
        const close = document.getElementById('closeDireccion');

        function cleanup() {
            confirm.removeEventListener('click', onConfirm);
            cancel.removeEventListener('click', onCancel);
            close.removeEventListener('click', onCancel);
            modal.classList.add('hidden');
        }
        function onConfirm(e) {
            e.preventDefault();
            if (input.value.trim()) {
                cleanup();
                resolve(input.value.trim());
            } else {
                input.focus();
                input.classList.add('input-error');
            }
        }
        function onCancel(e) {
            e.preventDefault();
            cleanup();
            resolve(null);
        }
        input.classList.remove('input-error');
        input.value = '';
        modal.classList.remove('hidden');
        input.focus();
        confirm.addEventListener('click', onConfirm);
        cancel.addEventListener('click', onCancel);
        close.addEventListener('click', onCancel);
    });
}

function getFechaFromModal(minDateStr) {
    return new Promise((resolve, reject) => {
        const modal = document.getElementById('modalFecha');
        const input = document.getElementById('inputFecha');
        const confirm = document.getElementById('confirmFecha');
        const cancel = document.getElementById('cancelFecha');
        const close = document.getElementById('closeFecha');

        function cleanup() {
            confirm.removeEventListener('click', onConfirm);
            cancel.removeEventListener('click', onCancel);
            close.removeEventListener('click', onCancel);
            modal.classList.add('hidden');
        }
        function onConfirm(e) {
            e.preventDefault();
            if (input.value && input.value >= minDateStr) {
                cleanup();
                resolve(input.value);
            } else {
                input.focus();
                input.classList.add('input-error');
            }
        }
        function onCancel(e) {
            e.preventDefault();
            cleanup();
            resolve(null);
        }
        input.classList.remove('input-error');
        input.value = '';
        input.setAttribute('min', minDateStr);
        modal.classList.remove('hidden');
        input.focus();
        confirm.addEventListener('click', onConfirm);
        cancel.addEventListener('click', onCancel);
        close.addEventListener('click', onCancel);
    });
}

document.getElementById('btnAgregarProducto')?.addEventListener('click', async function (e) {
    e.preventDefault();

    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    if (cart.length === 0) {
        alert('El carrito está vacío');
        return;
    }

    // Get address from modal
    const direccion = await getDireccionFromModal();
    if (!direccion) return;

    // Calcular la fecha mínima (hoy + 3 días)
    const hoy = new Date();
    const minDate = new Date(hoy.getFullYear(), hoy.getMonth(), hoy.getDate() + 3);
    const minDateStr = minDate.toISOString().split('T')[0];

    // Get date from modal
    let fechaEntrega = await getFechaFromModal(minDateStr);
    if (!fechaEntrega) return;

    // Obtener método de pago seleccionado
    const metodoPagoSeleccionado = document.querySelector('input[name="metodo_pago"]:checked')?.value;
    // Obtener número de referencia según método de pago
    let referenciaPago = '';
    if (metodoPagoSeleccionado === 'NEQUI') {
        referenciaPago = document.querySelector('#contenedorNequi .nroReferencia')?.value.trim();
    } else if (metodoPagoSeleccionado === 'DAVIPLATA') {
        referenciaPago = document.querySelector('#contenedorDavi .nroReferencia')?.value.trim();
    }

    // Validar campos de pago
    if (!metodoPagoSeleccionado) {
        alert('Debes seleccionar un método de pago.');
        return;
    }
    if (!referenciaPago || referenciaPago.length < 4) {
        alert('Debes digitar un número de referencia válido (mínimo 4 dígitos).');
        return;
    }
    // Ahora puedes usar direccion y fechaEntrega
    const payload = {
        carrito: cart,
        direccion: direccion,
        fecha_entrega: fechaEntrega,
        metodo_pago: metodoPagoSeleccionado,
        transaccion_id: referenciaPago
    };
    console.log('Enviando fetch a /procesar_compra/ con:', payload);

    // Validar método de pago y referencia
    if (!payload.metodo_pago || !payload.transaccion_id) {
        alert('Falta seleccionar método de pago o referencia de pago.');
        return;
    }

    fetch('/procesar_compra/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(payload)
    })
        .then(async response => {
            console.log('Respuesta recibida del backend:', response);
            if (!response.ok) {
                let text = await response.text();
                alert('Respuesta HTTP no OK: ' + response.status + '\n' + text);
                throw new Error('HTTP ' + response.status + ': ' + text);
            }
            try {
                return await response.json();
            } catch (e) {
                alert('La respuesta no es JSON válido: ' + e);
                throw e;
            }
        })
        .then(data => {
            console.log('Respuesta JSON del backend:', data);
            if (data.success) {
                localStorage.removeItem('cart');
                showHTML();
                document.getElementById('modalP').style.display = 'none';
                // Mostrar modal de compra exitosa SOLO con texto centrado (sin imagen)
                const modal = document.getElementById('modalCompraExitosa');
                if (!modal) {
                    console.error('No se encontró el modalCompraExitosa en el DOM');
                    document.body.insertAdjacentHTML('beforeend', `<div style="color:red; background:#fff3cd; border:1px solid #f5c6cb; padding:10px; position:fixed; top:10px; right:10px; z-index:9999;">No se encontró el modalCompraExitosa en el DOM</div>`);
                    return;
                }
                const info = modal.querySelector('.infoTotalCarrito');
                if (info) {
                    info.innerHTML = `
                        <div style="display:flex;align-items:center;justify-content:center;min-height:120px;">
                            <div style="font-size:2em;color:#3C2D31FF;font-family:'Dunkin',Arial,sans-serif;text-align:center;">
                                <b>¡Compra Exitosa!</b>
                            </div>
                        </div>
                    `;
                }
                modal.classList.remove('hidden');
                modal.classList.add('show');
                modal.style.display = 'flex';
                modal.style.opacity = '1';
                modal.style.zIndex = '9999';
                void modal.offsetWidth;
                modal.scrollIntoView({ behavior: 'smooth', block: 'center' });
                if (typeof showHTML === 'function') showHTML();
            } else {
                alert('Error al procesar la compra: ' + (data.error || ''));
            }
        })
        .catch(error => {
            alert('Ocurrió un error al procesar la compra: ' + error);
            document.body.insertAdjacentHTML('beforeend', `<div style="color:red; background:#fff3cd; border:1px solid #f5c6cb; padding:10px, position:fixed, top:10px, right:10px, z-index:9999;">Error: ${error}</div>`);
            console.error('Error en fetch:', error);
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

// Cerrar el modal de compra exitosa y recargar la página correctamente
function cerrarModalCompraExitosa() {
    const modal = document.getElementById('modalCompraExitosa');
    if (modal) {
        // Oculta el modal ANTES de recargar la página
        modal.classList.add('hidden');
        modal.classList.remove('show');
        modal.style.display = 'none';
        modal.style.opacity = '0';
        // Limpia el carrito visualmente
        localStorage.removeItem('cart');
        // Espera un pequeño tiempo para asegurar que el modal se oculte antes de recargar
        setTimeout(() => {
            window.location.reload(true);
        }, 100);
    }
}

// Asigna los listeners al botón OK y la X del modal de compra exitosa
document.addEventListener('DOMContentLoaded', function () {
    // Solo asigna listeners, NO muestres el modal ni lo toques aquí
    const modalCompraExitosa = document.getElementById('modalCompraExitosa');
    if (modalCompraExitosa) {
        modalCompraExitosa.classList.remove('show');
        modalCompraExitosa.classList.add('hidden');
        modalCompraExitosa.style.display = 'none';
        modalCompraExitosa.style.opacity = '0';
        // Listeners para cerrar el modal SOLO cuando está visible
        modalCompraExitosa.querySelector('button')?.addEventListener('click', cerrarModalCompraExitosa);
        modalCompraExitosa.querySelector('.close')?.addEventListener('click', cerrarModalCompraExitosa);
    }
    // Solo carga el carrito, no muestres ni toques el modal de compra exitosa aquí
    showHTML();
});


// Modal personalizado para agregado al carrito
function mostrarModalAgregadoCarrito(producto) {
    const modal = document.getElementById('modalAgregadoCarrito');
    const titulo = document.getElementById('modalAgregadoTitulo');
    const descripcion = document.getElementById('modalAgregadoDescripcion');
    if (!modal || !titulo || !descripcion) return;
    titulo.textContent = producto.titulo || '';
    descripcion.textContent = producto.descripcion || '';
    modal.classList.add('show');
    modal.classList.remove('hidden');
    // Cerrar con X o OK
    const closeBtn = document.getElementById('closeAgregadoCarrito');
    const okBtn = document.getElementById('okAgregadoCarrito');
    function cerrar() {
        modal.classList.remove('show');
        modal.classList.add('hidden');
        closeBtn.removeEventListener('click', cerrar);
        okBtn.removeEventListener('click', cerrar);
    }
    closeBtn.addEventListener('click', cerrar);
    okBtn.addEventListener('click', cerrar);
    // Cerrar con Escape
    function cerrarEscape(e) {
        if (e.key === 'Escape') {
            cerrar();
            document.removeEventListener('keydown', cerrarEscape);
        }
    }
    document.addEventListener('keydown', cerrarEscape);
}

// 1. Asegúrate de que el input de fecha tenga el atributo "min" correctamente
//    y que el modal de fecha esté en el HTML con el id correcto ("modalFecha" y "inputFecha").

// 2. Cuando abras el modal de fecha, asegúrate de establecer el valor mínimo:
function getFechaFromModal(minDateStr) {
    return new Promise((resolve, reject) => {
        const modal = document.getElementById('modalFecha');
        const input = document.getElementById('inputFecha');
        const confirm = document.getElementById('confirmFecha');
        const cancel = document.getElementById('cancelFecha');
        const close = document.getElementById('closeFecha');

        function cleanup() {
            confirm.removeEventListener('click', onConfirm);
            cancel.removeEventListener('click', onCancel);
            close.removeEventListener('click', onCancel);
            modal.classList.add('hidden');
        }
        function onConfirm(e) {
            e.preventDefault();
            if (input.value && input.value >= minDateStr) {
                cleanup();
                resolve(input.value);
            } else {
                input.focus();
                input.classList.add('input-error');
            }
        }
        function onCancel(e) {
            e.preventDefault();
            cleanup();
            resolve(null);
        }
        input.classList.remove('input-error');
        input.value = '';
        input.setAttribute('min', minDateStr); // Esto es correcto
        modal.classList.remove('hidden');
        input.focus();
        confirm.addEventListener('click', onConfirm);
        cancel.addEventListener('click', onCancel);
        close.addEventListener('click', onCancel);
    });
}

// 3. Cuando abras el modal de dirección, asegúrate de que el input tenga el id correcto ("inputDireccion").

// 4. El flujo correcto para la compra es:
//    - El usuario da click en "Comprar" (btnAgregarProducto)
//    - Se abre el modal de dirección y luego el de fecha
//    - Se valida el método de pago y la referencia
//    - Se envía el fetch al backend
//    - Si todo sale bien, se muestra el modal de compra exitosa

// 5. Si el modal de compra exitosa aparece vacío o no se recarga bien:
//    - Asegúrate de que el backend responde con los datos de la venta (data.venta)
//    - Asegúrate de que el código que llena el resumen (info.innerHTML = productosHTML) se ejecuta
//    - Si el modal sigue visible tras recargar, revisa que el HTML no tenga la clase "show" ni "display:flex" tras el reload

// 6. Si el input de fecha aparece vacío o no deja seleccionar fechas, revisa en el HTML que el input tenga el atributo "min" y que el valor sea una fecha válida (YYYY-MM-DD).

// 7. Si el modal de dirección o fecha no aparece, revisa que los IDs en el HTML coincidan con los usados en JS.

// 8. Si el fetch no envía los datos, revisa en la consola del navegador si hay errores de JavaScript.

// 9. Si el resumen de compra aparece vacío, revisa en la consola del navegador el valor de "data" después del fetch.

// 10. Si nada de esto funciona, abre la consola del navegador (F12) y revisa los errores de JavaScript y la respuesta del backend.