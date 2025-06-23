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
    // Verificar que los elementos básicos existan
    if (!rowProduct) {
        console.log('rowProduct no encontrado, omitiendo actualización del carrito');
        return;
    }

    rowProduct.innerHTML = '';

    if (allProducts.length === 0) {
        rowProduct.innerHTML = emptyCartMessage;
        // Verificar que el elemento existe antes de intentar modificarlo
        if (valorTotal) {
            valorTotal.innerText = '$0.00';
        }
        if (countProducts) {
            countProducts.innerText = '0';
        }
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
    initModal('modalB', 'btnInfoB', 'closeB');    initModal('modalOS', 'btnInfoOS', 'closeOS');
    initModal('modalA', 'btnInfoA', 'closeA');
    initModal('modalT1', 'btnInfoT1', 'closeT1');
    initModal('modalT2', 'btnInfoT2', 'closeT2');
    initModal('modalT3', 'btnInfoT3', 'closeT3');
    initModal('modalT4', 'btnInfoT4', 'closeT4');
    // initModal('modalP', 'btnPagar', 'closeP'); // Ya no se usa - ahora se redirige a /pago/

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
    
    if (cart.length === 0) {
        alert('Tu carrito está vacío. Agrega algunos productos antes de proceder al pago.');
        return;
    }

    // Redirigir a la nueva vista de pago
    window.location.href = '/pago/';
});

// Cerrar el modal de pago (ya no se usa)
// document.getElementById('equis')?.addEventListener('click', function () {
//     document.getElementById('modalP').style.display = 'none';
// });

// Funciones auxiliares del modal de pago anterior - ya no se usan
// function getDireccionFromModal() { ... }
// function getFechaFromModal(minDateStr) { ... }
// Se mantiene solo el comentario porque ahora se usa la nueva vista /pago/

// Esta función del modal de pago anterior ya no se usa - ahora se redirige a /pago/
// document.getElementById('btnAgregarProducto')?.addEventListener('click', async function (e) {
//     ... código comentado porque ahora se usa la nueva vista de pago
// });

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
    
    // Verificar que todos los elementos existan antes de continuar
    if (!modal || !titulo || !descripcion) {
        console.log('Modal de agregado al carrito no encontrado, omitiendo...');
        return;
    }
    
    titulo.textContent = producto.titulo || '';
    descripcion.textContent = producto.descripcion || '';
    modal.classList.add('show');
    modal.classList.remove('hidden');
    
    // Cerrar con X o OK
    const closeBtn = document.getElementById('closeAgregadoCarrito');
    const okBtn = document.getElementById('okAgregadoCarrito');
    
    if (!closeBtn || !okBtn) {
        console.log('Botones del modal no encontrados');
        return;
    }
    
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

// Reemplaza confirm() por un modal personalizado para eliminar insumos
function mostrarConfirmacionEliminarInsumo(callback) {
    // Si ya existe el modal, elimínalo primero
    let modal = document.getElementById('modalConfirmarEliminar');
    if (modal) modal.remove();

    // Crea el modal con estilos personalizados
    modal = document.createElement('div');
    modal.id = 'modalConfirmarEliminar';
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100vw';
    modal.style.height = '100vh';
    modal.style.background = 'rgba(0,0,0,0.5)';
    modal.style.display = 'flex';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.style.zIndex = '9999';

    modal.innerHTML = `
        <div style="
            background: #fff;
            border-radius: 24px;
            padding: 32px 32px 24px 32px;
            box-shadow: 0 8px 32px rgba(252,105,152,0.18);
            min-width: 340px;
            max-width: 90vw;
            text-align: center;
            font-family: 'Dunkin', Arial, sans-serif;
            color: #4e4032;
            border: 4px solid #fc6998;
        ">
            <div style="font-size: 2.2em; margin-bottom: 10px;">
                <i class="bi bi-exclamation-triangle-fill" style="color:#fc6998;"></i>
            </div>
            <div style="font-size: 1.2em; margin-bottom: 18px;">
                ¿Estás seguro de que deseas eliminar este insumo?
            </div>
            <div style="display: flex; justify-content: center; gap: 18px;">
                <button id="btnConfirmarEliminar" style="
                    background: #fc6998;
                    color: #fff;
                    border: none;
                    border-radius: 50px;
                    padding: 10px 32px;
                    font-size: 1em;
                    font-family: 'Dunkin', Arial, sans-serif;
                    cursor: pointer;
                    transition: background 0.2s;
                ">Sí, eliminar</button>
                <button id="btnCancelarEliminar" style="
                    background: #fff;
                    color: #fc6998;
                    border: 2px solid #fc6998;
                    border-radius: 50px;
                    padding: 10px 32px;
                    font-size: 1em;
                    font-family: 'Dunkin', Arial, sans-serif;
                    cursor: pointer;
                    transition: background 0.2s, color 0.2s;
                ">Cancelar</button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    document.getElementById('btnConfirmarEliminar').onclick = function() {
        modal.remove();
        if (typeof callback === 'function') callback(true);
    };
    document.getElementById('btnCancelarEliminar').onclick = function() {
        modal.remove();
        if (typeof callback === 'function') callback(false);
    };
}

// Ejemplo de uso en tu código (reemplaza confirm(...) por esto):
// mostrarConfirmacionEliminarInsumo(function(confirmado) {
//     if (confirmado) {
//         // Eliminar insumo
//     }
// });