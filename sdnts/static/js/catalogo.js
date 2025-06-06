// Selección de elementos del DOM
const btnCart = document.querySelector('.carrito');
const containerCartProducts = document.querySelector('.container-cart-products');
const rowProduct = document.querySelector('.row-product');
let allProducts = [];
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
}

// Función para configurar la selección de sabores
function configurarSeleccionSabores(modal, size) {
    modal.querySelectorAll('.sabor-option').forEach(option => {
        option.addEventListener('click', function() {
            const tipo = this.closest('.opcion-seleccion').querySelector('h4').textContent.toLowerCase();
            const valor = this.dataset.value;

            // Quitar 'active' solo en este grupo
            this.parentElement.querySelectorAll('.sabor-option').forEach(opt => {
                opt.classList.remove('active');
            });
            this.classList.add('active');

            // Actualizar la vista previa de la dona
            if (tipo === 'masa') {
                modal.querySelector(`#dona-masa-${size}`).style.backgroundColor = colores.masa[valor];
            } else if (tipo === 'cobertura') {
                modal.querySelector(`#dona-cobertura-${size}`).style.backgroundColor = colores.cobertura[valor];
            } else if (tipo === 'toppings') {
                const topping = modal.querySelector(`#dona-topping-${size}`);
                topping.style.backgroundImage = colores.toppings[valor];
                topping.style.display = (valor === 'ninguno') ? 'none' : 'block';
            }
        });
    });

    // Inicializar valores por defecto
    const masaElement = modal.querySelector(`#dona-masa-${size}`);
    const coberturaElement = modal.querySelector(`#dona-cobertura-${size}`);
    const toppingElement = modal.querySelector(`#dona-topping-${size}`);

    if (masaElement && coberturaElement && toppingElement) {
        masaElement.style.backgroundColor = colores.masa['vainilla'];
        coberturaElement.style.backgroundColor = colores.cobertura['chocolate-blanco'];
        toppingElement.style.backgroundImage = colores.toppings['chispas'];
        toppingElement.style.display = 'block';
    }
}

// Función para agregar producto al carrito
function agregarProductoAlCarrito(size) {
    const modal = document.getElementById(`modal${size}`);
    if (!modal) return;

    const titulo = modal.querySelector('h1')?.textContent || `Combo Talla ${size}`;
    const priceElement = modal.querySelector('.precio');
    let price = 0;

    if (priceElement) {
        price = parseFloat(priceElement.textContent.replace('$', '').replace('.', '').replace(',', ''));
    } else {
        // Precios por defecto según talla si no se encuentra el elemento
        const prices = { 'S': 10000, 'M': 20000, 'L': 30000, 'XL': 40000 };
        price = prices[size] || 0;
    }

    const infoProduct = {
        quantity: 1,
        titulo: titulo,
        price: price,
        size: size
    };

    const existingProduct = allProducts.find(item => item.titulo === infoProduct.titulo && item.size === infoProduct.size);
    if (existingProduct) {
        existingProduct.quantity++;
    } else {
        allProducts.push(infoProduct);
    }

    showHTML();
}

document.addEventListener('DOMContentLoaded', function() {
    // Configuración de productos
    const productConfig = {
        precios: { S: 10.00, M: 15.00, L: 20.00, XL: 25.00 },
        nombres: {
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
        }
    };

    // Obtener elementos del DOM
    const btnAgregarXL = document.getElementById('btnCerrarModalXL');
    
    // Evento para el botón Agregar al carrito
    if (btnAgregarXL) {
        btnAgregarXL.addEventListener('click', function() {
            const talla = this.dataset.talla;
            const precio = parseFloat(this.dataset.precio);
            
            // Obtener selecciones actuales
            const selecciones = getSeleccionesActuales('XL');
            
            // Crear objeto producto para el carrito
            const producto = {
                id: generarIdUnico(selecciones),
                tipo: 'combo-dona',
                talla: talla,
                masa: selecciones.masa,
                cobertura: selecciones.cobertura,
                topping: selecciones.topping,
                precio: precio,
                titulo: generarTituloProducto(selecciones, talla),
                quantity: 1
            };
            
            // Agregar al carrito
            agregarAlCarrito(producto);
        });
    }

    // Función para obtener las selecciones actuales
    function getSeleccionesActuales(talla) {
        const modal = document.getElementById(`modal${talla}`);
        if (!modal) return {};
        
        return {
            masa: {
                valor: modal.querySelector('.opcion-seleccion[data-tipo="masa"] .sabor-option.active').dataset.value,
                nombre: productConfig.nombres.masa[modal.querySelector('.opcion-seleccion[data-tipo="masa"] .sabor-option.active').dataset.value]
            },
            cobertura: {
                valor: modal.querySelector('.opcion-seleccion[data-tipo="cobertura"] .sabor-option.active').dataset.value,
                nombre: productConfig.nombres.cobertura[modal.querySelector('.opcion-seleccion[data-tipo="cobertura"] .sabor-option.active').dataset.value]
            },
            topping: {
                valor: modal.querySelector('.opcion-seleccion[data-tipo="topping"] .sabor-option.active').dataset.value,
                nombre: productConfig.nombres.topping[modal.querySelector('.opcion-seleccion[data-tipo="topping"] .sabor-option.active').dataset.value]
            }
        };
    }

    // Función para generar ID único basado en las selecciones
    function generarIdUnico(selecciones) {
        return `dona-${selecciones.masa.valor}-${selecciones.cobertura.valor}-${selecciones.topping.valor}`;
    }

    // Función para generar título descriptivo del producto
    function generarTituloProducto(selecciones, talla) {
        return `Combo Donas ${talla}: ${selecciones.masa.nombre}, ${selecciones.cobertura.nombre}, ${selecciones.topping.nombre}`;
    }

    // Función para agregar al carrito (adaptar a tu implementación)
    function agregarAlCarrito(producto) {
        // Verificar si el producto ya está en el carrito
        const index = allProducts.findIndex(p => p.id === producto.id);
        
        if (index !== -1) {
            // Si ya existe, incrementar cantidad
            allProducts[index].quantity += 1;
        } else {
            // Si no existe, agregar nuevo producto
            allProducts.push(producto);
        }
        
        // Actualizar localStorage
        localStorage.setItem('cart', JSON.stringify(allProducts));
        
        // Actualizar interfaz
        showHTML();
        
        // Mostrar notificación
        alert(`¡Agregado al carrito!\n${producto.titulo}`);
    }
});

