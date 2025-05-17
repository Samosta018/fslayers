document.addEventListener('DOMContentLoaded', function() {
    const messagesContainer = document.getElementById('messages-container');
    const messageForm = document.getElementById('message-form');
    let lastMessageId = 0;
    let messagePolling;

    // Инициализация lastMessageId
    const lastMessageElement = messagesContainer.querySelector('.message:last-child');
    if (lastMessageElement && lastMessageElement.dataset.id) {
        lastMessageId = parseInt(lastMessageElement.dataset.id);
    }

    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function addMessageElement(msg) {
        const msgId = parseInt(msg.id);
        const existingMessage = messagesContainer.querySelector(`.message[data-id="${msgId}"]`);
        if (existingMessage) return;

        const isMy = msg.sender_id === CURRENT_USER_ID;
        const messageHTML = `
            <div class="message ${isMy ? 'my-message' : 'other-message'}" data-id="${msgId}">
                <div class="message-content">
                    <p>${msg.text}</p>
                    <span class="message-time">${msg.created_at}</span>
                </div>
            </div>
        `;
        messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
    }

    function loadMessages() {
        fetch(`/chat/api/messages/${CHAT_ID}/?last_message_id=${lastMessageId}`)
            .then(response => {
                if (!response.ok) throw new Error('Network error');
                return response.json();
            })
            .then(data => {
                if (data.messages?.length > 0) {
                    data.messages.forEach(msg => {
                        addMessageElement(msg);
                        lastMessageId = Math.max(lastMessageId, msg.id);
                    });
                    scrollToBottom();
                }
            })
            .catch(error => console.error('Error:', error));
    }

    messageForm.addEventListener('submit', function(e) {
        e.preventDefault();
        clearInterval(messagePolling); // Остановить polling
        
        const formData = new FormData(this);
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Network error');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                lastMessageId = data.message.id; // Обновляем ID до добавления
                addMessageElement(data.message);
                scrollToBottom();
                this.reset();
            }
        })
        .catch(error => console.error('Error:', error))
        .finally(() => {
            messagePolling = setInterval(loadMessages, 3000); // Перезапустить polling
        });
    });

    // Инициализация polling
    messagePolling = setInterval(loadMessages, 3000);
    scrollToBottom();
});