document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const messageContainer = document.getElementById('message-container');
    // 获取 action url
    const actionUrl = window.location.origin + '/feedback/send_message/' + window.channelId;

    // 输入框自适应高度
    if (messageInput) {
        messageInput.addEventListener('input', function() {
            // alert('按钮被点击了');
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    }

    // 发送按钮事件
    if (sendButton && messageInput) {
        sendButton.addEventListener('click', function() {
            const messageContent = messageInput.value.trim();
            if (!messageContent) return;

            const tempTimestamp = new Date().toISOString();
            appendMyMessage(messageContent, tempTimestamp);

            // 清空输入框
            messageInput.value = '';
            messageInput.style.height = 'auto';
            messageInput.focus();

            // 发送异步请求
            fetch(actionUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: 'content=' + encodeURIComponent(messageContent)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success && data.message) {
                    // 可选：更新刚才添加的消息的时间戳
                    const tempMessage = messageContainer.querySelector(`[data-timestamp="${tempTimestamp}"]`);
                    if (tempMessage) {
                        const timeSpan = tempMessage.querySelector('.message-timestamp');
                        if (timeSpan) {
                            timeSpan.textContent = formatTimestamp(data.message.timestamp);
                        }
                        tempMessage.dataset.timestamp = data.message.timestamp;
                    }
                } else {
                    alert(data.error || '发送失败');
                }
            })
            .catch(() => {
                alert('网络错误，发送失败');
            });
        });
    }

    // 聊天列表点击设为已读
    document.querySelectorAll('.chat-list-item').forEach(function(item) {
        item.addEventListener('click', function(e) {
            // 获取频道ID
            const href = this.getAttribute('href');
            const match = href.match(/\/chat\/(\d+)/);
            if (match) {
                const channelId = match[1];
                fetch('/feedback/set_read/' + channelId, {
                    method: 'POST'
                });
            }
            // 不阻止默认跳转
        });
    });
});

// --- 辅助函数 ---

/**
 * 将当前用户发送的消息添加到聊天界面 (乐观更新)
 * @param {string} content 消息内容
 * @param {string} timestamp ISO 格式的时间戳 (可以是临时的)
 */
// --- 移除 myInitial 参数 ---
function appendMyMessage(content, timestamp) {
    const messageContainer = document.getElementById('message-container');
    if (!messageContainer) return;

    const placeholder = messageContainer.querySelector('.no-messages-placeholder');
    if (placeholder) {
        placeholder.remove();
    }

    const messageItem = document.createElement('div');
    messageItem.className = 'message-item sent';
    messageItem.dataset.timestamp = timestamp;

    // --- 移除 avatarDiv 和 avatarImg 的创建和添加 ---

    const messageContentDiv = document.createElement('div');
    messageContentDiv.className = 'message-content';

    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.textContent = content;
    messageContentDiv.appendChild(bubbleDiv);

    const timeSpan = document.createElement('span');
    timeSpan.className = 'message-timestamp';
    timeSpan.textContent = formatTimestamp(timestamp);
    messageContentDiv.appendChild(timeSpan);

    // --- 直接将 messageContentDiv 添加到 messageItem ---
    messageItem.appendChild(messageContentDiv);
    // --- 移除 avatarDiv 的添加 ---

    messageContainer.appendChild(messageItem);
    scrollToBottom(messageContainer);
}

/**
 * 将接收到的消息添加到聊天界面
 * @param {string} sender 发送者用户名
 * @param {string} content 消息内容
 * @param {string} timestamp ISO 格式的时间戳
 * @param {string} tenantUsername 租客用户名 (可能不再需要)
 * @param {string} landlordUsername 房东用户名 (可能不再需要)
 */
// --- 移除 avatarInitial, tenantUsername, landlordUsername 参数 ---
function appendReceivedMessage(sender, content, timestamp) {
    const messageContainer = document.getElementById('message-container');
    if (!messageContainer) return;

    const placeholder = messageContainer.querySelector('.no-messages-placeholder');
    if (placeholder) {
        placeholder.remove();
    }

    const messageItem = document.createElement('div');
    messageItem.className = 'message-item received';
    messageItem.dataset.timestamp = timestamp;

    // --- 移除 avatarDiv 和 avatarImg 的创建和添加 ---

    const messageContentDiv = document.createElement('div');
    messageContentDiv.className = 'message-content';

    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.textContent = content;
    messageContentDiv.appendChild(bubbleDiv);

    const timeSpan = document.createElement('span');
    timeSpan.className = 'message-timestamp';
    timeSpan.textContent = formatTimestamp(timestamp);
    messageContentDiv.appendChild(timeSpan);

    // --- 直接将 messageContentDiv 添加到 messageItem ---
    messageItem.appendChild(messageContentDiv);
    // --- 移除 avatarDiv 的添加 ---

    messageContainer.appendChild(messageItem);
    scrollToBottomIfNeeded(messageContainer);
}

/**
 * 格式化时间戳
 * @param {string} isoTimestamp ISO 格式的时间戳
 * @returns {string} 格式化后的时间字符串
 */
function formatTimestamp(isoTimestamp) {
    // ... (函数内容不变) ...
    if (!isoTimestamp) return '时间未知';
    try {
        const date = new Date(isoTimestamp);
        if (isNaN(date.getTime())) return '无效时间';

        const now = new Date();
        const diffSeconds = Math.round((now - date) / 1000);

        if (diffSeconds < 60) {
            return '刚刚';
        }

        // 默认格式
        return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
    } catch (e) {
        console.error("Error formatting timestamp:", e);
        return '时间错误';
    }
}

/**
 * 将容器滚动到底部
 * @param {HTMLElement} container
 */
function scrollToBottom(container) {
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}

/**
 * 如果滚动条接近底部，则滚动到底部
 * @param {HTMLElement} container
 */
function scrollToBottomIfNeeded(container) {
    if (!container) return;
    const isScrolledToBottom = container.scrollHeight - container.clientHeight <= container.scrollTop + 20;
    if (isScrolledToBottom) {
       scrollToBottom(container);
    }
}