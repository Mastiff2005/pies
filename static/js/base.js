let cookie = document.cookie
let csrfToken = cookie.substring(cookie.indexOf('=') + 1)


function set_null(productID) {
	let count = document.getElementById(productID);
	count.innerHTML = 0;
}

function clear(productID) {
	let count = document.getElementById(productID);
	count.innerHTML = null;
}

function get_quantity(productID) {
    let count = document.getElementById(productID);
    count.innerHTML = 0;
    $.ajax({
	    	url: "/api/cart_view/",
	        method: 'GET',
	        success: function(data) {
	        	let arr = data["items"];
	        	let len= arr.length;
	            for (let number = 0; number < len; number++) {
	                if (data["items"][number]["id"] == productID) {
	                	count.innerHTML = data["items"][number]["quantity"];
	                }
	            }
	        }
	 });
}

function closeCart() {
document.getElementById("cart_popup").style.display = "none";
}

function openCart() {
    document.getElementById("cart_popup").style.display = "block";
    let cartView = document.getElementById("cart_popup");
    cartView.innerHTML = "<b><big>Ваша корзина</big></b><br><br>"
    $.ajax({
        url: "/api/cart_view/",
        method: 'GET',
        success: function(data) {
            let arr = data["items"];
            let len= arr.length;
            for (let number = 0; number < len; number++) {
                cartView.innerHTML += data["items"][number]["name"] + " -- ";
                cartView.innerHTML += data["items"][number]["quantity"] + "шт. -- ";
                cartView.innerHTML += data["items"][number]["price"] + " руб.<br>";
            }
            cartView.innerHTML += "<br>";
            let quantity = data["quantity"];
            if ((quantity % 10) == 1 && (![11, 111].includes(quantity))) {
            	cartView.innerHTML += "<b>" + data["quantity"] + " позиция,</b>";
            }
            else if (([2, 3, 4].includes(quantity % 10)) && (![12, 13, 14, 112, 113, 114].includes(quantity))) {
            	cartView.innerHTML += "<b>" + data["quantity"] + " позиции,</b>";
            }
            else {
            	cartView.innerHTML += "<b>" + data["quantity"] + " позиций,</b>";
            }
            cartView.innerHTML += "<b> на сумму " + data["total_price"] + " руб.</b><br><br>";
            cartView.innerHTML += "<a href='/cart'><button class='btn btn-outline-primary' style='width: 170px'>Перейти в корзину</button></a>&nbsp;";
            cartView.innerHTML += "<button class='btn btn-outline-primary' onclick='closeCart()'>Закрыть</button>";
        }
    });
}

function add_ident(productID) {
	let ident = document.getElementById(productID + "ident");
    ident.innerHTML = "--- В корзине ---";
}

function remove_ident(productID) {
	let ident = document.getElementById(productID + "ident");
    ident.innerHTML = null;
}


function add_product(productID, quantity, update) {
    // Добавляем продукт в корзину
    let count = document.getElementById(productID);
    let clicks = parseInt(count.innerHTML);
    clicks += 1;
    $.ajax({
        url: "/cart/add/" + productID + '/',
        method: 'POST',
        headers: {'X-CSRFToken': csrfToken},
        data: {"quantity": quantity, "update": update},
        success: function(data) {
            console.log(data);
        }
    });
    count.innerHTML = clicks;
    // Выводим сумму товаров в корзине и меняем отображение корзины
    let cartSum = document.getElementById("cartSum");
    let cartImg = document.getElementById("cartImg");
    let cartView = document.getElementById("cart_popup");
    setTimeout(() => {
        $.ajax({
            url: "/api/cart_view/",
            method: 'GET',
            success: function(data) {
                cartSum.innerHTML = data["total_price"] + " руб.";
                cartImg.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-cart-fill" viewBox="0 0 16 16"><path d="M0 1.5A.5.5 0 0 1 .5 1H2a.5.5 0 0 1 .485.379L2.89 3H14.5a.5.5 0 0 1 .491.592l-1.5 8A.5.5 0 0 1 13 12H4a.5.5 0 0 1-.491-.408L2.01 3.607 1.61 2H.5a.5.5 0 0 1-.5-.5zM5 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm-7 1a1 1 0 1 1 0 2 1 1 0 0 1 0-2zm7 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>';
                cartView.innerHTML = "<b><big>Ваша корзина</big></b><br><br>"
                let arr = data["items"];
	            let len= arr.length;
	            for (let number = 0; number < len; number++) {
	                cartView.innerHTML += data["items"][number]["name"] + " -- ";
	                cartView.innerHTML += data["items"][number]["quantity"] + "шт. -- ";
	                cartView.innerHTML += data["items"][number]["price"] + " руб.<br>";
	            }
	            cartView.innerHTML += "<br>";
	            let quantity = data["quantity"];
	            if ((quantity % 10) == 1 && (![11, 111].includes(quantity))) {
	            	cartView.innerHTML += "<b>" + data["quantity"] + " позиция,</b>";
	            }
	            else if (([2, 3, 4].includes(quantity % 10)) && (![12, 13, 14, 112, 113, 114].includes(quantity))) {
	            	cartView.innerHTML += "<b>" + data["quantity"] + " позиции,</b>";
	            }
	            else {
	            	cartView.innerHTML += "<b>" + data["quantity"] + " позиций,</b>";
	            }
	            cartView.innerHTML += "<b> на сумму " + data["total_price"] + " руб.</b><br><br>";
	            cartView.innerHTML += "<a href='/cart'><button class='btn btn-outline-primary' style='width: 170px'>Перейти в корзину</button></a>&nbsp;";
	            cartView.innerHTML += "<button class='btn btn-outline-primary' onclick='closeCart()'>Закрыть</button>";
            }
        });
    }, 100);

}

