// База данных продуктов
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

// База знаний о проекте для чат-бота
const knowledgeBase = {
    // Общая информация о проекте
    project: {
        name: "Альтернатива",
        description: "Платформа для управления бойкотируемыми товарами и предоставления альтернативных продуктов местного производства.",
        mission: "Поддержка осознанного потребления и помощь людям в принятии этических решений при выборе товаров.",
        created: "Кыргызско-Турецким университетом Манаса",
        year: "2023",
        location: "Бишкек, Кыргызстан"
    },

    // Информация о функциях платформы
    features: {
        search: "Поиск информации о продуктах и их статусе (бойкотируется или нет)",
        alternatives: "Предложение этичных альтернатив для бойкотируемых товаров",
        local: "Приоритет товарам местного производства, которые отмечены значком 'KG'",
        ratings: "Рейтинговая система для оценки продуктов пользователями",
        categories: "Разделение товаров по категориям для удобного поиска"
    },

    // Критерии бойкота
    boycottCriteria: [
        "Поддержка военных действий",
        "Нарушение прав человека",
        "Негативное влияние на окружающую среду",
        "Использование неэтичных практик в производстве",
        "Эксплуатация водных и других природных ресурсов"
    ],

    // Часто задаваемые вопросы
    faq: {
        "Что такое бойкот?": "Бойкот — это форма протеста, при которой люди отказываются покупать товары или услуги определенного производителя из-за несогласия с его политикой или действиями.",
        "Как определяется, что товар нужно бойкотировать?": "Решение о включении товара в список бойкотируемых принимается на основе проверенной информации о нарушениях компании по нашим этическим критериям.",
        "Как я могу предложить добавить товар в список бойкотируемых?": "Вы можете отправить нам информацию через форму обратной связи с указанием продукта и причины, по которой его следует бойкотировать, приложив подтверждающие источники.",
        "Что означает значок 'KG'?": "Значок 'KG' указывает на то, что продукт произведен в Кыргызстане, что помогает поддерживать местных производителей."
    },

    // Контактная информация
    contact: {
        email: "info@alternative.kg",
        phone: "+996 555 123456",
        address: "г. Бишкек, Кыргызско-Турецкий университет Манаса"
    }
};

// Функция для создания карточки продукта
function createProductCard(product) {
    if (!product) {
        console.error("Продукт не определен");
        return "";
    }

    const statusClass = product.isBoycotted ? 'status-boycotted' : 'status-ok';
    const statusText = product.isBoycotted ? 'Бойкотируется' : 'Этичный выбор';

    const alternativesHTML = product.alternativeProducts && product.alternativeProducts.map(alt => {
        const localBadge = alt.isKyrgyzProduct ?
            `<div class="status-local" style="margin-left: 5px; font-size: 10px;">KG</div>` : '';

        return `
            <div class="alternative-item" onclick="showAlternativeModal('${alt.name}', '', ${alt.rating}, ${alt.isKyrgyzProduct}, '', '', false, '')">
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

    const boycottReasonHTML = product.isBoycotted && product.boycottReason ?
        `<div class="product-reason"><strong>Причина:</strong> ${product.boycottReason}</div>` : '';

    return `
        <div class="product-card">
            <div class="product-header">
                <img src="/api/placeholder/50/50" alt="${product.name}" class="product-logo">
                <div class="product-title">
                    <div class="product-name">${product.name}</div>
                    <div class="product-category">Категория: ${product.category || 'Не указана'}</div>
                </div>
                <div class="product-rating">
                    <span class="rating-star">★</span> ${product.rating || '0.0'}
                </div>
            </div>
            <div class="product-body">
                <div class="product-status ${statusClass}">${statusText}</div>
                ${boycottReasonHTML}
                <div class="product-description">
                    ${product.description || 'Описание отсутствует'}
                </div>

                <div class="alternatives-title">Этичные альтернативы:</div>
                <div class="alternatives-list">
                    ${alternativesHTML || '<div>Альтернативы не найдены</div>'}
                </div>
            </div>
        </div>
    `;
}

// Добавление сообщения в чат
function addMessage(content, isUser) {
    const chatMessages = document.querySelector('.chat-messages');
    if (!chatMessages) {
        console.warn("Элемент .chat-messages не найден!");
        return;
    }

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user-message' : 'ai-message');
    messageDiv.innerHTML = content;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Функция получения CSRF-токена из cookie
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

// Функция поиска продукта
function searchProduct(query) {
    console.log("Отправляем запрос:", query);

    // Проверка наличия query
    if (!query || query.trim() === '') {
        addMessage("Пожалуйста, введите название продукта для поиска.", false);
        return;
    }

    // Добавление индикатора загрузки
    const chatMessages = document.querySelector('.chat-messages');
    const loadingDiv = document.createElement('div');
    loadingDiv.classList.add('message', 'ai-message');
    loadingDiv.innerHTML = '<div style="display: flex; align-items: center;"><span style="margin-right: 10px;">Поиск</span><div class="loading-dots"><span>.</span><span>.</span><span>.</span></div></div>';
    chatMessages.appendChild(loadingDiv);

    // Отправка запроса на сервер
    fetch('http://localhost:8000/assistant/search-product/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({query})
    })
        .then(res => {
            if (!res.ok) {
                throw new Error(`Ошибка HTTP: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            // Удаляем индикатор загрузки
            if (chatMessages.contains(loadingDiv)) {
                chatMessages.removeChild(loadingDiv);
            }

            if (data.success) {
                addMessage(data.html + "<br>Хотите узнать подробнее о каком-то конкретном продукте?", false);
            } else {
                addMessage(data.html || "Информация о продукте не найдена.", false);
            }
        })
        .catch(err => {
            console.error("Ошибка запроса:", err);

            // Удаляем индикатор загрузки
            if (chatMessages.contains(loadingDiv)) {
                chatMessages.removeChild(loadingDiv);
            }

            // Симулируем ответ из локальной базы данных при ошибке соединения
            const lowerQuery = query.toLowerCase();
            let product = null;

            // Поиск в локальной базе данных
            for (const key in productDatabase) {
                if (lowerQuery.includes(key) || productDatabase[key].name.toLowerCase().includes(lowerQuery)) {
                    product = productDatabase[key];
                    break;
                }
            }

            if (product) {
                const productCardHTML = createProductCard(product);
                addMessage(productCardHTML + "<br>Хотите узнать подробнее о каком-то конкретном продукте?", false);
            } else {
                // Если продукт не найден в локальной базе данных, возвращаем общий ответ
                addMessage("Извините, я не смог найти информацию об этом продукте. Попробуйте поискать другой продукт или задать вопрос о проекте.", false);
            }
        });
}

