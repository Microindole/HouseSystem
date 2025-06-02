// message.js

document.addEventListener('DOMContentLoaded', function() {
    // 从 window.chatConfig 获取初始数据
    const currentUsername = window.chatConfig.currentUsername;
    let initialChannelId = window.chatConfig.initialChannelId;
    const feedbackBaseUrl = window.chatConfig.feedbackBaseUrl || '/feedback';

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

    // 合同弹窗中的输入字段
    const monthlyRentInput = document.getElementById('contract-monthly-rent');
    const startDateInput = document.getElementById('start-date');
    const monthsInput = document.getElementById('months');
    const calculatedEndDateSpan = document.getElementById('calculated-end-date');
    const hiddenEndDateInput = document.getElementById('end-date-hidden');

    const depositInput = document.getElementById('contract-deposit');
    const paymentFrequencySelect = document.getElementById('payment-frequency');
    const leasePurposeInput = document.getElementById('lease-purpose');
    const otherAgreementsTextarea = document.getElementById('other-agreements');

    // 全局状态变量
    let activeChannelId = initialChannelId;
    let activeTenantUsername = null; // 将在 loadChat 中被设置
    let activeLandlordUsername = null; // 将在 loadChat 中被设置
    let activeHouseInfo = null;

    function formatTimestamp(isoTimestamp) {
        if (!isoTimestamp) return '时间未知';
        try {
            const date = new Date(isoTimestamp);
            if (isNaN(date.getTime())) return '无效时间';
            return date.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
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

    async function loadChat(channelId) {
        if (!channelId || !messageContainer || !chatHeader || !inputArea) return;
        activeChannelId = channelId;

        chatListItems.forEach(item => {
            item.classList.remove('active');
            if (item.dataset.channelId === channelId.toString()) {
                item.classList.add('active');
            }
        });

        try {
            const response = await fetch(`${feedbackBaseUrl}/get_chat_data/${channelId}`);
            if (!response.ok) throw new Error(`获取聊天数据失败 (服务器响应: ${response.status})`);

            const data = await response.json();
            if (!data.success) throw new Error(data.error || '获取聊天数据失败 (数据解析错误)');

            activeTenantUsername = data.channel.tenant_username;
            activeLandlordUsername = data.channel.landlord_username;
            activeHouseInfo = data.house;

            updateChatHeader(data.channel, data.house);
            updateMessages(data.messages);
            inputArea.style.display = 'flex';
            markMessagesAsRead(channelId);

        } catch (error) {
            console.error('加载聊天失败:', error);
            if (window.showMessage) window.showMessage(`加载聊天失败: ${error.message}`, 'error');
            else alert(`加载聊天失败: ${error.message}`);
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

        if (channel.house_status === 0 && isLandlord) { // 0 代表可出租
            headerHTML += `<span style="color:green;margin-left:10px;margin-right:10px;">可出租</span>`;
            headerHTML += `<button id="send-contract-btn" class="send-button" style="margin-left:10px;display:inline-block;">发送合同</button>`;
        } else if (channel.house_status === 1) { // 1 代表出租中
            headerHTML += `<span style="color:orange;margin-left:10px;">出租中</span>`;
        } else if ([2, 4, 5].includes(channel.house_status)) {
            headerHTML += `<span style="color:red;margin-left:10px;">未上架/审核中/已终止</span>`;
        }
        headerHTML += `</h2>`;
        chatHeader.innerHTML = headerHTML;

        const sendContractBtn = document.getElementById('send-contract-btn');
        if (sendContractBtn) {
            sendContractBtn.addEventListener('click', async () => {
                try {
                    // 先检查是否有活跃合同
                    const checkResponse = await fetch(`/feedback/check_active_contracts/${channel.channel_id}`);
                    const checkData = await checkResponse.json();

                    if (checkData.has_active_contract) {
                        if (window.showMessage) {
                            window.showMessage(`此聊天已存在一份${checkData.status_text}的合同，请先处理现有合同。`, 'warning');
                        } else {
                            alert(`此聊天已存在一份${checkData.status_text}的合同，请先处理现有合同。`);
                        }
                        return;
                    }

                    // 原有的合同表单显示逻辑
                    if (tenantNameDisplay) tenantNameDisplay.textContent = channel.tenant_username;
                    if (houseNameDisplay) houseNameDisplay.textContent = houseName;

                    if (activeHouseInfo) {
                        if (monthlyRentInput) monthlyRentInput.value = activeHouseInfo.price > 0 ? parseFloat(activeHouseInfo.price).toFixed(2) : '';
                        if (depositInput) depositInput.value = activeHouseInfo.deposit >= 0 ? parseFloat(activeHouseInfo.deposit).toFixed(2) : ''; // 押金可以为0
                    } else {
                        if (monthlyRentInput) monthlyRentInput.value = '';
                        if (depositInput) depositInput.value = '';
                    }

                    if (paymentFrequencySelect) paymentFrequencySelect.value = '月付';
                    if (leasePurposeInput) leasePurposeInput.value = '居住';
                    if (otherAgreementsTextarea) otherAgreementsTextarea.value = '';
                    if (monthsInput) monthsInput.value = '12'; // 默认12个月
                    if (startDateInput) startDateInput.value = ''; // 清空让用户选择

                    updateCalculation(); // 更新结束日期显示
                    if (contractModal) {
                        contractModal.style.display = 'flex';
                    }
                } catch (error) {
                    console.error("检查合同状态失败:", error);
                    // 继续显示合同表单
                    if (tenantNameDisplay) tenantNameDisplay.textContent = channel.tenant_username;
                    if (houseNameDisplay) houseNameDisplay.textContent = houseName;

                    if (activeHouseInfo) {
                        if (monthlyRentInput) monthlyRentInput.value = activeHouseInfo.price > 0 ? parseFloat(activeHouseInfo.price).toFixed(2) : '';
                        if (depositInput) depositInput.value = activeHouseInfo.deposit >= 0 ? parseFloat(activeHouseInfo.deposit).toFixed(2) : ''; // 押金可以为0
                    } else {
                        if (monthlyRentInput) monthlyRentInput.value = '';
                        if (depositInput) depositInput.value = '';
                    }

                    if (paymentFrequencySelect) paymentFrequencySelect.value = '月付';
                    if (leasePurposeInput) leasePurposeInput.value = '居住';
                    if (otherAgreementsTextarea) otherAgreementsTextarea.value = '';
                    if (monthsInput) monthsInput.value = '12'; // 默认12个月
                    if (startDateInput) startDateInput.value = ''; // 清空让用户选择

                    updateCalculation(); // 更新结束日期显示
                    if (contractModal) {
                        contractModal.style.display = 'flex';
                    }
                }
            });
        }
    }

    function updateMessages(messages) {
        if (!messageContainer) return;
        if (!messages || messages.length === 0) {
            messageContainer.innerHTML = '<p class="no-messages-placeholder">开始你们的对话吧！</p>';
            return;
        }
        messageContainer.innerHTML = messages.map(message => {
            const isSent = message.sender_username === currentUsername;
            const formattedTime = formatTimestamp(message.timestamp);
            return `
                <div class="message-item ${isSent ? 'sent' : 'received'}" data-timestamp="${message.timestamp}">
                    <div class="message-content">
                        <div class="message-bubble">${escapeHTML(message.content)}</div>
                        <span class="message-timestamp">${formattedTime}</span>
                    </div>
                </div>`;
        }).join('');
        scrollToBottom(messageContainer);
    }

    function escapeHTML(str) {
        if (typeof str !== 'string') return '';
        return str.replace(/[&<>"']/g, function (match) {
            return {
                '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
            }[match];
        });
    }

    async function markMessagesAsRead(channelId) {
        try {
            fetch(`${feedbackBaseUrl}/set_read/${channelId}`, { method: 'POST' });
            const unreadBadge = document.getElementById(`unread-badge-${channelId}`);
            if (unreadBadge) {
                unreadBadge.style.display = 'none';
            }
        } catch (error) {
            console.error('标记消息为已读失败:', error);
        }
    }

    async function sendMessageInternal(content) {
        if (!content || !activeChannelId || !messageContainer || !messageInput) return;

        const tempTimestamp = new Date().toISOString();
        const placeholderEl = messageContainer.querySelector('.no-messages-placeholder');
        if (placeholderEl) placeholderEl.remove();

        const messageItem = document.createElement('div');
        messageItem.className = 'message-item sent';
        messageItem.dataset.timestamp = tempTimestamp;
        messageItem.innerHTML = `
            <div class="message-content">
                <div class="message-bubble">${escapeHTML(content)}</div>
                <span class="message-timestamp">${formatTimestamp(tempTimestamp)} (发送中...)</span>
            </div>`;
        messageContainer.appendChild(messageItem);
        scrollToBottom(messageContainer);

        const originalMessageValue = messageInput.value;
        messageInput.value = '';
        messageInput.style.height = 'auto';
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
                const optimisticMessageElement = messageContainer.querySelector(`[data-timestamp="${tempTimestamp}"]`);
                if (optimisticMessageElement) {
                    optimisticMessageElement.dataset.timestamp = data.message.timestamp;
                    const timeSpan = optimisticMessageElement.querySelector('.message-timestamp');
                    if (timeSpan) timeSpan.textContent = formatTimestamp(data.message.timestamp);
                }
            } else {
                if (window.showMessage) window.showMessage('发送消息失败: ' + (data.error || '未知错误'), 'error');
                if (messageItem) messageItem.classList.add('message-failed');
                messageInput.value = originalMessageValue;
            }
        } catch (error) {
            console.error('发送消息请求失败:', error);
            if (window.showMessage) window.showMessage('发送消息请求失败', 'error');
            if (messageItem) messageItem.classList.add('message-failed');
            messageInput.value = originalMessageValue;
        }
    }

    function updateCalculation() {
        if (!startDateInput || !monthsInput || !calculatedEndDateSpan || !hiddenEndDateInput) return;

        const startDateStr = startDateInput.value;
        const months = parseInt(monthsInput.value);

        if (!startDateStr || isNaN(months) || months <= 0) {
            calculatedEndDateSpan.textContent = '--';
            if (hiddenEndDateInput) hiddenEndDateInput.value = '';
            return;
        }

        const startDate = new Date(startDateStr);
        if (isNaN(startDate.getTime())) {
            calculatedEndDateSpan.textContent = '--';
            if (hiddenEndDateInput) hiddenEndDateInput.value = '';
            return;
        }
        const endDate = new Date(startDate);
        endDate.setMonth(endDate.getMonth() + months);
        if (endDate.getDate() !== startDate.getDate()) {
            endDate.setDate(0);
        }

        const endDateStr = endDate.toISOString().split('T')[0];
        calculatedEndDateSpan.textContent = endDateStr;
        if (hiddenEndDateInput) hiddenEndDateInput.value = endDateStr;
    }

    // Event listeners
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
            if (channelId && channelId !== activeChannelId) {
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

            const monthlyRentValue = monthlyRentInput ? monthlyRentInput.value : null;
            const startDate = startDateInput ? startDateInput.value : null;
            const endDate = hiddenEndDateInput ? hiddenEndDateInput.value : null; // Get from hidden input
            const depositValue = depositInput ? depositInput.value : null;

            const paymentFrequencyValue = paymentFrequencySelect ? paymentFrequencySelect.value : "";
            const leasePurposeValue = leasePurposeInput ? leasePurposeInput.value.trim() : "";
            const notesValue = otherAgreementsTextarea ? otherAgreementsTextarea.value.trim() : "";

            if (!activeChannelId || !activeTenantUsername) {
                if(window.showMessage) window.showMessage("无法确定聊天对象，请重新选择聊天或刷新页面。", 'error');
                return;
            }

            if (!startDate || !endDate || !monthlyRentValue || depositValue === null) { // depositValue can be 0
                if (window.showMessage) window.showMessage("请填写所有核心合同信息 (月租金、押金、开始日期、月数)。", 'warning');
                return;
            }
            const parsedMonthlyRent = parseFloat(monthlyRentValue);
            const parsedDeposit = parseFloat(depositValue);

            if (isNaN(parsedMonthlyRent) || parsedMonthlyRent <= 0) {
                if (window.showMessage) window.showMessage("月租金必须是大于0的有效数字。", 'warning');
                return;
            }
            if (isNaN(parsedDeposit) || parsedDeposit < 0) {
                if (window.showMessage) window.showMessage("押金必须是大于等于0的有效数字。", 'warning');
                return;
            }

            // Ensure end date is calculated and available
            if (!endDate) {
                updateCalculation(); // Attempt to calculate it again
                const finalEndDate = hiddenEndDateInput ? hiddenEndDateInput.value : null;
                if (!finalEndDate) {
                    if (window.showMessage) window.showMessage("无法计算结束日期，请检查开始日期和月数。", 'warning');
                    return;
                }
            }


            const payload = {
                channel_id: activeChannelId,
                // receiver_username is the tenant in this context (房东发送给租客)
                // This will be set on the server-side based on channel info or can be explicitly sent
                // For this form, activeTenantUsername is the receiver.
                receiver_username: activeTenantUsername,
                start_date: startDate,
                end_date: endDate, // Use the value from hiddenEndDateInput
                total_amount: parsedMonthlyRent.toFixed(2), // This is the monthly rent
                deposit_amount_numeric: parsedDeposit.toFixed(2), // Numeric deposit

                rent_payment_frequency: paymentFrequencyValue,
                lease_purpose_text: leasePurposeValue,
                other_agreements_text: notesValue // from contract_notes textarea
            };

            fetch(`/feedback/send_contract`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            })
                .then(res => {
                    if (!res.ok) {
                        return res.json().then(errData => {
                            throw new Error(errData.msg || `网络或服务器错误：${res.status}`);
                        }).catch(() => {
                            throw new Error(`网络或服务器错误：${res.statusText || res.status}`);
                        });
                    }
                    return res.json();
                })
                .then(data => {
                    if (data.success) {
                        if (window.showMessage) window.showMessage(data.msg || "合同已发送", 'success');
                        else alert(data.msg || "合同已发送");

                        if (contractModal) contractModal.style.display = 'none';

                        if (data.new_message && messageContainer) {
                            const newMessageData = data.new_message;
                            const placeholderEl = messageContainer.querySelector('.no-messages-placeholder');
                            if (placeholderEl) placeholderEl.remove();

                            const messageItem = document.createElement('div');
                            messageItem.className = 'message-item sent'; // Contract message sent by current user (landlord)
                            messageItem.dataset.timestamp = newMessageData.timestamp;
                            messageItem.innerHTML = `
                        <div class="message-content">
                            <div class="message-bubble">${escapeHTML(newMessageData.content)}</div>
                            <span class="message-timestamp">${formatTimestamp(newMessageData.timestamp)}</span>
                        </div>`;
                            messageContainer.appendChild(messageItem);
                            scrollToBottom(messageContainer);
                        }
                    } else {
                        if (window.showMessage) window.showMessage("发送失败：" + (data.msg || "未知错误"), 'error');
                        else alert("发送失败：" + (data.msg || "未知错误"));
                    }
                })
                .catch(err => {
                    console.error("发送合同请求出错：", err);
                    if (window.showMessage) window.showMessage("请求失败：" + err.message, 'error');
                    else alert("请求失败：" + err.message);
                });
        });
    }

    // Initial load
    if (initialChannelId) {
        loadChat(initialChannelId);
    } else if (chatListItems.length > 0) {
        if (messageContainer) messageContainer.innerHTML = '<p class="no-messages-placeholder">请在左侧选择一个聊天开始对话</p>';
    } else {
        if (messageContainer) messageContainer.innerHTML = '<p class="no-messages-placeholder">暂无聊天会话</p>';
    }
});