function remove_product(productID, quantity, update) {
    // Убираем продукт из корзины
    let count = document.getElementById(productID);
    let clicks = parseInt(count.innerHTML);
    clicks = 0;
    $.ajax({
        url: "/cart/remove/" + productID + '/',
        method: 'POST',
        headers: {'X-CSRFToken': csrfToken},
        data: {"quantity": quantity, "update": update},
        success: function(data) {
            console.log(data);
        }
    });
    count.innerHTML = clicks;
    // Выводим сумму товаров в корзине
    let cartSum = document.getElementById("cartSum");
    let cartImg = document.getElementById("cartImg");
    let cartView = document.getElementById("cart_popup");
    setTimeout(() => {
        $.ajax({
            url: "/api/cart_view/",
            method: 'GET',
            success: function(data) {
                cartSum.innerHTML = data["total_price"] + " руб.";
                if (data["total_price"] == 0) {
                    cartImg.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-cart" viewBox="0 0 16 16"><path d="M0 1.5A.5.5 0 0 1 .5 1H2a.5.5 0 0 1 .485.379L2.89 3H14.5a.5.5 0 0 1 .491.592l-1.5 8A.5.5 0 0 1 13 12H4a.5.5 0 0 1-.491-.408L2.01 3.607 1.61 2H.5a.5.5 0 0 1-.5-.5zM3.102 4l1.313 7h8.17l1.313-7H3.102zM5 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm-7 1a1 1 0 1 1 0 2 1 1 0 0 1 0-2zm7 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>';
                }
                cartView.innerHTML = "<b><big>Ваша корзина</big></b><br><br>"
                let arr = data["items"];
	            let len= arr.length;
	            for (let number = 0; number < len; number++) {
	                cartView.innerHTML += data["items"][number]["name"] + " -- ";
	                cartView.innerHTML += data["items"][number]["quantity"] + "шт. -- ";
	                cartView.innerHTML += data["items"][number]["price"] + " руб.<br>";
	            }
	            cartView.innerHTML += "<br>";
	            let quantity = data["quantity"];
	            if ((quantity % 10) == 1 && (![11, 111].includes(quantity))) {
	            	cartView.innerHTML += "<b>" + data["quantity"] + " позиция,</b>";
	            }
	            else if (([2, 3, 4].includes(quantity % 10)) && (![12, 13, 14, 112, 113, 114].includes(quantity))) {
	            	cartView.innerHTML += "<b>" + data["quantity"] + " позиции,</b>";
	            }
	            else {
	            	cartView.innerHTML += "<b>" + data["quantity"] + " позиций,</b>";
	            }
	            cartView.innerHTML += "<b> на сумму " + data["total_price"] + " руб.</b><br><br>";
	            cartView.innerHTML += "<a href='/cart'><button class='btn btn-outline-primary' style='width: 170px'>Перейти в корзину</button></a>&nbsp;";
	            cartView.innerHTML += "<button class='btn btn-outline-primary' onclick='closeCart()'>Закрыть</button>";
            }
        });
    }, 100);
}