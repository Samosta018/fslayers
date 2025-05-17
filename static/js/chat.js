document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.getElementById('ai-chat-input');
    const chatSubmit = document.getElementById('ai-chat-submit');
    const chatMessages = document.getElementById('ai-chat-messages');
    
    // Auto-resize textarea
    chatInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
    
    // Send message on button click
    chatSubmit.addEventListener('click', sendMessage);
    
    // Send message on Enter (but allow Shift+Enter for new line)
    chatInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    function sendMessage() {
        const messageText = chatInput.value.trim();
        if (messageText === '') return;
        
        // Add user message to chat
        addMessage(messageText, 'user');
        chatInput.value = '';
        chatInput.style.height = 'auto';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Make API call to Django backend
        fetch('/assistant/api/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({message: messageText})
        })
        .then(response => {
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                return response.text().then(text => {
                    throw new Error(`Сервер вернул HTML вместо JSON: ${text.substring(0, 100)}...`);
                });
            }
            return response.json();
        })
        .then(data => {
            removeTypingIndicator();
            if (data.response) {
                addMessage(data.response, 'assistant');
            } else {
                addMessage("Ошибка: сервер не вернул ответ", 'assistant');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            removeTypingIndicator();
            addMessage(`Ошибка запроса: ${error.message}`, 'assistant');
        });
    }
    
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `ai-message ai-message-${sender}`;
        
        const messageContent = document.createElement('div');
        messageContent.innerHTML = text;
        messageDiv.appendChild(messageContent);
        
        messageContent.querySelectorAll('a').forEach(link => {
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
        });
        
        const timestamp = document.createElement('div');
        timestamp.className = 'ai-message-timestamp';
        timestamp.textContent = getCurrentTime();
        messageDiv.appendChild(timestamp);
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'ai-message ai-message-assistant';
        typingDiv.id = 'ai-typing-indicator';
        
        const typingContent = document.createElement('div');
        typingContent.className = 'ai-typing-indicator';
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.className = 'ai-typing-dot';
            typingContent.appendChild(dot);
        }
        
        typingDiv.appendChild(typingContent);
        chatMessages.appendChild(typingDiv);
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('ai-typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    }
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});