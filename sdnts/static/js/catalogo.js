// Selección de elementos del DOM
const btnCart = document.querySelector('.carrito');
const ContainerCartProducts = document.querySelector('.container-cart-products');
const rowProduct = document.querySelector('.row-product');
let allProducts = [];
const valorTotal = document.querySelector('.total-pagar');
const countProducts = document.querySelector('#contador-productos');
const emptyCartMessage = '<p class="empty-cart-message">Tu carrito está vacío</p>';

// Evento para mostrar/ocultar el carrito
btnCart.addEventListener('click', () => {
    ContainerCartProducts.classList.toggle('hidden-cart');
});
// Cerrar el carrito al hacer clic fuera del contenedor
document.addEventListener('click', (event) => {
    const isClickInsideCart = ContainerCartProducts.contains(event.target);
    const isClickOnButton = btnCart.contains(event.target);

    // Si el clic no es en el carrito ni en el botón, ocultamos el carrito
    if (!isClickInsideCart && !isClickOnButton) {
        ContainerCartProducts.classList.add('hidden-cart');
    }
});

// Función para mostrar los productos en el carrito
// Función para mostrar los productos en el carrito
const showHTML = () => {
    rowProduct.innerHTML = ''; // Limpiar el contenedor antes de agregar nuevos elementos

    if (allProducts.length === 0) {
        rowProduct.innerHTML = emptyCartMessage; // Mostrar mensaje si el carrito está vacío
        valorTotal.innerText = '$0.00'; // Asegúrate de que el total sea cero
        countProducts.innerText = '0'; // Asegúrate de que el contador sea cero
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
                    <span class="precio-producto-carrito">$${(product.price * product.quantity).toFixed(2)}</span>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="icon-close" data-title="${product.titulo}">
                        <path fill-rule="evenodd" d="M5.47 5.47a.75.75 0 0 1 1.06 0L12 10.94l5.47-5.47a.75.75 0 1 1 1.06 1.06L13.06 12l5.47 5.47a.75.75 0 1 1-1.06 1.06L12 13.06l-5.47 5.47a.75.75 0 0 1-1.06-1.06L10.94 12 5.47 6.53a.75.75 0 0 1 0-1.06Z" clip-rule="evenodd" />
                    </svg>
                </div>`;

            rowProduct.append(containerProduct);
            total += product.quantity * product.price;
            totalOfProduct += product.quantity;
        });

        valorTotal.innerText = `$${total.toFixed(2)}`; // Actualizar el total
        countProducts.innerText = totalOfProduct; // Actualizar el contador
    }
};



// Evento para eliminar productos del carrito
rowProduct.addEventListener('click', e => {
    if (e.target.classList.contains('icon-close')) {
        const titleToRemove = e.target.getAttribute('data-title');
        allProducts = allProducts.filter(product => product.titulo !== titleToRemove);
        showHTML();
    }
});

const productList = document.querySelector('.modal-content');

// Función para agregar el producto al carrito
const agregarProductoAlCarrito = (size) => {
    const modal = document.querySelector(`#modal${size}`);
    const titulo = modal.querySelector('h1').textContent;
    const price = parseFloat(modal.querySelector('.modal-price').textContent.replace('$', '').replace('.', '').replace(',', ''));

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

// Funciones para manejar los modales y añadir productos con talla
const handleModal = (btnAgregar, modal, closeBtn, addToCartBtn, size) => {
    if (btnAgregar) {
        btnAgregar.addEventListener('click', () => {
            modal.classList.remove('hidden'); 
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            modal.classList.add('hidden'); 
        });
    }

    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', () => {
            agregarProductoAlCarrito(size); 
            modal.classList.add('hidden'); 
        });
    }
};

// Manejo de modales para las diferentes tallas
const btnInfoS = document.getElementById('btnAgregar');
const modalS = document.getElementById('modalS');
const closeS = document.querySelector('.closeS');
const btnCerrarModalS = document.getElementById('btnCerrarModalS');
handleModal(btnInfoS, modalS, closeS, btnCerrarModalS, 'S');

const btnInfoM = document.getElementById('btnAgregarM');
const modalM = document.getElementById('modalM');
const closeM = document.querySelector('.closeM');
const btnCerrarModalM = document.getElementById('btnCerrarModalM');
handleModal(btnInfoM, modalM, closeM, btnCerrarModalM, 'M');

const btnInfoL = document.getElementById('btnAgregarL');
const modalL = document.getElementById('modalL');
const closeL = document.querySelector('.closeL');
const btnCerrarModalL = document.getElementById('btnCerrarModalL');
handleModal(btnInfoL, modalL, closeL, btnCerrarModalL, 'L');

const btnInfoXL = document.getElementById('btnAgregarXL');
const modalXL = document.getElementById('modalXL');
const closeXL = document.querySelector('.closeXL');
const btnCerrarModalXL = document.getElementById('btnCerrarModalXL');
handleModal(btnInfoXL, modalXL, closeXL, btnCerrarModalXL, 'XL');

