// app/views/static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers de Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-cierre de alertas después de 5 segundos
    setTimeout(function() {
        document.querySelectorAll('.alert').forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Controladores para botones de cantidad en el carrito
    setupQuantityControls();

    // Validación de formularios
    setupFormValidation();
});

/**
 * Configurar los controles de cantidad en el carrito
 */
function setupQuantityControls() {
    // Botones de incremento/decremento de cantidad
    const decrementButtons = document.querySelectorAll('.decrement-quantity');
    const incrementButtons = document.querySelectorAll('.increment-quantity');
    
    decrementButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.nextElementSibling;
            const value = parseInt(input.value, 10);
            if (value > 1) {
                input.value = value - 1;
            }
        });
    });
    
    incrementButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const value = parseInt(input.value, 10);
            if (value < 10) {
                input.value = value + 1;
            }
        });
    });
}

/**
 * Configurar validación de formularios
 */
function setupFormValidation() {
    // Obtener todos los formularios a los que queremos aplicar estilos de validación de Bootstrap
    const forms = document.querySelectorAll('.needs-validation');
    
    // Bucle sobre ellos y prevenir envío si no son válidos
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Función para mostrar estrellas de valoración basadas en un valor numérico
 * @param {number} rating - Valoración del 0 al 5
 * @param {string} containerId - ID del contenedor donde mostrar las estrellas
 */
function showStarRating(rating, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = '';
    
    // Redondeamos a media estrella más cercana
    const roundedRating = Math.round(rating * 2) / 2;
    
    for (let i = 1; i <= 5; i++) {
        const star = document.createElement('i');
        
        if (i <= roundedRating) {
            star.className = 'bi bi-star-fill';
        } else if (i - 0.5 === roundedRating) {
            star.className = 'bi bi-star-half';
        } else {
            star.className = 'bi bi-star';
        }
        
        container.appendChild(star);
    }
}

/**
 * Función para actualizar automáticamente el subtotal en el carrito
 * cuando se cambia la cantidad
 */
function updateSubtotal() {
    const quantityInputs = document.querySelectorAll('input[name^="quantity_"]');
    
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const itemId = this.name.split('_')[1];
            const quantity = parseInt(this.value, 10);
            const price = parseFloat(document.getElementById(`price_${itemId}`).textContent);
            const subtotalElement = document.getElementById(`subtotal_${itemId}`);
            
            if (subtotalElement) {
                const subtotal = (price * quantity).toFixed(2);
                subtotalElement.textContent = `$${subtotal}`;
            }
            
            // Actualizar el total
            updateTotal();
        });
    });
}

/**
 * Función para actualizar el total en el carrito
 */
function updateTotal() {
    const subtotalElements = document.querySelectorAll('[id^="subtotal_"]');
    let total = 0;
    
    subtotalElements.forEach(element => {
        const value = parseFloat(element.textContent.replace('$', ''));
        total += value;
    });
    
    const deliveryFee = parseFloat(document.getElementById('delivery-fee').textContent.replace('$', ''));
    const totalElement = document.getElementById('total-amount');
    
    if (totalElement) {
        totalElement.textContent = `$${(total + deliveryFee).toFixed(2)}`;
    }
}

/**
 * Función para confirmar eliminación de elementos
 * @param {string} message - Mensaje de confirmación
 * @returns {boolean} - Verdadero si el usuario confirma, falso en caso contrario
 */
function confirmDelete(message) {
    return confirm(message || '¿Estás seguro de que deseas eliminar este elemento?');
}

/**
 * Función para mostrar modal de dirección de entrega
 */
function showAddressModal() {
    const addressModal = new bootstrap.Modal(document.getElementById('addressModal'));
    addressModal.show();
}

/**
 * Función para recargar página después de un tiempo determinado
 * Útil para seguimiento de pedidos en tiempo real
 * @param {number} seconds - Segundos antes de recargar
 */
function autoReload(seconds) {
    setTimeout(function() {
        location.reload();
    }, seconds * 1000);
}