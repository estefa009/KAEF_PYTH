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
        'chispas': "url('{% static 'Image/pepitasPatron.png' %}')",
        'oreo': "url('{% static 'Image/oreoPatron.png' %}')",
        'mym': "url('{% static 'Image/mymPatron.png' %}')",
        'chips': "url('{% static 'Image/chipsPatron.png' %}')",
        'ninguno': 'none'
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
    if (['S', 'M', 'L', 'XL'].includes(size)) {
        configurarSeleccionSabores(modal, size);
    }
}document.addEventListener('DOMContentLoaded', function() {
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
function obtenerSeleccionesActuales(talla) {
    const modal = document.getElementById(`modal${talla}`);
    if (!modal) {
        console.error('Modal no encontrado para talla:', talla);
        return null;
    }
    
    // Buscar las opciones activas de manera más robusta
    const masaActive = modal.querySelector('.opcion-seleccion h4:contains("Masa")').nextElementSibling.querySelector('.sabor-option.active');
    const coberturaActive = modal.querySelector('.opcion-seleccion h4:contains("Cobertura")').nextElementSibling.querySelector('.sabor-option.active');
    const toppingActive = modal.querySelector('.opcion-seleccion h4:contains("Toppings")').nextElementSibling.querySelector('.sabor-option.active');

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
    btnAgregarS.addEventListener('click', function() {
    const talla = this.dataset.talla;
    const precio = parseFloat(this.dataset.precio);
    
    console.log('Intentando agregar producto talla:', talla);
    
    const selecciones = obtenerSeleccionesActuales(talla);
    
    if (!selecciones) {
        alert('Por favor selecciona masa, cobertura y topping antes de agregar al carrito');
        return; // Detener la ejecución si no hay selecciones
    }
    
    console.log('Selecciones encontradas:', selecciones);
    
    const producto = {
        id: `${talla}-${selecciones.masa.valor}-${selecciones.cobertura.valor}-${selecciones.topping.valor}`,
        tipo: 'combo-dona',
        talla: talla,
        masa: selecciones.masa,
        cobertura: selecciones.cobertura,
        topping: selecciones.topping,
        precio: precio,
        titulo: `Donas ${talla}`,
        descripcion: `${selecciones.masa.nombre} | ${selecciones.cobertura.nombre} | ${selecciones.topping.nombre}`,
        quantity: 1,
        timestamp: Date.now() // Para hacer el ID más único
    };
    
    console.log('Producto a agregar:', producto);
    
    agregarAlCarrito(producto);
});

    // Función para generar ID único del producto
    function generarIdProducto(selecciones) {
        return `dona-${selecciones.masa.valor}-${selecciones.cobertura.valor}-${selecciones.topping.valor}-${Date.now()}`;
    }

    // Función para generar descripción detallada
    function generarDescripcion(selecciones) {
        return `Masa: ${selecciones.masa.nombre}, Cobertura: ${selecciones.cobertura.nombre}, Topping: ${selecciones.topping.nombre}`;
    }

    // Función para agregar al carrito (adaptar a tu implementación)
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

// Función showHTML actualizada para mostrar detalles
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

// Inicializar todos los modales
document.addEventListener('DOMContentLoaded', function() {
    // Modales de combos
    initModal('modalS', 'btnAgregar', 'closeS', 'btnCerrarModalS', 'S');
    initModal('modalM', 'btnAgregarM', 'closeM', 'btnCerrarModalM', 'M');
    initModal('modalL', 'btnAgregarL', 'closeL', 'btnCerrarModalL', 'L');
    initModal('modalXL', 'btnAgregarXL', 'closeXL', 'btnCerrarModalXL', 'XL');
    
    // Modales de información
    initModal('modalV', 'btnInfoV', 'closeV', 'btnCerrarModalV');
    initModal('modalC', 'btnInfoC', 'closeC', 'btnCerrarModalC');
    initModal('modalR', 'btnInfoR', 'closeR', 'btnCerrarModalR');
    initModal('modalB', 'btnInfoB', 'closeB', 'btnCerrarModalB');
    initModal('modalOS', 'btnInfoOS', 'closeOS', 'btnCerrarModalOS');
    initModal('modalA', 'btnInfoA', 'closeA', 'btnCerrarModalA');
    initModal('modalT1', 'btnInfoT1', 'closeT1', 'btnCerrarModalT1');
    initModal('modalT2', 'btnInfoT2', 'closeT2', 'btnCerrarModalT2');
    initModal('modalT3', 'btnInfoT3', 'closeT3', 'btnCerrarModalT3');
    initModal('modalT4', 'btnInfoT4', 'closeT4', 'btnCerrarModalT4');
    initModal('modalP', 'btnPagar', 'closeP');

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


// -----------------------------ajustes para el carrito carlexy-------------------------------

// Selección de elementos del DOM
const totalPagarModal = document.getElementById('total-pagar-modal');

// Carrito en memoria (temporal) con localStorage
allProducts = JSON.parse(localStorage.getItem('cart')) || [];

// Función para guardar el carrito en localStorage
function saveCartToStorage() {
    localStorage.setItem('cart', JSON.stringify(allProducts));
}

// Función para actualizar el contador
function updateCartCounter() {
    if (countProducts) {
        const totalItems = allProducts.reduce((total, product) => total + product.quantity, 0);
        countProducts.textContent = totalItems;
    }
}

// Función para actualizar el total
function updateTotal() {
    const total = allProducts.reduce((sum, product) => sum + (product.price * product.quantity), 0);
    
    if (valorTotal) {
        valorTotal.textContent = `$${total.toLocaleString()}`;
    }
    
    if (totalPagarModal) {
        totalPagarModal.textContent = total.toLocaleString();
    }
}

// Función para mostrar los productos en el carrito
// (Eliminado: función duplicada, ya está definida correctamente más arriba)
// Función para agregar producto al carrito
function agregarProductoAlCarrito(size) {
    const modal = document.getElementById(`modal${size}`);
    if (!modal) return;

    const titulo = modal.querySelector('h1')?.textContent || `Combo Talla ${size}`;
    const priceElement = modal.querySelector('.precio');
    let price = 0;

    // Obtener selecciones de personalización
    const masaSeleccionada = modal.querySelector('.opcion-seleccion:nth-child(1) .sabor-option.active')?.textContent.trim() || 'Vainilla';
    const coberturaSeleccionada = modal.querySelector('.opcion-seleccion:nth-child(2) .sabor-option.active')?.textContent.trim() || 'Chocolate Blanco';
    const toppingSeleccionado = modal.querySelector('.opcion-seleccion:nth-child(3) .sabor-option.active')?.textContent.trim() || 'Chispas';

    if (priceElement) {
        price = parseFloat(priceElement.textContent.replace('$', '').replace('.', ''));
    } else {
        // Precios por defecto según talla
        const prices = { 'S': 10000, 'M': 20000, 'L': 30000, 'XL': 40000 };
        price = prices[size] || 0;
    }

    const productId = `${size}-${masaSeleccionada}-${coberturaSeleccionada}-${toppingSeleccionado}`.replace(/\s+/g, '-');

    const infoProduct = {
        id: productId,
        quantity: 1,
        titulo: titulo,
        price: price,
        size: size,
        masa: masaSeleccionada,
        cobertura: coberturaSeleccionada,
        topping: toppingSeleccionado
    };

    const existingProduct = allProducts.find(item => item.id === productId);
// Función para agregar producto al carrito
function agregarProductoAlCarrito(size) {
    const modal = document.getElementById(`modal${size}`);
    if (!modal) return;

    const titulo = modal.querySelector('h1')?.textContent || `Combo Talla ${size}`;
    const priceElement = modal.querySelector('.precio');
    let precio = 0;

    // Obtener selecciones de personalización
    const masaSeleccionada = modal.querySelector('.opcion-seleccion:nth-child(1) .sabor-option.active')?.textContent.trim() || 'Vainilla';
    const coberturaSeleccionada = modal.querySelector('.opcion-seleccion:nth-child(2) .sabor-option.active')?.textContent.trim() || 'Chocolate Blanco';
    const toppingSeleccionado = modal.querySelector('.opcion-seleccion:nth-child(3) .sabor-option.active')?.textContent.trim() || 'Chispas';

    if (priceElement) {
        precio = parseFloat(priceElement.textContent.replace('$', '').replace('.', ''));
    } else {
        // Precios por defecto según talla
        const prices = { 'S': 10000, 'M': 20000, 'L': 30000, 'XL': 40000 };
        precio = prices[size] || 0;
    }

    const productId = `${size}-${masaSeleccionada}-${coberturaSeleccionada}-${toppingSeleccionado}`.replace(/\s+/g, '-');

    const descripcion = `Masa: ${masaSeleccionada} | Cobertura: ${coberturaSeleccionada} | Topping: ${toppingSeleccionado}`;

    const infoProduct = {
        id: productId,
        quantity: 1,
        titulo: titulo,
        precio: precio,
        talla: size,
        masa: masaSeleccionada,
        cobertura: coberturaSeleccionada,
        topping: toppingSeleccionado,
        descripcion: descripcion
    };

    const existingProduct = allProducts.find(item => item.id === productId);
    if (existingProduct) {
        existingProduct.quantity++;
    } else {
        allProducts.push(infoProduct);
    }

// (Eliminado: evento duplicado, ya está unificado arriba)
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };

// Inicialización del carrito al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    // Cargar carrito desde localStorage
    const savedCart = localStorage.getItem('cart');
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
    // Configurar botón de cerrar modal de pago
    const closeP = document.querySelector('.closeP');
    if (closeP) {
        closeP.addEventListener('click', () => {
            document.getElementById('modalP').classList.add('hidden');
        });
    }
    
    // Configurar botón de comprar
    const btnComprar = document.getElementById('btnAgregarProducto');
    if (btnComprar) {
        btnComprar.addEventListener('click', () => {
            // Aquí puedes agregar lógica para procesar el pago
            alert('Compra realizada con éxito!');
            allProducts = [];
            showHTML();
            document.getElementById('modalP').classList.add('hidden');
        });
    }

// Inicialización del carrito al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    // Mostrar el estado inicial del carrito
    showHTML();
    
    // Configurar botón de pagar
    const btnPagar = document.getElementById('btnPagar');
    if (btnPagar) {
        btnPagar.addEventListener('click', (e) => {
            e.preventDefault();
            document.getElementById('modalP').classList.remove('hidden');
        });
    }
    
    // Configurar botón de cerrar modal de pago
    const closeP = document.querySelector('.closeP');
    if (closeP) {
        closeP.addEventListener('click', () => {
            document.getElementById('modalP').classList.add('hidden');
        });
    }
    
    // Configurar botón de comprar
    const btnComprar = document.getElementById('btnAgregarProducto');
    if (btnComprar) {
        btnComprar.addEventListener('click', () => {
            // Aquí puedes agregar lógica para procesar el pago
            alert('Compra realizada con éxito!');
            allProducts = [];
            showHTML();
            document.getElementById('modalP').classList.add('hidden');
        });
    }
});