const btnInfoP = document.getElementById('btnPagar');
const modalP = document.getElementById('modalP');
const closeP = document.querySelector('.closeP');
const btnCerrarModalP = document.getElementById('btnCerrarModalP');
handleModal(btnInfoP, modalP, closeP, btnCerrarModalP, 'P');

// Llamar a showHTML al inicio para mostrar el estado inicial del carrito
showHTML(); 


//////////////////BOTON PAGAR////////////////////////////////


// Funciones para manejar el modal de Talla V
const btnInfoV = document.getElementById('btnInfoV');
const modalV = document.getElementById('modalV');
const closeV = document.querySelector('.closeV');
const btnCerrarModalV = document.getElementById('btnCerrarModalV');

// Función para abrir el modal de Talla V
if (btnInfoV) {
    btnInfoV.addEventListener('click', () => {
        modalV.classList.remove('hidden'); // Muestra el modal
    });
}

// Función para cerrar el modal de Talla V
const cerrarModalV = () => {
    modalV.classList.add('hidden'); // Oculta el modal
};

// Añadir eventos para cerrar el modal de Talla V
if (closeV) {
    closeV.addEventListener('click', cerrarModalV);
}
if (btnCerrarModalV) {
    btnCerrarModalV.addEventListener('click', cerrarModalV);
}


// Funciones para manejar el modal de Talla C
const btnInfoC = document.getElementById('btnInfoC');
const modalC = document.getElementById('modalC');
const closeC = document.querySelector('.closeC');
const btnCerrarModalC = document.getElementById('btnCerrarModalC');

// Función para abrir el modal de Talla C
if (btnInfoC) {
    btnInfoC.addEventListener('click', () => {
        modalC.classList.remove('hidden'); // Muestra el modal
    });
}

// Función para cerrar el modal de Talla C
const cerrarModalC = () => {
    modalC.classList.add('hidden'); // Oculta el modal
};

// Añadir eventos para cerrar el modal de Talla C
if (closeC) {
    closeC.addEventListener('click', cerrarModalC);
}
if (btnCerrarModalC) {
    btnCerrarModalC.addEventListener('click', cerrarModalC);
}

// Funciones para manejar el modal de Talla R
const btnInfoR = document.getElementById('btnInfoR');
const modalR = document.getElementById('modalR');
const closeR = document.querySelector('.closeR');
const btnCerrarModalR = document.getElementById('btnCerrarModalR');

// Función para abrir el modal de Talla R
if (btnInfoR) {
    btnInfoR.addEventListener('click', () => {
        modalR.classList.remove('hidden'); // Muestra el modal
    });
}

// Función para cerrar el modal de Talla R
const cerrarModalR = () => {
    modalR.classList.add('hidden'); // Oculta el modal
};

// Añadir eventos para cerrar el modal de Talla R
if (closeR) {
    closeR.addEventListener('click', cerrarModalR);
}
if (btnCerrarModalR) {
    btnCerrarModalR.addEventListener('click', cerrarModalR);
}

// Funciones para manejar el modal de Talla B
const btnInfoB = document.getElementById('btnInfoB');
const modalB = document.getElementById('modalB');
const closeB = document.querySelector('.closeB');
const btnCerrarModalB = document.getElementById('btnCerrarModalB');

// Función para abrir el modal de Talla B
if (btnInfoB) {
    btnInfoB.addEventListener('click', () => {
        modalB.classList.remove('hidden'); // Muestra el modal
    });
}

// Función para cerrar el modal de Talla B
const cerrarModalB = () => {
    modalB.classList.add('hidden'); // Oculta el modal
};

// Añadir eventos para cerrar el modal de Talla B
if (closeB) {
    closeB.addEventListener('click', cerrarModalB);
}
if (btnCerrarModalB) {
    btnCerrarModalB.addEventListener('click', cerrarModalB);
}


// Funciones para manejar el modal de Talla OS
const btnInfoOS = document.getElementById('btnInfoOS');
const modalOS = document.getElementById('modalOS');
const closeOS = document.querySelector('.closeOS');
const btnCerrarModalOS = document.getElementById('btnCerrarModalOS');

// Función para abrir el modal de Talla OS
if (btnInfoOS) {
    btnInfoOS.addEventListener('click', () => {
        modalOS.classList.remove('hidden'); // Muestra el modal
    });
}

// Función para cerrar el modal de Talla OS
const cerrarModalOS = () => {
    modalOS.classList.add('hidden'); // Oculta el modal
};

// Añadir eventos para cerrar el modal de Talla OS
if (closeOS) {
    closeOS.addEventListener('click', cerrarModalOS);
}
if (btnCerrarModalOS) {
    btnCerrarModalOS.addEventListener('click', cerrarModalOS);
}



// Funciones para manejar el modal de Talla A
const btnInfoA = document.getElementById('btnInfoA');
const modalA = document.getElementById('modalA');
const closeA = document.querySelector('.closeA');
const btnCerrarModalA = document.getElementById('btnCerrarModalA');

// Función para abrir el modal de Talla A
if (btnInfoA) {
    btnInfoA.addEventListener('click', () => {
        modalA.classList.remove('hidden'); // Muestra el modal
    });
}

