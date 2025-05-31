document.addEventListener('DOMContentLoaded', function() {
    // 从 window.chatConfig 获取初始数据
    const currentUsername = window.chatConfig.currentUsername;
    let initialChannelId = window.chatConfig.initialChannelId;
    const feedbackBaseUrl = window.chatConfig.feedbackBaseUrl || '/feedback'; // 提供一个默认值

    // DOM元素获取
    const chatListItems = document.querySelectorAll('.chat-list-item');
    const chatHeader = document.getElementById('chat-header');
    const messageContainer = document.getElementById('message-container');
    const inputArea = document.getElementById('input-area');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    // 合同弹窗相关DOM
    const contractModal = document.getElementById('contract-modal');
    const tenantNameDisplay = document.getElementById('tenant-name-display');
    const houseNameDisplay = document.getElementById('house-name-display');
    const closeContractModalBtn = document.getElementById('close-contract-modal-btn');
    const contractForm = document.getElementById('contract-form');
    const startDateInput = document.getElementById('start-date');
    const monthsInput = document.getElementById('months');
    const calculatedEndDateSpan = document.getElementById('calculated-end-date');
    const calculatedAmountSpan = document.getElementById('calculated-amount');
    const hiddenEndDateInput = document.getElementById('end-date');
    const hiddenAmountInput = document.getElementById('amount');

    // 全局状态变量 (之前在HTML中通过 window.active... 定义)
    let activeChannelId = null;
    let activeTenantUsername = null;
    let activeLandlordUsername = null;
    let activeHousePrice = 0;
    let activeHouseDeposit = 0;

    // --- 原 message.js 中的辅助函数 ---
    function formatTimestamp(isoTimestamp) {
        if (!isoTimestamp) return '时间未知';
        try {
            const date = new Date(isoTimestamp);
            if (isNaN(date.getTime())) return '无效时间';

            // 强制转换为北京时间 (不依赖浏览器时区)
            const beijingTimestamp = new Date(date.getTime() + (8 - date.getTimezoneOffset() / 60) * 3600000);
            const year = beijingTimestamp.getFullYear();
            const month = String(beijingTimestamp.getMonth() + 1).padStart(2, '0');
            const day = String(beijingTimestamp.getDate()).padStart(2, '0');
            const hour = String(beijingTimestamp.getHours()).padStart(2, '0');
            const minute = String(beijingTimestamp.getMinutes()).padStart(2, '0');
            return `${year}-${month}-${day} ${hour}:${minute}`;
        } catch (e) {
            console.error("Error formatting timestamp:", e);
            return '时间错误';
        }
    }

    function scrollToBottom(container) {
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    }

    // --- 从 message.html 移入的函数 ---
    async function loadChat(channelId) {
        if (!channelId || !messageContainer || !chatHeader || !inputArea) return;
        activeChannelId = channelId; // 更新活动频道ID

        chatListItems.forEach(item => {
            item.classList.remove('active');
            if (item.dataset.channelId === channelId.toString()) {
                item.classList.add('active');
            }
        });

        try {
            const response = await fetch(`${feedbackBaseUrl}/get_chat_data/${channelId}`);
            if (!response.ok) throw new Error('获取聊天数据失败 (服务器响应异常)');

            const data = await response.json();
            if (!data.success) throw new Error(data.error || '获取聊天数据失败 (数据错误)');

            activeTenantUsername = data.channel.tenant_username;
            activeLandlordUsername = data.channel.landlord_username;
            if (data.house) {
                activeHousePrice = parseFloat(data.house.price) || 0;
                activeHouseDeposit = parseFloat(data.house.deposit) || 0;
            } else { // 如果没有房源信息，重置价格和押金
                activeHousePrice = 0;
                activeHouseDeposit = 0;
            }

            updateChatHeader(data.channel, data.house);
            updateMessages(data.messages);
            inputArea.style.display = 'flex';
            markMessagesAsRead(channelId);

        } catch (error) {
            console.error('加载聊天失败:', error);
            if (window.showMessage) {
                window.showMessage(`加载聊天失败: ${error.message}`, 'error');
            } else {
                alert(`加载聊天失败: ${error.message}`);
            }
            messageContainer.innerHTML = `<p class="no-messages-placeholder">加载聊天失败: ${error.message}</p>`;
        }
    }

    function updateChatHeader(channel, house) {
        if (!chatHeader) return;
        const isLandlord = currentUsername === channel.landlord_username;
        const contactName = isLandlord ? channel.tenant_username : channel.landlord_username;
        const contactRole = isLandlord ? '租客' : '房东';
        const houseName = house ? house.house_name : '未知房源';

        let headerHTML = `
            <h2 style="position:relative;">
                ${contactName}
                <span style="font-size: 12px; color: #666; font-weight: normal;">(${contactRole})</span>
                <span style="font-size: 13px; color: #888; margin-left: 16px;">房源：${houseName}</span>`;

        if (channel.house_status === 0) { // 可出租
            headerHTML += `<span style="color:green;margin-left:10px;margin-right:10px;">可出租</span>`;
            if (isLandlord) {
                headerHTML += `<button id="send-contract-btn" class="send-button" style="margin-left:10px;display:inline-block;">发送合同</button>`;
            }
        } else if (channel.house_status === 1) { // 出租中
            headerHTML += `<span style="color:orange;margin-left:10px;">出租中</span>`;
        } else if ([2, 4, 5].includes(channel.house_status)) { // 未上架/待审核/审核未通过
            headerHTML += `<span style="color:red;margin-left:10px;">未上架/审核中</span>`;
        }
        headerHTML += `</h2>`;
        chatHeader.innerHTML = headerHTML;

        const sendContractBtn = document.getElementById('send-contract-btn');
        if (sendContractBtn) {
            sendContractBtn.addEventListener('click', () => {
                if (tenantNameDisplay) tenantNameDisplay.textContent = channel.tenant_username;
                if (houseNameDisplay) houseNameDisplay.textContent = houseName;
                if (contractModal) contractModal.style.display = 'block';
                updateCalculation(); // 初始化计算
            });
        }
    }

    function updateMessages(messages) {
        if (!messageContainer) return;
        if (!messages || messages.length === 0) {
            messageContainer.innerHTML = '<p class="no-messages-placeholder">开始你们的对话吧！</p>';
            return;
        }

        let messagesHTML = '';
        messages.forEach(message => {
            const isSent = message.sender_username === currentUsername;
            const formattedTime = formatTimestamp(message.timestamp);
            messagesHTML += `
                <div class="message-item ${isSent ? 'sent' : 'received'}" data-timestamp="${message.timestamp}">
                    <div class="message-content">
                        <div class="message-bubble">${message.content}</div>
                        <span class="message-timestamp">${formattedTime}</span>
                    </div>
                </div>`;
        });
        messageContainer.innerHTML = messagesHTML;
        scrollToBottom(messageContainer);
    }

    async function markMessagesAsRead(channelId) {
        try {
            await fetch(`${feedbackBaseUrl}/set_read/${channelId}`, { method: 'POST' });
            const unreadBadge = document.getElementById(`unread-badge-${channelId}`);
            if (unreadBadge) {
                unreadBadge.style.display = 'none';
            }
        } catch (error) {
            console.error('标记消息为已读失败:', error);
            // 可选择添加用户提示
        }
    }

    async function sendMessageInternal(content) { // Renamed to avoid conflict if global sendMessage exists
        if (!content || !activeChannelId || !messageContainer || !messageInput) return;

        const tempTimestamp = new Date().toISOString(); // 用于乐观更新
        // 乐观更新UI (使用已有的 appendMyMessage 逻辑，但需适配)
        const placeholderEl = messageContainer.querySelector('.no-messages-placeholder');
        if (placeholderEl) placeholderEl.remove();

        const messageItem = document.createElement('div');
        messageItem.className = 'message-item sent';
        messageItem.dataset.timestamp = tempTimestamp; // 临时时间戳
        messageItem.innerHTML = `
            <div class="message-content">
                <div class="message-bubble">${content}</div>
                <span class="message-timestamp">${formatTimestamp(tempTimestamp)}</span>
            </div>`;
        messageContainer.appendChild(messageItem);
        scrollToBottom(messageContainer);

        messageInput.value = ''; // 清空输入框
        messageInput.style.height = 'auto'; // 重置高度
        messageInput.focus();


        try {
            const formData = new FormData();
            formData.append('content', content);

            const response = await fetch(`${feedbackBaseUrl}/send_message/${activeChannelId}`, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.success && data.message) {
                // 更新刚刚乐观添加的消息的时间戳和内容 (如果后端有处理)
                const optimisticMessageElement = messageContainer.querySelector(`[data-timestamp="${tempTimestamp}"]`);
                if (optimisticMessageElement) {
                    optimisticMessageElement.dataset.timestamp = data.message.timestamp;
                    const timeSpan = optimisticMessageElement.querySelector('.message-timestamp');
                    if (timeSpan) timeSpan.textContent = formatTimestamp(data.message.timestamp);
                    // 如果后端处理了内容（比如过滤），也可以更新 bubble 内容
                    // const bubble = optimisticMessageElement.querySelector('.message-bubble');
                    // if (bubble) bubble.textContent = data.message.content;
                }
            } else {
                if (window.showMessage) {
                    window.showMessage('发送消息失败: ' + (data.error || '未知错误'), 'error');
                } else {
                    alert('发送消息失败: ' + (data.error || '未知错误'));
                }
                // 考虑是否移除乐观更新的消息或标记为发送失败
                if (messageItem) messageItem.classList.add('message-failed'); // 示例：添加失败样式
            }
        } catch (error) {
            console.error('发送消息请求失败:', error);
            if (window.showMessage) {
                window.showMessage('发送消息请求失败', 'error');
            } else {
                alert('发送消息请求失败');
            }
            if (messageItem) messageItem.classList.add('message-failed');
        }
    }

    function updateCalculation() {
        if (!startDateInput || !monthsInput || !calculatedEndDateSpan || !calculatedAmountSpan || !hiddenEndDateInput || !hiddenAmountInput) return;

        const startDateStr = startDateInput.value;
        const months = parseInt(monthsInput.value);

        if (!startDateStr || isNaN(months) || months <= 0) {
            calculatedEndDateSpan.textContent = '--';
            calculatedAmountSpan.textContent = '--';
            hiddenEndDateInput.value = '';
            hiddenAmountInput.value = '';
            return;
        }

        const startDate = new Date(startDateStr);
        const endDate = new Date(startDate);
        endDate.setMonth(endDate.getMonth() + months);
        if (endDate.getDate() !== startDate.getDate()) {
            endDate.setDate(0);
        }

        const endDateStr = endDate.toISOString().split('T')[0];
        const totalAmount = (activeHousePrice * months + activeHouseDeposit).toFixed(2);

        calculatedEndDateSpan.textContent = endDateStr;
        calculatedAmountSpan.textContent = totalAmount;
        hiddenEndDateInput.value = endDateStr;
        hiddenAmountInput.value = totalAmount;
    }


    // --- 事件监听器 ---
    if (messageInput) {
        messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const content = messageInput.value.trim();
                if (content) {
                    sendMessageInternal(content);
                }
            }
        });
    }

    if (sendButton) {
        sendButton.addEventListener('click', () => {
            const content = messageInput.value.trim();
            if (content) {
                sendMessageInternal(content);
            }
        });
    }

    chatListItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const channelId = item.dataset.channelId;
            if (channelId !== activeChannelId) { // 只有在切换频道时才加载
                loadChat(channelId);
            }
        });
    });

    if (closeContractModalBtn && contractModal) {
        closeContractModalBtn.addEventListener('click', () => {
            contractModal.style.display = 'none';
        });
    }

    if (startDateInput) startDateInput.addEventListener('change', updateCalculation);
    if (monthsInput) monthsInput.addEventListener('input', updateCalculation);

    if (contractForm) {
        contractForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const startDate = startDateInput.value;
            const endDate = hiddenEndDateInput.value;
            const amount = hiddenAmountInput.value;

            if (!startDate || !endDate || !amount) {
                if (window.showMessage) {
                    window.showMessage("请填写完整的合同信息（开始日期、月数）。", 'warning');
                } else {
                    alert("请填写完整的合同信息（开始日期、月数）。");
                }
                return;
            }

            fetch(`${feedbackBaseUrl}/send_contract`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    channel_id: activeChannelId,
                    start_date: startDate,
                    end_date: endDate,
                    amount: amount,
                    receiver_username: activeTenantUsername // 确保这个变量在 loadChat 中被正确设置
                })
            })
                .then(res => {
                    if (!res.ok) throw new Error("网络或服务器错误：" + res.status);
                    return res.json();
                })
                .then(data => {
                    if (data.success) {
                        if (window.showMessage) {
                            window.showMessage("合同已发送", 'success');
                        } else {
                            alert("合同已发送");
                        }
                        if (contractModal) contractModal.style.display = 'none';
                        if (activeChannelId) loadChat(activeChannelId); // 重新加载聊天以显示新消息
                    } else {
                        if (window.showMessage) {
                            window.showMessage("发送失败：" + data.msg, 'error');
                        } else {
                            alert("发送失败：" + data.msg);
                        }
                    }
                })
                .catch(err => {
                    console.error("请求出错：", err);
                    if (window.showMessage) {
                        window.showMessage("请求失败：" + err.message, 'error');
                    } else {
                        alert("请求失败：" + err.message);
                    }
                });
        });
    }

    // --- 初始加载 ---
    if (initialChannelId) {
        loadChat(initialChannelId);
    } else if (chatListItems.length > 0) {
        // 如果没有指定初始频道，但列表不为空，可以默认加载第一个
        // loadChat(chatListItems[0].dataset.channelId);
        // 或者保持原样，等待用户点击
        if (messageContainer) messageContainer.innerHTML = '<p class="no-messages-placeholder">请在左侧选择一个聊天开始对话</p>';
    } else {
        if (messageContainer) messageContainer.innerHTML = '<p class="no-messages-placeholder">暂无聊天会话</p>';
    }
});