// Función para mostrar los productos en el carrito (actualizada)
function showHTML() {
    if (!rowProduct) return;

    rowProduct.innerHTML = '';

    if (allProducts.length === 0) {
        rowProduct.innerHTML = emptyCartMessage;
        if (valorTotal) valorTotal.innerText = '$0.00';
        if (countProducts) countProducts.innerText = '0';
    } else {
        let total = 0;
        let totalOfProduct = 0;

        allProducts.forEach(product => {
            const containerProduct = document.createElement('div');
            containerProduct.classList.add('cart-product');

            containerProduct.innerHTML = `
                <div class="info-cart-product">
                    <span class="cantidad-producto-carrito">${product.quantity}</span>
                    <p class="titulo-producto-carrito">${product.titulo}</p>
                    <span class="precio-producto-carrito">$${(product.price * product.quantity).toLocaleString()}</span>
                    <button class="btn-eliminar" data-id="${product.id}">−</button>
                </div>
                <div class="detalles-producto-carrito">
                    <small>Masa: ${product.masa.nombre}</small><br>
                    <small>Cobertura: ${product.cobertura.nombre}</small><br>
                    <small>Topping: ${product.topping.nombre}</small>
                </div>`;

            rowProduct.append(containerProduct);
            total += product.quantity * product.price;
            totalOfProduct += product.quantity;
        });

        if (valorTotal) valorTotal.innerText = `$${total.toLocaleString()}`;
        if (countProducts) countProducts.innerText = totalOfProduct;
    }
}
// Evento para eliminar productos del carrito
if (rowProduct) {
    rowProduct.addEventListener('click', e => {
        if (e.target.classList.contains('icon-close')) {
            const titleToRemove = e.target.getAttribute('data-title');
            const sizeToRemove = e.target.getAttribute('data-size');
            allProducts = allProducts.filter(product => 
                !(product.titulo === titleToRemove && product.size === sizeToRemove)
            );
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
function showHTML() {
    if (!rowProduct) return;

    rowProduct.innerHTML = '';

    if (allProducts.length === 0) {
        rowProduct.innerHTML = emptyCartMessage;
    } else {
        allProducts.forEach(product => {
            const containerProduct = document.createElement('div');
            containerProduct.classList.add('cart-product');

            containerProduct.innerHTML = `
                <div class="info-cart-product">
                    <span class="cantidad-producto-carrito">${product.quantity}</span>
                    <p class="titulo-producto-carrito">${product.titulo}</p>
                    <p class="personalizacion">
                        Masa: ${product.masa || '-'}<br>
                        Cobertura: ${product.cobertura || '-'}<br>
                        Topping: ${product.topping || '-'}
                    </p>
                    <span class="precio-producto-carrito">$${(product.price * product.quantity).toLocaleString()}</span>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="icon-close" data-id="${product.id}">
                        <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25Zm-1.72 6.97a.75.75 0 1 0-1.06 1.06L10.94 12l-1.72 1.72a.75.75 0 1 0 1.06 1.06L12 13.06l1.72 1.72a.75.75 0 1 0 1.06-1.06L13.06 12l1.72-1.72a.75.75 0 1 0-1.06-1.06L12 10.94l-1.72-1.72Z" clip-rule="evenodd" />
                    </svg>
                </div>`;

            rowProduct.append(containerProduct);
        });
    }

    updateCartCounter();
    updateTotal();
    saveCartToStorage();
}

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
    if (existingProduct) {
        existingProduct.quantity++;
    } else {
        allProducts.push(infoProduct);
    }

    showHTML();
}

// Evento para eliminar productos del carrito
if (rowProduct) {
    rowProduct.addEventListener('click', e => {
        if (e.target.classList.contains('icon-close')) {
            const productId = e.target.getAttribute('data-id');
            allProducts = allProducts.filter(product => product.id !== productId);
            showHTML();
        }
    });
}

// Evento para mostrar/ocultar el carrito
if (btnCart && containerCartProducts) {
    btnCart.addEventListener('click', () => {
        containerCartProducts.classList.toggle('hidden-cart');
    });

    // Cerrar el carrito al hacer clic fuera
    document.addEventListener('click', (event) => {
        const isClickInsideCart = containerCartProducts.contains(event.target);
        const isClickOnButton = btnCart.contains(event.target);

        if (!isClickInsideCart && !isClickOnButton) {
            containerCartProducts.classList.add('hidden-cart');
        }
    });
}

// Funciones para los modales de pago
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

// Inicialización del carrito al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    // Cargar carrito desde localStorage
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
        allProducts = JSON.parse(savedCart);
    }
    
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