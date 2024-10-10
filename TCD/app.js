// Initialize cart array to store selected items
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Function to check if an item is in the cart
const isItemInCart = (itemName) => {
    return cart.some(item => item.name === itemName);
};

// Update the cart count in the navbar
const updateCartCount = () => {
    const cartCount = document.querySelector('.cart-count');
    cartCount.textContent = cart.length;
};

// Add to Cart button functionality
const addToCart = (dishName, dishPrice, button) => {
    const existingItem = cart.find(item => item.name === dishName);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ name: dishName, price: dishPrice, quantity: 1 });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();

    // Change button text and style if item added for the first time
    button.textContent = 'Go to Cart';
    button.style.backgroundColor = 'green';

    // Add an event listener to navigate to the cart page on button click
    button.addEventListener('click', () => {
        window.location.href = 'cart.html';
    });
};

// Navigate to cart page on clicking the cart icon
const cartIcon = document.querySelector('.cart-icon');
cartIcon.addEventListener('click', () => {
    window.location.href = 'cart.html';
});

// Load menu data and create "Add to Cart" buttons
document.addEventListener('DOMContentLoaded', () => {
    const menuContainer = document.getElementById('menu-container');

    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            data.menu.forEach(category => {
                const categoryBlock = document.createElement('div');
                categoryBlock.classList.add('category-block');
                
                const categoryTitle = document.createElement('h3');
                categoryTitle.textContent = category.category;
                categoryBlock.appendChild(categoryTitle);

                category.subcategories.forEach(subcategory => {
                    const subcategoryBlock = document.createElement('div');
                    subcategoryBlock.classList.add('subcategory-block');

                    const subcategoryTitle = document.createElement('h4');
                    subcategoryTitle.textContent = `${subcategory.name} (${subcategory.type})`;
                    subcategoryBlock.appendChild(subcategoryTitle);

                    const dishGrid = document.createElement('div');
                    dishGrid.classList.add('dish-grid');

                    subcategory.dishes.forEach(dish => {
                        const menuItem = document.createElement('div');
                        menuItem.classList.add('menu-item');

                        menuItem.innerHTML = `
                            <img src="${dish.image_url}" alt="${dish.name}">
                            <h5>${dish.name}</h5>
                            <p class="price">$${dish.price.toFixed(2)}</p>
                            <button class="add-to-cart-btn" data-name="${dish.name}" data-price="${dish.price}">
                                ${isItemInCart(dish.name) ? 'Go to Cart' : 'Add to Cart'}
                            </button>
                            `;
                        
                        // Add event listener to "Add to Cart" button
                        const addToCartButton = menuItem.querySelector('.add-to-cart-btn');

                        if (isItemInCart(dish.name)) {
                            addToCartButton.classList.add('added-to-cart'); // Add class if item is in cart
                        }

                        addToCartButton.addEventListener('click', () => {
                            // If item is already in cart, go to cart
                            if (cart.some(item => item.name === dish.name)) {
                                window.location.href = 'cart.html';
                            } else {
                                // Otherwise, add item to cart
                                addToCart(dish.name, dish.price, addToCartButton);
                            }
                        });

                        dishGrid.appendChild(menuItem);
                    });

                    subcategoryBlock.appendChild(dishGrid);
                    categoryBlock.appendChild(subcategoryBlock);
                });

                menuContainer.appendChild(categoryBlock);
            });

            // Update cart count on page load
            updateCartCount();
        });
});
// On the cart page
if (window.location.pathname.includes('cart.html')) {
    document.addEventListener('DOMContentLoaded', () => {
        const cartContainer = document.getElementById('cart-container');
        const cartTotalElement = document.getElementById('cart-total');
        const placeOrderBtn = document.querySelector('.place-order-btn');

        // Display cart items
        cart.forEach(item => {
            const cartItem = document.createElement('div');
            cartItem.classList.add('cart-item');

            cartItem.innerHTML = `
                <img src="https://example.com/images/default-item.jpg" alt="${item.name}">
                <div class="cart-item-info">
                    <h5>${item.name}</h5>
                    <p class="cart-item-price">$${item.price.toFixed(2)}</p>
                    <div class="cart-item-quantity">
                        <label for="quantity-${item.name}">Qty:</label>
                        <input type="number" id="quantity-${item.name}" value="${item.quantity}" min="1">
                    </div>
                </div>
            `;

            cartContainer.appendChild(cartItem);

            // Add event listener to quantity input
            const quantityInput = cartItem.querySelector(`#quantity-${item.name}`);
            quantityInput.addEventListener('change', (e) => {
                const newQuantity = parseInt(e.target.value);
                item.quantity = newQuantity;
                updateCartTotal();
            });
        });

        // Update total price when quantity changes
        function updateCartTotal() {
            const total = cart.reduce((acc, item) => acc + item.price * item.quantity, 0);
            cartTotalElement.textContent = `$${total.toFixed(2)}`;
        }

        // Place order button functionality
        placeOrderBtn.addEventListener('click', () => {
            alert('Order placed successfully!');
        });

        // Initial cart total
        updateCartTotal();
    });
}
