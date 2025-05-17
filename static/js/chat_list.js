document.addEventListener('DOMContentLoaded', function() {
    const chatsContainer = document.getElementById('chats-container');
    let isMobile = window.innerWidth <= 768;

    function loadChats() {
        fetch('/chat/api/chats/')
            .then(response => response.json())
            .then(data => {
                chatsContainer.innerHTML = data.chats.map(chat => `
                    <a href="/chat/${chat.id}/" class="chat-item">
                        <div class="chat-info">
                            <h4 class="chat-user-name">${chat.other_user.name}</h4>
                            ${chat.last_message ? `<p>${chat.last_message}</p>` : ''}
                        </div>
                        ${chat.unread_count > 0 ? `<span class="unread-count">${chat.unread_count}</span>` : ''}
                    </a>
                `).join('');
            });
    }

    setInterval(loadChats, 3000);
    loadChats();

    // Обновление счетчика в шапке
    function updateHeaderCounter() {
        fetch('/chat/api/chats/')
            .then(response => response.json())
            .then(data => {
                const totalUnread = data.chats.reduce((sum, chat) => sum + chat.unread_count, 0);
                const counter = document.getElementById('messages-counter');
                if (counter) {
                    counter.textContent = totalUnread > 0 ? `(${totalUnread})` : '';
                }
            });
    }

    setInterval(updateHeaderCounter, 5000);
    updateHeaderCounter();
});