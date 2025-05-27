/**
 * 消息提示模块
 * 用于显示成功、错误、警告等类型的提示消息
 */
class MessageToast {
    constructor() {
        this.toastContainer = null;
        this.initContainer();
    }

    /**
     * 初始化消息容器
     */
    initContainer() {
        // 如果已存在容器则直接返回
        if (document.querySelector('.toast-container')) {
            this.toastContainer = document.querySelector('.toast-container');
            return;
        }

        // 创建消息容器
        this.toastContainer = document.createElement('div');
        this.toastContainer.className = 'toast-container';
        this.toastContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            pointer-events: none;
            max-width: 400px;
        `;
        document.body.appendChild(this.toastContainer);
    }

    /**
     * 显示消息提示
     * @param {string} message 消息内容
     * @param {string} type 消息类型: success, error, warning, info
     * @param {number} duration 显示时长(毫秒)，默认3000ms
     */
    show(message, type = 'success', duration = 3000) {
        // 创建消息元素
        const messageDiv = document.createElement('div');
        messageDiv.className = `message-toast message-${type}`;
        messageDiv.textContent = message;
        
        // 设置基础样式
        messageDiv.style.cssText = `
            padding: 12px 20px;
            margin-bottom: 10px;
            border-radius: 6px;
            color: white;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            transform: translateX(100%);
            transition: all 0.3s ease;
            max-width: 100%;
            word-wrap: break-word;
            pointer-events: auto;
            cursor: pointer;
            font-size: 14px;
            line-height: 1.5;
            position: relative;
            overflow: hidden;
        `;

        // 设置不同类型的背景色
        this.setTypeStyle(messageDiv, type);

        // 添加关闭按钮
        this.addCloseButton(messageDiv);

        // 添加到容器
        this.toastContainer.appendChild(messageDiv);

        // 显示动画
        setTimeout(() => {
            messageDiv.style.transform = 'translateX(0)';
        }, 100);

        // 自动隐藏
        const hideTimeout = setTimeout(() => {
            this.hide(messageDiv);
        }, duration);

        // 点击关闭
        messageDiv.addEventListener('click', () => {
            clearTimeout(hideTimeout);
            this.hide(messageDiv);
        });

        return messageDiv;
    }

    /**
     * 设置消息类型样式
     * @param {HTMLElement} element 消息元素
     * @param {string} type 消息类型
     */
    setTypeStyle(element, type) {
        const styles = {
            success: 'linear-gradient(135deg, #28a745, #20c997)',
            error: 'linear-gradient(135deg, #dc3545, #e74c3c)',
            warning: 'linear-gradient(135deg, #ffc107, #fd7e14)',
            info: 'linear-gradient(135deg, #17a2b8, #007bff)'
        };
        
        element.style.background = styles[type] || styles.info;
    }

    /**
     * 添加关闭按钮
     * @param {HTMLElement} element 消息元素
     */
    addCloseButton(element) {
        const closeBtn = document.createElement('span');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.cssText = `
            position: absolute;
            top: 8px;
            right: 12px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            opacity: 0.8;
        `;
        closeBtn.addEventListener('mouseenter', () => {
            closeBtn.style.opacity = '1';
        });
        closeBtn.addEventListener('mouseleave', () => {
            closeBtn.style.opacity = '0.8';
        });
        element.appendChild(closeBtn);
        
        // 为了给关闭按钮留空间，调整padding
        element.style.paddingRight = '40px';
    }

    /**
     * 隐藏消息
     * @param {HTMLElement} element 消息元素
     */
    hide(element) {
        element.style.transform = 'translateX(100%)';
        element.style.opacity = '0';
        
        setTimeout(() => {
            if (element.parentNode) {
                element.parentNode.removeChild(element);
            }
        }, 300);
    }

    /**
     * 清除所有消息
     */
    clear() {
        const messages = this.toastContainer.querySelectorAll('.message-toast');
        messages.forEach(msg => this.hide(msg));
    }

    // 便捷方法
    success(message, duration) {
        return this.show(message, 'success', duration);
    }

    error(message, duration) {
        return this.show(message, 'error', duration);
    }

    warning(message, duration) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration) {
        return this.show(message, 'info', duration);
    }
}

// 创建全局实例
window.messageToast = new MessageToast();

// 兼容旧版本的 showMessage 函数
window.showMessage = function(message, type = 'success', duration = 3000) {
    return window.messageToast.show(message, type, duration);
};

// 导出（如果支持模块化）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MessageToast;
}