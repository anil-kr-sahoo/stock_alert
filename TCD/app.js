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
const addToCart = (dishName, dishPrice, src, button) => {
    const existingItem = cart.find(item => item.name === dishName);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ name: dishName, price: dishPrice, quantity: 1, image_src: src});
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

// Function to scroll to the category
const scrollToCategory = (categoryId) => {
    const categoryElement = document.getElementById(categoryId);
    if (categoryElement) {
        categoryElement.scrollIntoView({ behavior: 'smooth' });
    }
};

// Load menu data and create "Add to Cart" buttons
document.addEventListener('DOMContentLoaded', () => {
    const menuContainer = document.getElementById('menu-container');
    const shortcutsContainer = document.querySelector('.shortcuts-grid'); // Get the shortcuts container

    // Load checkbox states from localStorage
    const onlyVegCheckbox = document.getElementById('vegFilter');
    const onlyNonVegCheckbox = document.getElementById('nonVegFilter');
    onlyVegCheckbox.checked = localStorage.getItem('onlyVeg') === 'true';
    onlyNonVegCheckbox.checked = localStorage.getItem('onlyNonVeg') === 'true';

    const renderMenu = () => {
        menuContainer.innerHTML = ''; // Clear previous content
        fetch('data.json')
            .then(response => response.json())
            .then(data => {
                // Reset shortcuts
                shortcutsContainer.innerHTML = '';

                // Create shortcut links based on categories
                data.menu.forEach(category => {
                    const shortcutCard = document.createElement('div');
                    shortcutCard.classList.add('shortcut-card');
                    const shortcutLink = document.createElement('a');
                    shortcutLink.href = `#${category.category}`; // Link to the category ID
                    shortcutLink.className = 'shortcut';
                    shortcutLink.textContent = category.category; // Set link text
                    shortcutCard.appendChild(shortcutLink);
                    shortcutsContainer.appendChild(shortcutCard); // Append to shortcuts container
                });

                // Render categories and dishes
                data.menu.forEach(category => {
                    const categoryBlock = document.createElement('div');
                    categoryBlock.classList.add('category-block');
                    categoryBlock.id = category.category; // Set ID for scrolling

                    const categoryTitle = document.createElement('h3');
                    categoryTitle.textContent = category.category;
                    categoryBlock.appendChild(categoryTitle);

                    let hasVisibleDishes = false; // Track if there are visible dishes in this category

                    category.subcategories.forEach(subcategory => {
                        const subcategoryBlock = document.createElement('div');
                        subcategoryBlock.classList.add('subcategory-block');

                        const subcategoryTitle = document.createElement('h4');
                        subcategoryTitle.textContent = subcategory.name
                            ? `${subcategory.name} (${subcategory.type})`
                            : ''; // Set subcategory name and type, if available
                        subcategoryBlock.appendChild(subcategoryTitle);

                        const dishGrid = document.createElement('div');
                        dishGrid.classList.add('dish-grid');

                        subcategory.dishes.forEach(dish => {
                            // Filter logic: Show items with no subcategory type or based on filters
                            if ((onlyVegCheckbox.checked && onlyNonVegCheckbox.checked) ||
                            (!onlyVegCheckbox.checked && !onlyNonVegCheckbox.checked)) {
                            // Both checkboxes are checked (or none), show all items
                            } else if (onlyVegCheckbox.checked && subcategory.type !== 'Veg' && subcategory.type) {
                            return; // Filter out non-Veg items if Veg is checked
                            } else if (onlyNonVegCheckbox.checked && subcategory.type !== 'NonVeg' && subcategory.type) {
                            return; // Filter out Veg items if Non-Veg is checked
                            }


                            const menuItem = document.createElement('div');
                            menuItem.classList.add('menu-item');

                            menuItem.innerHTML = `
                                <div class="menu-item-container" style="text-align: center;">
                                    <img src="${dish.image_url}" alt="${dish.name}" style="width: 150px; height: 150px; object-fit: cover; border-radius: 8px; display: block; margin: 0 auto 10px auto;">
                                    <h5 style="margin-top: 10px;">${dish.name}</h5>
                                    <p class="price">₹${dish.price.toFixed(2)}/-</p>
                                    <button class="add-to-cart-btn" data-name="${dish.name}" data-price="${dish.price}">
                                        ${isItemInCart(dish.name) ? 'Go to Cart' : 'Add to Cart'}
                                    </button>
                                </div>
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
                                    addToCart(dish.name, dish.price, dish.image_url, addToCartButton);
                                }
                            });

                            dishGrid.appendChild(menuItem);
                            hasVisibleDishes = true; // Mark that there's at least one visible dish
                        });

                        if (dishGrid.children.length > 0) {
                            subcategoryBlock.appendChild(dishGrid);
                            categoryBlock.appendChild(subcategoryBlock);
                        }
                    });

                    if (hasVisibleDishes) {
                        menuContainer.appendChild(categoryBlock); // Only append if there are visible dishes
                    }
                });

                // Update cart count on page load
                updateCartCount();
            });
    };

    renderMenu(); // Initial render of menu

    // Setup filter functionality
    const saveCheckboxState = () => {
        localStorage.setItem('onlyVeg', onlyVegCheckbox.checked);
        localStorage.setItem('onlyNonVeg', onlyNonVegCheckbox.checked);
        renderMenu(); // Re-render menu when checkbox state changes
    };

    onlyVegCheckbox.addEventListener('change', saveCheckboxState);
    onlyNonVegCheckbox.addEventListener('change', saveCheckboxState);

    // Setup shortcut navigation
    const shortcuts = document.querySelectorAll('.shortcut');
    shortcuts.forEach(shortcut => {
        shortcut.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent default link behavior
            scrollToCategory(shortcut.textContent); // Scroll to the category
        });
    });
});
