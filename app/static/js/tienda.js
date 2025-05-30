// ----------------- Menú Toggle -----------------
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const wrapper = document.getElementById('wrapper');
    if(menuToggle && wrapper) {
        menuToggle.addEventListener('click', function() {
            wrapper.classList.toggle('active');
        });
    }
    // Calculadora toggle si lo tienes
    const calcToggle = document.getElementById('calculadora-toggle');
    const calculadora = document.getElementById('calculadora');
    if(calcToggle && calculadora) {
        calcToggle.addEventListener('click', function() {
            calculadora.classList.toggle('active');
        });
    }
});

// ----------------- Carrito de Compras -----------------
let carrito = [];
let total = 0;

function agregarAlCarrito(categoria) {
    const checkboxes = document.querySelectorAll(`#${categoria} input[type="checkbox"]:checked`);
    if (checkboxes.length > 0) {
        alert(`Has agregado ${checkboxes.length} producto(s) de ${categoria} al carrito.`);
    } else {
        alert(`Por favor, selecciona al menos un producto de ${categoria}.`);
    }
    checkboxes.forEach(checkbox => {
        const producto = checkbox.getAttribute('data-producto');
        const precio = parseFloat(checkbox.getAttribute('data-precio'));
        const item = { producto, precio, cantidad: 1 };
        const existe = carrito.find(item => item.producto === producto);
        if (existe) {
            existe.cantidad += 1;
        } else {
            carrito.push(item);
        }
        total += precio;
        checkbox.checked = false;
    });
    actualizarCarrito();
}

function actualizarCarrito() {
    const listaCarrito = document.getElementById('lista-carrito');
    const totalCarrito = document.getElementById('total-carrito');
    if(listaCarrito) listaCarrito.innerHTML = '';
    carrito.forEach(item => {
        const li = document.createElement('li');
        li.innerHTML = `
          <div class="producto-info">${item.producto} - $${item.precio.toFixed(2)}</div>
          <div class="cantidad-control">
            <button onclick="cambiarCantidad('${item.producto}', -1)">-</button>
            <span>${item.cantidad}</span>
            <button onclick="cambiarCantidad('${item.producto}', 1)">+</button>
          </div>
        `;
        if(listaCarrito) listaCarrito.appendChild(li);
    });
    if(totalCarrito) totalCarrito.textContent = `$${total.toFixed(2)}`;
}

// window global para onclick desde HTML
window.cambiarCantidad = function(producto, cambio) {
    const item = carrito.find(item => item.producto === producto);
    if (item) {
        item.cantidad += cambio;
        total += cambio * item.precio;
        if (item.cantidad <= 0) {
            carrito = carrito.filter(item => item.producto !== producto);
        }
        actualizarCarrito();
    }
};

// ----------------- Pagar -----------------
searchBtn.addEventListener("click", function() {
    if(carrito.length === 0) {
        alert("¡El carrito está vacío!");
        return;
    }
    fetch('/comprar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ carrito: carrito, total: total.toFixed(2) })
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            alert('¡Compra realizada con éxito!');
            carrito = [];
            total = 0;
            actualizarCarrito();
            // Redirige usando la URL recibida
            window.location.href = data.redirect_url;
        } else {
            alert('Error: ' + (data.error || 'No se pudo completar la compra.'));
        }
    })
    .catch(err => alert('Error de conexión: ' + err));
});