// Función para cerrar el modal de Talla A
const cerrarModalA = () => {
    modalA.classList.add('hidden'); // Oculta el modal
};

// Añadir eventos para cerrar el modal de Talla A
if (closeA) {
    closeA.addEventListener('click', cerrarModalA);
}
if (btnCerrarModalA) {
    btnCerrarModalA.addEventListener('click', cerrarModalA);
}

// Funciones para manejar el modal de Talla T1

const btnInfoT1 = document.getElementById('btnInfoT1');
const modalT1 = document.getElementById('modalT1');
const closeT1 = document.querySelector('.closeT1');
const btnCerrarModalT1 = document.getElementById('btnCerrarModalT1');

// Función para abrir el modal de Talla T1

if (btnInfoT1) {
    btnInfoT1.addEventListener('click', () => {
        modalT1.classList.remove('hidden'); // Muestra el modal
    });
}

// Función para cerrar el modal de Talla T1

const cerrarModalT1 = () => {
    modalT1.classList.add('hidden'); // Oculta el modal
};

// Añadir eventos para cerrar el modal de Talla T1

if (closeT1) {
    closeT1.addEventListener('click', cerrarModalT1);
}
if (btnCerrarModalT1) {
    btnCerrarModalT1.addEventListener('click', cerrarModalT1);
}


// Funciones para manejar el modal de Talla T2

const btnInfoT2 = document.getElementById('btnInfoT2');
const modalT2 = document.getElementById('modalT2');
const closeT2 = document.querySelector('.closeT2');
const btnCerrarModalT2 = document.getElementById('btnCerrarModalT2');

// Función para abrir el modal de Talla T2

if (btnInfoT2) {
    btnInfoT2.addEventListener('click', () => {
        modalT2.classList.remove('hidden'); // Muestra el modal
    });
}

// Función para cerrar el modal de Talla T2

const cerrarModalT2 = () => {
    modalT2.classList.add('hidden'); // Oculta el modal
};

// Añadir eventos para cerrar el modal de Talla T2

if (closeT2) {
    closeT2.addEventListener('click', cerrarModalT2);
}
if (btnCerrarModalT2) {
    btnCerrarModalT2.addEventListener('click', cerrarModalT2);
}



// Funciones para manejar el modal de Talla T3

const btnInfoT3 = document.getElementById('btnInfoT3');
const modalT3 = document.getElementById('modalT3');
const closeT3 = document.querySelector('.closeT3');
const btnCerrarModalT3 = document.getElementById('btnCerrarModalT3');

// Función para abrir el modal de Talla T3

if (btnInfoT3) {
    btnInfoT3.addEventListener('click', () => {
        modalT3.classList.remove('hidden'); // Muestra el modal
    });
}

// Función para cerrar el modal de Talla T3

const cerrarModalT3 = () => {
    modalT3.classList.add('hidden'); // Oculta el modal
};

// Añadir eventos para cerrar el modal de Talla T3

if (closeT3) {
    closeT3.addEventListener('click', cerrarModalT3);
}
if (btnCerrarModalT3) {
    btnCerrarModalT3.addEventListener('click', cerrarModalT3);
}


// Funciones para manejar el modal de Talla T4

const btnInfoT4 = document.getElementById('btnInfoT4');
const modalT4 = document.getElementById('modalT4');
const closeT4 = document.querySelector('.closeT4');
const btnCerrarModalT4 = document.getElementById('btnCerrarModalT4');

// Funciones para manejar el modal de Talla S

if (btnInfoT4) {
    btnInfoT4.addEventListener('click', () => {
        modalT4.classList.remove('hidden'); // Muestra el modal
    });
}

// Función para cerrar el modal de Talla T4

const cerrarModalT4 = () => {
    modalT4.classList.add('hidden'); // Oculta el modal
};

// Añadir eventos para cerrar el modal de Talla T4

if (closeT4) {
    closeT4.addEventListener('click', cerrarModalT4);
}
if (btnCerrarModalT4) {
    btnCerrarModalT4.addEventListener('click', cerrarModalT4);
}

// Cerrar el modal al hacer clic fuera de él (para todos los modales)
window.addEventListener('click', (event) => {
    if (event.target === modalV) {
        cerrarModalV();
    }
    if (event.target === modalV) {
        cerrarModalV();
    }
    if (event.target === modalC) {
        cerrarModalC();
    }
    if (event.target === modalR) {
        cerrarModalR();
    }
    if (event.target === modalB) {
        cerrarModalB();
    }
    if (event.target === modalOS) {
        cerrarModalOS();
    }
    if (event.target === modalA) {
        cerrarModalA();
    }
    if (event.target === modalT1) {
        cerrarModalT1();
    }
    if (event.target === modalT2) {
        cerrarModalT2();
    }
    if (event.target === modalT3) {
        cerrarModalT3();
    }
    if (event.target === modalT4) {
        cerrarModalT4();
    }
});

function openModal(modalId) {
    document.getElementById(modalId).style.display = "block";
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}

// Cerrar modal al hacer clic fuera del contenido
window.onclick = function (event) {
    const modals = document.querySelectorAll(".modal-nequi, .modal-davi");
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
};

