// Retrieve the cart from localStorage
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Render the cart items on the cart page
const renderCartItems = () => {
    const cartItemsContainer = document.getElementById('cart-items');
    cartItemsContainer.innerHTML = ''; // Clear the container before rendering

    cart.forEach((item, index) => {
        const cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');

        cartItem.innerHTML = `
            <img src="https://example.com/dummy.jpg" alt="${item.name}">
            <div class="cart-item-info">
                <h5>${item.name}</h5>
                <p class="cart-item-price">$${item.price.toFixed(2)}</p>
            </div>
            <div class="cart-item-quantity">
                <button class="decrease-quantity" data-index="${index}">-</button>
                <span class="quantity">${item.quantity}</span>
                <button class="increase-quantity" data-index="${index}">+</button>
            </div>
            <button class="delete-item" data-index="${index}">🗑️</button>
        `;

        // Append event listeners for increase, decrease, and delete buttons
        cartItem.querySelector('.increase-quantity').addEventListener('click', () => {
            item.quantity += 1;
            updateCartStorage();
            renderCartItems(); // Re-render cart items to reflect changes
        });

        cartItem.querySelector('.decrease-quantity').addEventListener('click', () => {
            if (item.quantity > 1) {
                item.quantity -= 1;
                updateCartStorage();
                renderCartItems(); // Re-render cart items to reflect changes
            }
        });

        cartItem.querySelector('.delete-item').addEventListener('click', () => {
            cart.splice(index, 1); // Remove item from cart
            updateCartStorage();
            renderCartItems(); // Re-render cart items to reflect changes
        });

        cartItemsContainer.appendChild(cartItem);
    });

    updateTotalPrice();
};

// Update the total price dynamically
const updateTotalPrice = () => {
    let totalPrice = 0;

    cart.forEach(item => {
        totalPrice += item.price * item.quantity;
    });

    document.getElementById('cart-total').textContent = totalPrice.toFixed(2);
};

// Update session storage whenever cart changes
const updateCartStorage = () => {
    localStorage.setItem('cart', JSON.stringify(cart));
};

// Load the cart items when the cart page is opened
document.addEventListener('DOMContentLoaded', () => {
    renderCartItems();
});