// Функция для отображения модального окна с информацией о продукте
function showAlternativeModal(name, image, rating, isKyrgyzProduct, category, description, isBoycotted, boycottReason) {
    // Проверка параметров
    name = name || 'Нет названия';
    rating = rating || '0.0';
    category = category || 'Не указана';
    description = description || 'Информация отсутствует';

    // Приведение к строковому типу для корректного сравнения
    isKyrgyzProduct = String(isKyrgyzProduct);
    isBoycotted = String(isBoycotted);

    // Получение элементов модального окна
    const modal = document.getElementById("alternative-modal");
    if (!modal) {
        console.error("Модальное окно не найдено");
        return;
    }

    // Установка основной информации
    const nameElement = document.getElementById("modal-alt-name");
    const ratingElement = document.getElementById("modal-alt-rating");
    const categoryElement = document.getElementById("modal-alt-category");
    const descriptionElement = document.getElementById("modal-alt-description");

    if (nameElement) nameElement.innerText = name;
    if (ratingElement) ratingElement.innerText = rating;
    if (categoryElement) categoryElement.innerText = category;
    if (descriptionElement) descriptionElement.innerText = description;

    // Установка изображения
    const imageElement = document.getElementById("modal-alt-image");
    if (imageElement) {
        if (image && image !== 'undefined' && !image.includes('undefined')) {
            imageElement.src = image;
        } else {
            imageElement.src = "/api/placeholder/200/150"; // Запасное изображение
        }
    }

    // Установка статуса продукта
    const statusBadge = document.getElementById("modal-alt-status-badge");
    const statusText = document.getElementById("modal-alt-status");
    const reasonContainer = document.getElementById("modal-alt-reason-container");
    const reasonElement = document.getElementById("modal-alt-reason");

    if (statusBadge && statusText) {
        if (isBoycotted === "true" || isBoycotted === "True") {
            statusBadge.className = "modal-status boycotted";
            statusText.innerText = "Бойкотируется";

            // Показываем причину бойкота
            if (reasonContainer && reasonElement) {
                reasonElement.innerText = boycottReason || "Причина не указана";
                reasonContainer.classList.remove("modal-reason-hidden");
            }
        } else {
            statusBadge.className = "modal-status ethical";
            statusText.innerText = "Этичный выбор";

            // Скрываем причину бойкота
            if (reasonContainer) {
                reasonContainer.classList.add("modal-reason-hidden");
            }
        }
    }

    // Установка информации о стране производства
    const countryBadge = document.getElementById("modal-alt-country-badge");
    const countryText = document.getElementById("modal-alt-country");

    if (countryBadge && countryText) {
        if (isKyrgyzProduct === "true" || isKyrgyzProduct === "True") {
            countryBadge.style.backgroundColor = "#e3f2fd";
            countryBadge.style.color = "#1565c0";
            countryText.innerText = "Кыргызстан";
        } else {
            countryBadge.style.backgroundColor = "#f0f0f0";
            countryBadge.style.color = "#666";
            countryText.innerText = "Зарубежный";
        }
    }

    // Показываем модальное окно с плавной анимацией
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
    if (!modal) return;

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
    const nameElement = document.getElementById("modal-alt-name");
    if (!nameElement) return;

    const name = nameElement.innerText;
    closeModal();

    // Имитируем поиск как обычный ввод
    addMessage(name, true);
    searchProduct(name);
}

