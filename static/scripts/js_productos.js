document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/carrito');
        const carritoData = await response.json();
        actualizarCarritoUI(carritoData);
    } catch (err) {
        console.error('Error al cargar el carrito:', err);
        actualizarCarritoUI({});
    }
});

async function agregarAlCarrito(productoId) {
    try {
        const response = await fetch('/api/carrito/agregar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: productoId })
        });
        const data = await response.json();
        if (data.carrito) {
            actualizarCarritoUI(data.carrito);
        }
    } catch (err) {
        console.error('Error al agregar:', err);
    }
}

async function eliminarDelCarrito(productoId) {
    try {
        const response = await fetch('/api/carrito/eliminar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: productoId })
        });
        const data = await response.json();
        if (data.carrito !== undefined) {
            actualizarCarritoUI(data.carrito);
        }
    } catch (err) {
        console.error('Error al eliminar:', err);
    }
}

async function comprarCarrito() {
    try {
        const response = await fetch('/api/carrito/comprar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();
        alert(data.mensaje);
        actualizarCarritoUI({});
    } catch (err) {
        console.error('Error al comprar:', err);
    }
}

function actualizarCarritoUI(carritoData) {
    const container = document.getElementById('carrito-items');
    const vacioMsg = document.getElementById('carrito-vacio');
    const items = Object.values(carritoData);

    if (items.length === 0) {
        container.style.display = 'none';
        vacioMsg.style.display = 'block';
        container.innerHTML = '';
        return;
    }

    vacioMsg.style.display = 'none';
    container.style.display = 'block';

    let total = 0;
    let html = '';

    items.forEach(item => {
        const subtotal = item.precio * item.cantidad;
        total += subtotal;
        html += `
            <div class="carrito-item">
                <span>${item.nombre} <em>×${item.cantidad}</em></span>
                <span class="item-total">S/ ${subtotal.toFixed(2)}</span>
                <button onclick="eliminarDelCarrito(${item.id})" title="Quitar uno">✕</button>
            </div>
        `;
    });

    html += `
        <div class="carrito-total">
            <span>Total</span>
            <span>S/ ${total.toFixed(2)}</span>
        </div>
        <button id="btn-comprar" class="btn-comprar" onclick="comprarCarrito()">
            Confirmar compra
        </button>
    `;

    container.innerHTML = html;
}