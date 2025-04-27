let cart = JSON.parse(localStorage.getItem('cart')) || [];

function loadCart() {
    let cartList = document.getElementById('cart-items');
    let totalElement = document.getElementById('cart-total');
    cartList.innerHTML = '';
    let total = 0;

    cart.forEach(item => {
        let li = document.createElement('li');
        li.innerText = `${item.name} - ${item.price}₸`;
        cartList.appendChild(li);
        total += item.price;
    });

    totalElement.innerText = total;
}

function clearCart() {
    localStorage.removeItem('cart');
    cart = [];
    loadCart();
}

function goToHome() {
    window.location.href = 'index.html';
}

function showCreditOptions() {
    document.getElementById('credit-options').classList.toggle('hidden');
}

function calculateCredit(months) {
    let total = parseInt(document.getElementById('cart-total').innerText);
    let percent = months * 0.01;
    let finalSum = total + (total * percent);
    let monthlyPayment = (finalSum / months).toFixed(2);

    let creditResult = document.getElementById('credit-result');
    creditResult.innerHTML =
        `Вы выбрали ${months} месяцев. Итоговая сумма: ${finalSum}₸. Ежемесячный платеж: ${monthlyPayment}₸.` +
        `<br><button onclick="confirmCreditPurchase()" class="credit-confirm-btn">Оформить кредит</button>`;
}

function confirmCreditPurchase() {
    alert('Поздравляем с покупкой в кредит! Спасибо, что выбрали наш магазин.');
    clearCart();
}

function addToCart(button) {
    let product = button.parentElement;
    let name = product.querySelector('h3').innerText;
    let price = parseInt(product.querySelector('.price').innerText);

    cart.push({ name, price });
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}

function openDownloadModal(button) {
    let product = button.closest('.product');
    let img = product.querySelector('img');
    let imgUrl = img.src;
    let fileName = imgUrl.split('/').pop();

    document.getElementById('download-path').value = `Файл будет загружен в папку, указанную в настройках браузера`;
    document.getElementById('download-modal').dataset.imgUrl = imgUrl;
    document.getElementById('download-modal').dataset.fileName = fileName;
    document.getElementById('download-modal').style.display = 'flex';
}

function downloadImage() {
    let modal = document.getElementById('download-modal');
    let imgUrl = modal.dataset.imgUrl;
    let fileName = modal.dataset.fileName;

    let a = document.createElement("a");
    a.href = imgUrl;
    a.setAttribute("download", fileName);
    a.click();

    modal.style.display = 'none';
}

function closeDownloadModal() {
    document.getElementById('download-modal').style.display = 'none';
}

function updateCartCount() {
    document.getElementById('cart-count').innerText = cart.length;
}

function goToCart() {
    window.location.href = 'catalog.html';
}

document.addEventListener("DOMContentLoaded", () => {
    loadCart();
    updateCartCount();
    document.querySelector('.checkout-btn').addEventListener('click', processPayment);

    localStorage.removeItem("username");
    document.getElementById("welcome-modal").style.display = "flex";
});

function saveUserData() {
    let name = document.getElementById("username").value.trim();
    let age = document.getElementById("age").value.trim();

    if (name && age) {
        document.getElementById("welcome-modal").style.display = "none";
        showWelcomeMessage(name);
    } else {
        alert("Пожалуйста, введите имя и возраст!");
    }
}

function showWelcomeMessage(name) {
    let messageBox = document.getElementById("welcome-message");
    messageBox.innerText = `Добро пожаловать, ${name}!`;
    messageBox.style.display = "block";
}
