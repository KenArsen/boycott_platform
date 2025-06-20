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

document.addEventListener('DOMContentLoaded', function () {
    // Имитация ввода "Coca-Cola" в чат
    const defaultQuery = 'Coca-Cola';

    // Автоматически выполняем поиск с query=Coca-Cola
    console.log("Автоматический запрос при загрузке:", defaultQuery);

    // Добавляем сообщение от пользователя (если нужно отображать его)
    // addMessage(defaultQuery, true);

    // Отправляем запрос
    searchProduct(defaultQuery);
});