document.addEventListener('DOMContentLoaded', function () {
    const aiChatIcon = document.getElementById('ai-chat-icon-container');
    const aiChatWindow = document.getElementById('ai-chat-window');
    const closeChatButton = document.getElementById('ai-chat-close-button');
    const chatMessagesContainer = document.getElementById('ai-chat-messages-container');
    const chatInput = document.getElementById('ai-chat-input');
    const chatSendButton = document.getElementById('ai-chat-send-button');
    const clearHistoryButton = document.getElementById('ai-chat-clear-history');
    const analyzePageButton = document.getElementById('ai-chat-analyze-page');
    const aiChatTypingIndicator = document.getElementById('ai-chat-typing-indicator');
    const aiChatHeader = document.getElementById('ai-chat-header');

    let chatHistoryLoaded = false;
    let currentAssistantMessageElement = null;
    let accumulatedStreamContent = '';

    // 拖拽相关变量
    let isDragging = false;
    let dragOffset = { x: 0, y: 0 };
    // 调整大小相关变量
    let isResizing = false;
    let resizeStartX = 0;
    let resizeStartY = 0;
    let resizeStartWidth = 0;
    let resizeStartHeight = 0;

    // 获取页面内容的函数
    function getPageContent() {
        try {
            // 克隆整个文档
            const clonedDoc = document.cloneNode(true);

            // 移除AI聊天相关元素
            const elementsToRemove = [
                '#ai-chat-icon-container',
                '#ai-chat-window',
                '.user-sidebar', // 假设这是用户侧边栏的选择器
                'script',
                'style'
            ];

            elementsToRemove.forEach(selector => {
                const elements = clonedDoc.querySelectorAll(selector);
                elements.forEach(el => el.remove());
            });

            // 获取主要内容区域
            const mainContent = clonedDoc.querySelector('.container') || clonedDoc.querySelector('main') || clonedDoc.body;

            if (mainContent) {
                // 提取文本内容，保留一些结构信息
                let content = '';
                const walker = document.createTreeWalker(
                    mainContent,
                    NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT,
                    {
                        acceptNode: function(node) {
                            if (node.nodeType === Node.TEXT_NODE) {
                                return node.textContent.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
                            }
                            if (node.nodeType === Node.ELEMENT_NODE) {
                                const tagName = node.tagName.toLowerCase();
                                // 忽略脚本、样式等标签
                                if (['script', 'style', 'noscript', 'button', 'input', 'textarea', 'select', 'option', 'label', 'form', 'a'].includes(tagName)) {
                                    // 对于链接，可以考虑提取其文本或href，但这里简单忽略
                                    return NodeFilter.FILTER_REJECT;
                                }
                                // 忽略具有特定类名的交互元素，例如导航栏中的按钮
                                if (node.closest('nav') || node.closest('.header-nav') || node.closest('.footer-nav')) {
                                    return NodeFilter.FILTER_REJECT;
                                }
                                return NodeFilter.FILTER_ACCEPT;
                            }
                            return NodeFilter.FILTER_REJECT;
                        }
                    }
                );

                let node;
                while (node = walker.nextNode()) {
                    if (node.nodeType === Node.TEXT_NODE) {
                        const text = node.textContent.trim();
                        if (text) {
                            content += text + ' ';
                        }
                    } else if (node.nodeType === Node.ELEMENT_NODE) {
                        const tagName = node.tagName.toLowerCase();
                        // 在某些标签后添加换行
                        if (['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'br', 'li', 'tr', 'article', 'section'].includes(tagName)) {
                            if (!content.endsWith('\n')) { // 避免连续换行
                                content += '\n';
                            }
                        }
                    }
                }

                // 清理多余的空白字符
                content = content.replace(/\s+/g, ' ').replace(/\n\s+/g, '\n').replace(/\n{2,}/g, '\n').trim();
                return content;
            }

            return '';
        } catch (error) {
            console.error('获取页面内容时出错:', error);
            return '';
        }
    }

    // 初始化拖拽功能
    function initializeDragging() {
        if (!aiChatHeader || !aiChatWindow) return;

        aiChatHeader.addEventListener('mousedown', function(e) {
            // 检查是否点击的是按钮或调整大小手柄
            if (e.target.tagName === 'BUTTON' || e.target.classList.contains('resize-handle')) return;

            isDragging = true;
            aiChatWindow.classList.add('dragging');

            const rect = aiChatWindow.getBoundingClientRect();
            dragOffset.x = e.clientX - rect.left;
            dragOffset.y = e.clientY - rect.top;

            e.preventDefault();
        });

        document.addEventListener('mousemove', function(e) {
            if (!isDragging) return;

            const windowWidth = window.innerWidth;
            const windowHeight = window.innerHeight;
            const chatWidth = aiChatWindow.offsetWidth;
            const chatHeight = aiChatWindow.offsetHeight;

            let newX = e.clientX - dragOffset.x;
            let newY = e.clientY - dragOffset.y;

            // 限制在窗口范围内
            newX = Math.max(0, Math.min(newX, windowWidth - chatWidth));
            newY = Math.max(0, Math.min(newY, windowHeight - chatHeight));

            aiChatWindow.style.left = newX + 'px';
            aiChatWindow.style.top = newY + 'px';
            aiChatWindow.style.right = 'auto';
            aiChatWindow.style.bottom = 'auto';
        });

        document.addEventListener('mouseup', function() {
            if (isDragging) {
                isDragging = false;
                aiChatWindow.classList.remove('dragging');
            }
        });
    }

    // 初始化调整大小功能
    function initializeResizing() {
        if (!aiChatWindow) return;

        let resizeHandle = aiChatWindow.querySelector('.resize-handle');
        if (!resizeHandle) {
            resizeHandle = document.createElement('div');
            resizeHandle.className = 'resize-handle';
            // 样式可以移到CSS文件中
            resizeHandle.style.cssText = `
                position: absolute;
                bottom: 0;
                right: 0;
                width: 20px;
                height: 20px;
                cursor: se-resize;
                z-index: 1001; /* Ensure it's above other elements in the chat window */
                /* background: rgba(0,0,0,0.1); // Optional: make handle visible for debugging */
            `;
            aiChatWindow.appendChild(resizeHandle);
        }

        resizeHandle.addEventListener('mousedown', function(e) {
            isResizing = true;
            resizeStartX = e.clientX;
            resizeStartY = e.clientY;
            resizeStartWidth = parseInt(window.getComputedStyle(aiChatWindow).width, 10);
            resizeStartHeight = parseInt(window.getComputedStyle(aiChatWindow).height, 10);
            e.preventDefault();
            e.stopPropagation(); // 防止触发拖拽
        });

        document.addEventListener('mousemove', function(e) {
            if (!isResizing) return;

            const newWidth = resizeStartWidth + (e.clientX - resizeStartX);
            const newHeight = resizeStartHeight + (e.clientY - resizeStartY);

            const minWidth = 320;
            const minHeight = 400;
            // 确保不会拖动到屏幕外或过小
            const maxWidth = Math.min(800, window.innerWidth - parseFloat(aiChatWindow.style.left || 0) - 20);
            const maxHeight = Math.min(800, window.innerHeight - parseFloat(aiChatWindow.style.top || 0) - 20);


            const finalWidth = Math.max(minWidth, Math.min(newWidth, maxWidth));
            const finalHeight = Math.max(minHeight, Math.min(newHeight, maxHeight));

            aiChatWindow.style.width = finalWidth + 'px';
            aiChatWindow.style.height = finalHeight + 'px';
        });

        document.addEventListener('mouseup', function() {
            isResizing = false;
        });
    }

    if (chatInput) {
        chatInput.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }

    function addMessageToUI(message, role, isStreamingUpdate = false) {
        if (!chatMessagesContainer) return;

        if (role === 'assistant') {
            if (isStreamingUpdate && currentAssistantMessageElement) {
                accumulatedStreamContent += message;
                const unsafeHtml = marked.parse(accumulatedStreamContent); // Assuming 'marked' is available
                currentAssistantMessageElement.innerHTML = DOMPurify.sanitize(unsafeHtml); // Assuming 'DOMPurify' is available

                const cursorSpan = document.createElement('span');
                cursorSpan.className = 'ai-chat-streaming-cursor';
                currentAssistantMessageElement.appendChild(cursorSpan);

            } else {
                accumulatedStreamContent = message;
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('ai-chat-message', `ai-chat-${role}`);

                const unsafeHtml = marked.parse(accumulatedStreamContent);
                messageDiv.innerHTML = DOMPurify.sanitize(unsafeHtml);

                chatMessagesContainer.appendChild(messageDiv);
                currentAssistantMessageElement = messageDiv;

                if (message === "" || isStreamingUpdate) {
                    const cursorSpan = document.createElement('span');
                    cursorSpan.className = 'ai-chat-streaming-cursor';
                    currentAssistantMessageElement.appendChild(cursorSpan);
                }
            }
        } else {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('ai-chat-message', `ai-chat-${role}`);
            messageDiv.textContent = message; // For user/system messages, plain text is usually fine
            chatMessagesContainer.appendChild(messageDiv);
            currentAssistantMessageElement = null;
        }
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    }

    function finalizeAssistantMessage() {
        if (currentAssistantMessageElement) {
            const unsafeHtml = marked.parse(accumulatedStreamContent);
            currentAssistantMessageElement.innerHTML = DOMPurify.sanitize(unsafeHtml);
            currentAssistantMessageElement = null;
            accumulatedStreamContent = '';
        }
    }

    async function loadChatHistory() {
        if (chatHistoryLoaded && clearHistoryButton && !clearHistoryButton.disabled) return;
        if (aiChatTypingIndicator) aiChatTypingIndicator.style.display = 'block';

        try {
            const response = await fetch('/ai_chat/get_history');
            if (!response.ok) {
                console.error('Failed to load chat history:', response.statusText);
                addMessageToUI('无法加载历史记录。', 'system');
                return;
            }
            const history = await response.json();
            if (chatMessagesContainer) chatMessagesContainer.innerHTML = '';
            history.forEach(item => {
                if (item.role === 'user') {
                    addMessageToUI(item.content, item.role);
                } else if (item.role === 'assistant') {
                    accumulatedStreamContent = item.content;
                    addMessageToUI(item.content, item.role, false);
                    finalizeAssistantMessage();
                }
            });
            chatHistoryLoaded = true;
        } catch (error) {
            console.error('Error loading chat history:', error);
            addMessageToUI('加载历史记录时出错。', 'system');
        } finally {
            if (aiChatTypingIndicator) aiChatTypingIndicator.style.display = 'none';
            if (chatMessagesContainer) chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
        }
    }

    function toggleChatWindow() {
        if (!aiChatWindow || !aiChatIcon || !chatInput) return;
        const isHidden = aiChatWindow.classList.contains('hidden');
        if (isHidden) {
            aiChatWindow.classList.remove('hidden');
            aiChatIcon.classList.add('hidden');
            if (!chatHistoryLoaded) {
                loadChatHistory();
            }
            chatInput.focus();
            chatInput.style.height = 'auto';
            chatInput.style.height = (chatInput.scrollHeight) + 'px';
        } else {
            aiChatWindow.classList.add('hidden');
            aiChatIcon.classList.remove('hidden');
        }
    }

    async function analyzePage() {
        if (!analyzePageButton || !chatInput || !chatSendButton || !clearHistoryButton || !chatMessagesContainer) return;

        analyzePageButton.classList.add('analyzing');
        analyzePageButton.disabled = true;
        chatInput.disabled = true;
        chatSendButton.disabled = true;
        clearHistoryButton.disabled = true;

        if (aiChatTypingIndicator) aiChatTypingIndicator.style.display = 'block';

        try {
            const pageContent = getPageContent();
            if (!pageContent.trim()) {
                addMessageToUI('无法获取页面内容进行分析。', 'system');
                return;
            }
            addMessageToUI('请分析当前页面的内容', 'user');
            addMessageToUI("", 'assistant', false); // Initialize assistant message bubble

            const response = await fetch('/ai_chat/send_message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: '请分析当前页面的内容，包括主要功能、页面结构和用户可以进行的操作。',
                    pageContent: pageContent
                }),
            });

            if (!response.ok || !response.body) {
                finalizeAssistantMessage(); // Clean up empty bubble
                if(currentAssistantMessageElement) currentAssistantMessageElement.remove(); // remove bubble
                const errorData = response.ok ? { error: "响应体为空" } : await response.json().catch(() => ({error: response.statusText}));
                addMessageToUI(`分析页面时出错: ${errorData.error || response.statusText}`, 'system');
                return;
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const { value, done } = await reader.read();
                if (done) {
                    finalizeAssistantMessage();
                    break;
                }
                buffer += decoder.decode(value, { stream: true });
                let separatorIndex;
                while ((separatorIndex = buffer.indexOf('\n\n')) >= 0) {
                    const line = buffer.substring(0, separatorIndex);
                    buffer = buffer.substring(separatorIndex + 2);
                    if (line.startsWith('data: ')) {
                        const chunk = line.substring(6).trim();
                        if (chunk) {
                            try {
                                const jsonResponse = JSON.parse(chunk);
                                if (jsonResponse.error) {
                                    finalizeAssistantMessage();
                                    if(currentAssistantMessageElement) currentAssistantMessageElement.remove();
                                    addMessageToUI(`AI 分析错误: ${jsonResponse.error}`, 'system');
                                    return; // Stop further processing on error
                                }
                                if (jsonResponse.content) {
                                    addMessageToUI(jsonResponse.content, 'assistant', true);
                                }
                                if (jsonResponse.done) {
                                    finalizeAssistantMessage(); // Finalize even if more chunks might come, safety
                                }
                            } catch (e) {
                                console.error('Error parsing JSON chunk:', e, "Chunk:", chunk);
                            }
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error analyzing page:', error);
            finalizeAssistantMessage();
            if(currentAssistantMessageElement) currentAssistantMessageElement.remove();
            addMessageToUI('页面分析时出错，请检查网络连接或联系管理员。', 'system');
        } finally {
            if (aiChatTypingIndicator) aiChatTypingIndicator.style.display = 'none';
            analyzePageButton.classList.remove('analyzing');
            analyzePageButton.disabled = false;
            chatInput.disabled = false;
            chatSendButton.disabled = false;
            clearHistoryButton.disabled = false;
            chatInput.focus();
            chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
        }
    }

    if (aiChatIcon) aiChatIcon.addEventListener('click', toggleChatWindow);
    if (closeChatButton) closeChatButton.addEventListener('click', toggleChatWindow);
    if (analyzePageButton) analyzePageButton.addEventListener('click', analyzePage);

    document.addEventListener('keydown', function (event) {
        if (event.ctrlKey && event.altKey && (event.key === 'h' || event.key === 'H')) {
            event.preventDefault();
            toggleChatWindow();
        }
    });

    async function sendMessage() {
        if (!chatInput || !chatSendButton || !clearHistoryButton || !chatMessagesContainer) return;
        const messageText = chatInput.value.trim();
        if (!messageText) return;

        addMessageToUI(messageText, 'user');
        chatInput.value = '';
        chatInput.style.height = 'auto';
        chatInput.disabled = true;
        chatSendButton.disabled = true;
        clearHistoryButton.disabled = true;
        if (analyzePageButton) analyzePageButton.disabled = true;
        if (aiChatTypingIndicator) aiChatTypingIndicator.style.display = 'block';

        addMessageToUI("", 'assistant', false); // Initialize assistant message bubble

        try {
            const pageContent = getPageContent();
            const response = await fetch('/ai_chat/send_message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: messageText, pageContent: pageContent }),
            });

            if (!response.ok || !response.body) {
                finalizeAssistantMessage();
                if(currentAssistantMessageElement) currentAssistantMessageElement.remove();
                const errorData = response.ok ? { error: "响应体为空" } : await response.json().catch(() => ({error: response.statusText}));
                addMessageToUI(`错误: ${errorData.error || response.statusText}`, 'system');
                return;
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const { value, done } = await reader.read();
                if (done) {
                    finalizeAssistantMessage();
                    break;
                }
                buffer += decoder.decode(value, { stream: true });
                let separatorIndex;
                while ((separatorIndex = buffer.indexOf('\n\n')) >= 0) {
                    const line = buffer.substring(0, separatorIndex);
                    buffer = buffer.substring(separatorIndex + 2);
                    if (line.startsWith('data: ')) {
                        const chunk = line.substring(6).trim();
                        if (chunk) {
                            try {
                                const jsonResponse = JSON.parse(chunk);
                                if (jsonResponse.error) {
                                    finalizeAssistantMessage();
                                    if(currentAssistantMessageElement) currentAssistantMessageElement.remove();
                                    addMessageToUI(`AI 错误: ${jsonResponse.error}`, 'system');
                                    return;
                                }
                                if (jsonResponse.content) {
                                    addMessageToUI(jsonResponse.content, 'assistant', true);
                                }
                                if (jsonResponse.done) {
                                    finalizeAssistantMessage();
                                }
                            } catch (e) {
                                console.error('Error parsing JSON chunk:', e, "Chunk:", chunk);
                            }
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error sending message:', error);
            finalizeAssistantMessage();
            if(currentAssistantMessageElement) currentAssistantMessageElement.remove();
            addMessageToUI('发送消息时若出错，请检查网络连接或联系管理员。', 'system');
        } finally {
            if (aiChatTypingIndicator) aiChatTypingIndicator.style.display = 'none';
            chatInput.disabled = false;
            chatSendButton.disabled = false;
            clearHistoryButton.disabled = false;
            if (analyzePageButton) analyzePageButton.disabled = false;
            chatInput.focus();
            chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
        }
    }

    if (chatSendButton) chatSendButton.addEventListener('click', sendMessage);
    if (chatInput) {
        chatInput.addEventListener('keypress', function (event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            } else if (event.key === 'Enter' && event.shiftKey) {
                setTimeout(() => {
                    this.style.height = 'auto';
                    this.style.height = (this.scrollHeight) + 'px';
                }, 0);
            }
        });
    }

    if (clearHistoryButton) {
        clearHistoryButton.addEventListener('click', async () => {
            if (!chatInput || !chatSendButton || !clearHistoryButton || !chatMessagesContainer) return;

            let confirmed = false;
            // MODIFIED: Using window.showConfirm
            if (window.showConfirm) {
                confirmed = await window.showConfirm("确定要清除当前对话的所有记录吗？此操作将保留系统提示。", { // Clarified system messages retention
                    title: "清除确认",
                    type: "warning",
                    confirmText: "确定清除",
                    cancelText: "取消"
                });
            } else { // Fallback to native confirm
                confirmed = confirm("确定要清除当前对话的所有记录吗？此操作将保留系统提示。");
            }

            if (!confirmed) {
                return;
            }

            chatInput.disabled = true;
            chatSendButton.disabled = true;
            clearHistoryButton.disabled = true;
            if (analyzePageButton) analyzePageButton.disabled = true;
            if (aiChatTypingIndicator) aiChatTypingIndicator.style.display = 'block';

            try {
                const response = await fetch('/ai_chat/clear_history', { method: 'POST' });
                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({ message: response.statusText }));
                    addMessageToUI(`清除历史记录失败: ${errorData.message || response.statusText}`, 'system');
                    return;
                }
                chatMessagesContainer.innerHTML = ''; // Clear UI
                addMessageToUI('聊天记录已清除。新的对话开始了。', 'system'); // Add system message to chat UI
                chatHistoryLoaded = false; // Allow reloading history if needed, or set to true if new session starts clean
                currentAssistantMessageElement = null;
                accumulatedStreamContent = '';
                // Optionally, call loadChatHistory() if you want to fetch a "new session started" message from backend
            } catch (error) {
                console.error('Error clearing chat history:', error);
                addMessageToUI('清除历史记录时出错。', 'system');
            } finally {
                if (aiChatTypingIndicator) aiChatTypingIndicator.style.display = 'none';
                chatInput.disabled = false;
                chatSendButton.disabled = false;
                clearHistoryButton.disabled = false;
                if (analyzePageButton) analyzePageButton.disabled = false;
                chatInput.focus();
            }
        });
    }

    initializeDragging();
    initializeResizing();
});