const productDatabase = {
    'coca-cola': {
        name: 'Coca-Cola',
        category: 'Напитки',
        rating: 2.4,
        isBoycotted: true,
        isKyrgyzProduct: false,
        boycottReason: 'Продолжение работы в России после вторжения в Украину',
        description: 'Coca-Cola - газированный безалкогольный напиток, производимый компанией The Coca-Cola Company.',
        alternativeProducts: [
            {
                name: 'Шоро Cola',
                rating: 4.5,
                isKyrgyzProduct: true
            },
            {
                name: 'Pepsi',
                rating: 3.8,
                isKyrgyzProduct: false
            },
            {
                name: 'Royal Crown Cola',
                rating: 4.0,
                isKyrgyzProduct: false
            },
            {
                name: 'Alatoo Cola',
                rating: 3.9,
                isKyrgyzProduct: true
            }
        ]
    },
    'nestle': {
        name: 'Nestle',
        category: 'Продукты питания',
        rating: 1.8,
        isBoycotted: true,
        isKyrgyzProduct: false,
        boycottReason: 'Эксплуатация водных ресурсов и продолжение работы в России',
        description: 'Nestle - швейцарская транснациональная корпорация, производитель продуктов питания.',
        alternativeProducts: [
            {
                name: 'Байтик',
                rating: 4.7,
                isKyrgyzProduct: true
            },
            {
                name: 'Arla Foods',
                rating: 4.2,
                isKyrgyzProduct: false
            }
        ]
    }
};

// Функция для создания карточки продукта
function createProductCard(product) {
    const statusClass = product.isBoycotted ? 'status-boycotted' : 'status-ok';
    const statusText = product.isBoycotted ? 'Бойкотируется' : 'Этичный выбор';

    const alternativesHTML = product.alternativeProducts.map(alt => {
        const localBadge = alt.isKyrgyzProduct ?
            `<div class="status-local" style="margin-left: 5px; font-size: 10px;">KG</div>` : '';

        return `
                <div class="alternative-item" onclick="showAlternativeModal('${alt.name}', '${alt.rating}', '${alt.isKyrgyzProduct}')">
                    <img src="/api/placeholder/120/80" alt="${alt.name}" class="alternative-image">
                    <div class="alternative-info">
                        <div class="alternative-name">${alt.name}</div>
                        <div class="alternative-rating">
                            <span class="rating-star">★</span> ${alt.rating}
                            ${localBadge}
                        </div>
                    </div>
                </div>
                `;
    }).join('');

    const boycottReasonHTML = product.isBoycotted ?
        `<div class="product-reason"><strong>Причина:</strong> ${product.boycottReason}</div>` : '';

    return `
            <div class="product-card">
                <div class="product-header">
                    <img src="/api/placeholder/50/50" alt="${product.name}" class="product-logo">
                    <div class="product-title">
                        <div class="product-name">${product.name}</div>
                        <div class="product-category">Категория: ${product.category}</div>
                    </div>
                    <div class="product-rating">
                        <span class="rating-star">★</span> ${product.rating}
                    </div>
                </div>
                <div class="product-body">
                    <div class="product-status ${statusClass}">${statusText}</div>
                    ${boycottReasonHTML}
                    <div class="product-description">
                        ${product.description}
                    </div>

                    <div class="alternatives-title">Этичные альтернативы:</div>
                    <div class="alternatives-list">
                        ${alternativesHTML}
                    </div>
                </div>
            </div>
            `;
}

// Добавление сообщения в чат
function addMessage(content, isUser) {
    const chatMessages = document.querySelector('.chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user-message' : 'ai-message');
    messageDiv.innerHTML = content;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function searchProduct(query) {
    console.log("Отправляем запрос:", query);
    fetch('http://localhost:8000/assistant/search-product/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({query})
    })
        .catch(err => {
            console.error("Ошибка запроса:", err);
            addMessage("Произошла ошибка при получении ответа.", false);
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                addMessage(data.html + "<br>Хотите узнать подробнее о каком-то конкретном продукте?", false);
            } else {
                addMessage(data.html, false);
            }
        })
        .catch(err => {
            addMessage("Произошла ошибка при получении ответа.", false);
        });
}

// Обработчик отправки сообщения
document.querySelector('.chat-input button').addEventListener('click', function () {
    const input = document.querySelector('.chat-input input');
    const message = input.value.trim();

    if (message) {
        addMessage(message, true);
        input.value = '';

        // Имитация загрузки (в реальном приложении здесь был бы запрос к API)
        setTimeout(function () {
            searchProduct(message);
        }, 500);
    }
});

// Обработка нажатия Enter для отправки сообщения
document.querySelector('.chat-input input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        document.querySelector('.chat-input button').click();
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Проверяем совпадение имени
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showAlternativeModal(name, rating, isKyrgyzProduct, category, description, isBoycotted, boycottReason) {
    document.getElementById("modal-alt-name").innerText = name;
    document.getElementById("modal-alt-rating").innerText = rating;
    document.getElementById("modal-alt-country").innerText = isKyrgyzProduct === "True" ? "Кыргызстан" : "Зарубежный";
    document.getElementById("modal-alt-category").innerText = category;
    document.getElementById("modal-alt-description").innerText = description;
    document.getElementById("modal-alt-status").innerText = isBoycotted === "True" ? "Бойкотируется" : "Этичный выбор";
    document.getElementById("modal-alt-reason").innerText = boycottReason || "—";

    document.getElementById("alternative-modal").style.display = "block";
}

function closeModal() {
    document.getElementById("alternative-modal").style.display = "none";
}

function searchAlternative() {
    const name = document.getElementById("modal-alt-name").innerText;
    closeModal();

    // Имитируем поиск как обычный ввод
    addMessage(name, true);
    setTimeout(() => {
        searchProduct(name);
    }, 300);
}