// Функция для генерации ответа на вопрос пользователя
function generateResponse(query) {
    if (!query || query.trim() === '') {
        return 'Пожалуйста, задайте вопрос или введите название продукта для поиска.';
    }

    // Приводим запрос к нижнему регистру для поиска ключевых слов
    const lowerQuery = query.toLowerCase();

    // Проверяем наличие ключевых слов и возвращаем соответствующие ответы

    // Приветствия
    if (lowerQuery.includes('привет') || lowerQuery.includes('здравствуй') || lowerQuery.includes('добрый день')) {
        return 'Здравствуйте! Рад помочь вам узнать больше о проекте "Альтернатива". Что именно вас интересует?';
    }

    // О проекте
    if (lowerQuery.includes('о проект') || lowerQuery.includes('что такое альтернатива') || (lowerQuery.includes('расскаж') && lowerQuery.includes('проект'))) {
        return `"${knowledgeBase.project.name}" - это ${knowledgeBase.project.description} Наша миссия - ${knowledgeBase.project.mission} Проект был создан ${knowledgeBase.project.created} в ${knowledgeBase.project.year} году.`;
    }

    // О миссии
    if (lowerQuery.includes('цель') || lowerQuery.includes('миссия')) {
        return `Наша миссия - ${knowledgeBase.project.mission} Мы стремимся обеспечить пользователей достоверной информацией о бойкотируемых продуктах и предложить качественные альтернативы, отдавая предпочтение товарам местного производства.`;
    }

    // О критериях бойкота
    if (lowerQuery.includes('критери') || (lowerQuery.includes('причин') && (lowerQuery.includes('бойкот') || lowerQuery.includes('отказ')))) {
        return `Мы оцениваем продукты по следующим этическим критериям:<br>
                <ul class="about-list" style="margin-top: 8px;">
                ${knowledgeBase.boycottCriteria.map(criterion => `<li>${criterion}</li>`).join('')}
                </ul>`;
    }

    // О функциях платформы
    if (lowerQuery.includes('функции') || lowerQuery.includes('что умеет') || lowerQuery.includes('возможности')) {
        return `Наша платформа предлагает следующие функции:<br>
                <ul class="about-list" style="margin-top: 8px;">
                <li>Поиск информации о продуктах и их статусе</li>
                <li>Предложение этичных альтернатив</li>
                <li>Приоритет товарам местного производства (со значком "KG")</li>
                <li>Рейтинговая система для оценки продуктов</li>
                <li>Удобное разделение по категориям</li>
                </ul>`;
    }

    // FAQ - вопросы из базы знаний
    for (const [question, answer] of Object.entries(knowledgeBase.faq)) {
        if (lowerQuery.includes(question.toLowerCase())) {
            return answer;
        }
    }

    // О значке KG
    if (lowerQuery.includes('kg') || lowerQuery.includes('кыргыз') || (lowerQuery.includes('местн') && lowerQuery.includes('продукт'))) {
        return `Значок "KG" указывает на то, что продукт произведен в Кыргызстане. Мы отдаем приоритет местным производителям, чтобы поддержать экономику страны и сократить углеродный след от транспортировки товаров.`;
    }

    // О рейтинге
    if (lowerQuery.includes('рейтинг') || lowerQuery.includes('оценк') || lowerQuery.includes('звезд')) {
        return `Рейтинговая система нашей платформы позволяет пользователям оценивать продукты по пятибалльной шкале. Рейтинг отображается в виде звезд. Чем выше рейтинг, тем лучше продукт оценен нашим сообществом.`;
    }

    // Контакты
    if (lowerQuery.includes('контакт') || lowerQuery.includes('связ') || lowerQuery.includes('почта') || lowerQuery.includes('телефон')) {
        return `Вы можете связаться с нами:<br>
                Email: ${knowledgeBase.contact.email}<br>
                Телефон: ${knowledgeBase.contact.phone}<br>
                Адрес: ${knowledgeBase.contact.address}`;
    }

    // Как пользоваться
    if (lowerQuery.includes('как пользоваться') || lowerQuery.includes('инструкция') || lowerQuery.includes('как работает')) {
        return `Чтобы воспользоваться нашей платформой:<br>
                1. Введите название интересующего вас продукта в поисковую строку.<br>
                2. Ознакомьтесь с информацией о статусе продукта (бойкотируется или нет).<br>
                3. Если продукт бойкотируется, изучите предложенные альтернативы.<br>
                4. Обратите внимание на товары со значком "KG" - это местные продукты.`;
    }

    // Как добавить продукт
    if ((lowerQuery.includes('добавить') || lowerQuery.includes('предложить')) && lowerQuery.includes('продукт')) {
        return `Чтобы предложить добавить новый продукт или обновить информацию о существующем, пожалуйста, свяжитесь с нами по email: ${knowledgeBase.contact.email}. Укажите название продукта, производителя и, если это предложение для бойкота, приложите подтверждающие источники о нарушениях.`;
    }

    // Проверка на запрос о продукте
    const productKeys = Object.keys(productDatabase);
    for (const key of productKeys) {
        if (lowerQuery.includes(key) || lowerQuery.includes(productDatabase[key].name.toLowerCase())) {
            // Если запрос о продукте, перенаправляем к функции поиска продукта
            return null; // Возвращаем null для перенаправления запроса
        }
    }

    // Общий ответ при отсутствии совпадений
    return `Спасибо за ваш вопрос! Я постараюсь на него ответить.<br><br>
            Платформа "Альтернатива" помогает пользователям делать осознанный выбор товаров, предоставляя информацию о бойкотируемых продуктах и их этичных альтернативах.<br><br>
            Если я не ответил на ваш вопрос, вы можете связаться с нами напрямую по email: ${knowledgeBase.contact.email}`;
}

