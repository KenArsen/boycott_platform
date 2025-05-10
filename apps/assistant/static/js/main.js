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


// Функция для отображения модального окна с информацией о продукте
function showAlternativeModal(name, image, rating, isKyrgyzProduct, category, description, isBoycotted, boycottReason) {
    // Установка основной информации
    document.getElementById("modal-alt-name").innerText = name;
    document.getElementById("modal-alt-rating").innerText = rating;
    document.getElementById("modal-alt-category").innerText = category || "Неизвестно";
    document.getElementById("modal-alt-description").innerText = description || "Информация отсутствует";

    // Установка изображения (добавлено)
    const imageElement = document.getElementById("modal-alt-image");
    if (image && image !== 'undefined' && !image.includes('undefined')) {
        imageElement.src = image;
    } else {
        imageElement.src = "/api/placeholder/200/150"; // Запасное изображение
    }

    // Установка статуса продукта (бойкотируется или этичный)
    const statusBadge = document.getElementById("modal-alt-status-badge");
    const statusText = document.getElementById("modal-alt-status");

    if (isBoycotted === "True") {
        statusBadge.className = "modal-status boycotted";
        statusText.innerText = "Бойкотируется";

        // Показываем причину бойкота
        const reasonContainer = document.getElementById("modal-alt-reason-container");
        document.getElementById("modal-alt-reason").innerText = boycottReason || "Причина не указана";
        reasonContainer.classList.remove("modal-reason-hidden");
    } else {
        statusBadge.className = "modal-status ethical";
        statusText.innerText = "Этичный выбор";

        // Скрываем причину бойкота
        document.getElementById("modal-alt-reason-container").classList.add("modal-reason-hidden");
    }

    // Установка информации о стране производства
    const countryBadge = document.getElementById("modal-alt-country-badge");
    const countryText = document.getElementById("modal-alt-country");

    if (isKyrgyzProduct === "True") {
        countryBadge.style.backgroundColor = "#e3f2fd";
        countryBadge.style.color = "#1565c0";
        countryText.innerText = "Кыргызстан";
    } else {
        countryBadge.style.backgroundColor = "#f0f0f0";
        countryBadge.style.color = "#666";
        countryText.innerText = "Зарубежный";
    }

    // Показываем модальное окно с плавной анимацией
    const modal = document.getElementById("alternative-modal");
    modal.style.display = "block";

    // Добавляем обработчик для закрытия по клику вне содержимого
    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    // Добавляем обработчик для закрытия по Escape
    document.addEventListener("keydown", handleEscKey);
}

// Функция закрытия модального окна
function closeModal() {
    const modal = document.getElementById("alternative-modal");

    // Плавное скрытие
    modal.style.opacity = "0";

    setTimeout(() => {
        modal.style.display = "none";
        modal.style.opacity = "1";
    }, 300);

    // Удаляем обработчик Escape
    document.removeEventListener("keydown", handleEscKey);
}

// Обработчик нажатия клавиши Escape
function handleEscKey(event) {
    if (event.key === "Escape") {
        closeModal();
    }
}

// Функция поиска альтернативного продукта
function searchAlternative() {
    const name = document.getElementById("modal-alt-name").innerText;
    closeModal();

    // Имитируем поиск как обычный ввод с небольшой задержкой
    addMessage(name, true);

    // Добавляем индикатор загрузки
    const chatMessages = document.querySelector('.chat-messages');
    const loadingDiv = document.createElement('div');
    loadingDiv.classList.add('message', 'ai-message');
    loadingDiv.innerHTML = '<div style="display: flex; align-items: center;"><span style="margin-right: 10px;">Поиск</span><div class="loading-dots"><span>.</span><span>.</span><span>.</span></div></div>';
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Выполняем поиск
    setTimeout(() => {
        chatMessages.removeChild(loadingDiv);
        searchProduct(name);
    }, 800);
}

// Стили для анимации загрузки
document.head.insertAdjacentHTML('beforeend', `
<style>
    .loading-dots {
        display: inline-flex;
    }
    
    .loading-dots span {
        animation: loadingDots 1.4s infinite ease-in-out both;
        margin: 0 2px;
    }
    
    .loading-dots span:nth-child(1) {
        animation-delay: 0s;
    }
    
    .loading-dots span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .loading-dots span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes loadingDots {
        0%, 80%, 100% { 
            opacity: 0;
        }
        40% { 
            opacity: 1;
        }
    }
</style>
`);