// Инициализация после загрузки DOM
document.addEventListener('DOMContentLoaded', function () {
    // Добавляем стили для анимации загрузки
    const styleElement = document.createElement('style');
    styleElement.textContent = `
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
    `;
    document.head.appendChild(styleElement);

    // Инициализация обработчиков для чата на главной странице
    const chatButton = document.querySelector('.chat-input button');
    const chatInput = document.querySelector('.chat-input input');

    if (chatButton && chatInput) {
        // Обработчик клика на кнопку отправки
        chatButton.addEventListener('click', function () {
            const message = chatInput.value.trim();

            if (message) {
                addMessage(message, true);
                chatInput.value = '';

                // Проверяем, является ли сообщение вопросом о проекте или запросом продукта
                const response = generateResponse(message);

                // Если response равен null, значит это запрос о продукте
                if (response === null) {
                    searchProduct(message);
                } else {
                    setTimeout(function () {
                        addMessage(response, false);
                    }, 500);
                }
            }
        });

        // Обработчик нажатия клавиши Enter в поле ввода
        chatInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                chatButton.click();
            }
        });
    }

    // Инициализация чата на странице "О проекте"
    const aboutChatButton = document.getElementById('about-chat-button');
    const aboutChatInput = document.getElementById('about-chat-input');

    if (aboutChatButton && aboutChatInput) {
        // Функция отправки сообщения
        function sendMessage() {
            const message = aboutChatInput.value.trim();

            if (message) {
                addMessage(message, true);
                aboutChatInput.value = '';

                setTimeout(function () {
                    const response = generateResponse(message);
                    addMessage(response || "Извините, я не смог обработать ваш запрос. Попробуйте сформулировать вопрос иначе.", false);
                }, 500);
            }
        }

        // Обработчик клика на кнопку отправки
        aboutChatButton.addEventListener('click', sendMessage);

        // Обработчик нажатия клавиши Enter в поле ввода
        aboutChatInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Проверка и обработка формы обратной связи (если есть)
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            const messageInput = document.getElementById('message');

            if (!nameInput || !emailInput || !messageInput) {
                alert('Ошибка: форма не содержит необходимые поля');
                return;
            }

            const name = nameInput.value.trim();
            const email = emailInput.value.trim();
            const message = messageInput.value.trim();

            if (name === '' || email === '' || message === '') {
                alert('Все поля должны быть заполнены!');
                return;
            }

            // Валидация email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert('Пожалуйста, введите корректный email адрес');
                return;
            }

            alert('Ваше сообщение отправлено!');
            contactForm.reset();
        });
    }
});